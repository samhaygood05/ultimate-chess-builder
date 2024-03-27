'''
Copyright 2024 Sam A. Haygood

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

def parse_collection(value, collection, loaded: dict):
    new_value = value
    if type(value) != str:
        raise ValueError(f'Invalid value: {value}')
    seperated = value.split(".")
    match seperated[0]:
        case 'position':
            new_value =  collection['position']
        case 'tile':
            match seperated[1]:
                case 'type':
                    new_value = collection['tile'].types
                case 'properties':
                    if len(seperated) >= 3:
                        try:
                            new_value = collection['tile'].properties['.'.join(seperated[2:])]
                        except KeyError:
                            raise ValueError(f'Invalid value: {value}')
                    else:
                        raise ValueError(f'Invalid value: {value}')
                case 'piece':
                    raise ValueError(f"Access piece using 'collection.piece' instead of 'collection.tile.piece'")
                case _:
                    raise ValueError(f'Invalid value: {value}')
        case 'piece':
            if len(seperated) == 1:
                new_value =  collection['piece']
            else:
                match seperated[1]:
                    case 'type':
                        if len(seperated) == 2:
                            new_value = None if collection['piece'] == None else collection['piece'].piece_type
                        elif seperated[2] == 'properties':
                            new_value = None if collection['piece'] == None else loaded['pieces'][collection['piece'].piece_type].properties['.'.join(seperated[3:])]
                        elif seperated[2] == 'is_royal':
                            new_value = None if collection['piece'] == None else loaded['pieces'][collection['piece'].piece_type].is_royal
                        else:
                            raise ValueError(f'Invalid value: {value}')
                    case 'teams':
                        new_value = None if collection['piece'] == None else collection['piece'].teams
                    case 'facing':
                        new_value = None if collection['piece'] == None else collection['piece'].facing
                    case 'has_moved':
                        new_value = None if collection['piece'] == None else collection['piece'].has_moved
                    case 'properties':
                        if len(seperated) >= 2:
                            if collection['piece'] == None:
                                new_value = None
                            try:
                                new_value = collection['piece'].properties['.'.join(seperated[2:])]
                            except KeyError:
                                new_value = None
                        else:
                            raise ValueError(f'Invalid value: {value}')
                    case _:
                        raise ValueError(f'Invalid value: {value}')
        case 'allies':
            new_value = collection['allies']
        case _:
            raise ValueError(f'Invalid value: {value}')
    return new_value

def parse(value, loaded: dict):
    value_func = lambda board, source, target, extra, team: value
    if type(value) == str:
        seperated = value.split(".")
        if len(seperated) > 1:
            match seperated[0]:
                case 'board':
                    match seperated[1]:
                        case 'distance':
                            if len(seperated) == 2:
                                value_func = lambda board, source, target: board.distance(source['position'], target['position'])
                            elif len(seperated) == 4:
                                position1 = seperated[2]
                                position2 = seperated[3]
                                def func(board, source, target):
                                    if position1 == 'source':
                                        pos1 = source['position']
                                    elif position1 == 'target':
                                        pos1 = target['position']
                                    else:
                                        pos1 = position1
                                    if position2 == 'source':
                                        pos2 = source['position']
                                    elif position2 == 'target':
                                        pos2 = target['position']
                                    else:
                                        pos2 = position2
                                    return board.distance(pos1, pos2)
                                value_func = func
                            else:
                                raise ValueError(f'Invalid value: {value}')
                        case 'current_team':
                            value_func = lambda board, source, target: board.current_team
                case 'source':
                    new_value = '.'.join(seperated[1:])
                    value_func = lambda board, source, target, extra, team: parse_collection(new_value, source, loaded)
                case 'target':
                    new_value = '.'.join(seperated[1:])
                    value_func = lambda board, source, target, extra, team: parse_collection(new_value, target, loaded)
                case 'extra':
                    index = int(seperated[1])
                    new_value = '.'.join(seperated[2:])
                    def func(board, source, target, extra, team):
                        try:
                            return parse_collection(new_value, extra[index], loaded)
                        except IndexError:
                            raise ValueError(f'{index} is out of range. extra only has {len(extra)} elements')
                    value_func = func
                case 'team':
                    if len(seperated) == 1:
                        value_func = lambda board, source, target, extra, team: team.name
                    else:
                        match seperated[1]:
                            case 'type':
                                if len(seperated) == 2:
                                    value_func = lambda board, source, target, extra, team: team.type
                                elif seperated[2] == 'properties':
                                    value_func = lambda board, source, target, extra, team: loaded['teams'][team.type].properties['.'.join(seperated[3:])]
                                elif seperated[2] == 'name':
                                    raise ValueError(f"Access team type name using 'team.type' instead of 'team.type.name'")
                                else:
                                    raise ValueError(f'Invalid value: {value}')
                            case 'name':
                                raise ValueError(f"Access team name using 'team' instead of 'team.name'")
                            case 'properties':
                                if len(seperated) >= 2:
                                    try:
                                        value_func = lambda board, source, target, extra, team: team.properties['.'.join(seperated[2:])]
                                    except KeyError:
                                        value_func = lambda board, source, target, extra, team: None
                                else:
                                    raise ValueError(f'Invalid value: {value}')
                            case _:
                                raise ValueError(f'Invalid value: {value}')
                case _:
                    value_func = lambda board, source, target, extra, team: value
    elif type(value) == 'Selector':
        value_func = lambda board, source, target, extra, team: value.evaluate(board, source, target, loaded)
    else:
        value_func = lambda board, source, target, extra, team: value
    return value_func