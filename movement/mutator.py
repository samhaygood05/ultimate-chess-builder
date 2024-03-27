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

import json
import warnings
from util.condition import Condition
from util import util

class Mutator:
    def __init__(self, name, set_values: dict, append_values, swap: dict, remove: dict):
        self.name = name
        self.set_values = set_values
        self.append_values = append_values
        self.swap = swap
        self.remove = remove

    @staticmethod
    def build(data: dict, loaded):
        if type(data) == str:
            if data in loaded['mutators']:
                return loaded['mutators'][data]
            else:
                seperated = data.split(":")
                if len(seperated) == 2:
                    file_path = f"games/{seperated[0]}/data/mutators/{seperated[1]}.json"
                    return Mutator.build_from_file(file_path, loaded)
        else:
            name = None
            set_values = {}
            append_values = {}
            swap = {'tile': {}, 'piece': {}}
            remove = {'source': Condition.FALSE, 'target': Condition.FALSE}
            if 'name' in data:
                name = data['name']
            if 'set' in data:
                for key, value in data['set'].items():
                    set_values[key] = value
            if 'append' in data:
                for key, value in data['append'].items():
                    append_values[key] = value
            if 'swap' in data:
                swap = data['swap']
            if 'remove' in data:
                for key, value in data['remove'].items():
                    remove[key] = Condition.build(value, loaded)
            return Mutator(name, set_values, append_values, swap, remove)
    
    @staticmethod
    def build_from_file(file_path: str, loaded):
        try:
            with open(file_path, 'r') as file:
                split_path = file_path.split('/')
                if split_path[-2] != 'mutators' or split_path[-3] != 'data' or split_path[-1].split('.')[-1] != 'json':
                    raise ValueError(f'[{file_path}]: Invalid file path for mutator')
                data = json.load(file)
                namespace = split_path[-4]
                name = split_path[-1].split('.')[0]

                mutator = Mutator.build(data, loaded)
                mutator.name = f'{namespace}:{name}'
                return mutator

        except FileNotFoundError:
            raise FileNotFoundError(f"[{file_path}] is missing")
    
    def evaluate(self, board, source, target, extra, team, loaded):
        mutated_source = {
            'position': source['position'],
            'tile': source['tile'].__copy__(),
            'piece': source['piece'].__copy__() if source['piece'] != None else None
        }
        mutated_target = {
            'position': target['position'],
            'tile': target['tile'].__copy__(),
            'piece': target['piece'].__copy__() if target['piece'] != None else None
        }
        mutated_extra = [
            {
                'position': extra_piece['position'],
                'tile': extra_piece['tile'].__copy__(),
                'piece': extra_piece['piece'].__copy__() if extra_piece['piece'] != None else None
            } for extra_piece in extra
        ]
        mutated_team = team.__copy__()

        for key, value in self.set_values.items():
            split_key = key.split(".")
            match split_key[0]:
                case 'board':
                    raise ValueError('Board is not mutable')
                case 'source':
                    match split_key[1]:
                        case 'position':
                            raise ValueError('Position is not mutable')
                        case 'tile':
                            match split_key[2]:
                                case 'types':
                                    if len(split_key) > 3:
                                        raise ValueError(f'Tile type is not mutable')
                                    else:
                                        mutated_source['tile'].types = util.parse(value, loaded)(board, source, target, extra, team)
                                        mutated_source['tile'].types_mutated = True
                                case 'properties':
                                    if len(split_key) > 3:
                                        mutated_source['tile'].properties['.'.join(split_key[3:])] = util.parse(value, loaded)(board, source, target, extra, team)
                                    else:
                                        raise ValueError(f'Must specify a property to set')
                                case 'piece':
                                    raise ValueError(f"Access piece using 'source.piece' instead of 'source.tile.piece'")
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case 'piece':
                            match split_key[2]:
                                case 'type':
                                    if len(split_key) > 3:
                                        raise ValueError(f'Piece type is not mutable')
                                    else:
                                        mutated_source['piece'].piece_type = util.parse(value, loaded)(board, source, target, extra, team)
                                        mutated_source['piece'].type_mutated = True
                                case 'teams':
                                    mutated_source['piece'].teams = util.parse(value, loaded)(board, source, target, extra, team)
                                case 'facing':
                                    mutated_source['piece'].facing = util.parse(value, loaded)(board, source, target, extra, team)
                                case 'has_moved':
                                    mutated_source['piece'].has_moved = util.parse(value, loaded)(board, source, target, extra, team)
                                case 'properties':
                                    if len(split_key) > 3:
                                        mutated_source['piece'].properties['.'.join(split_key[3:])] = util.parse(value, loaded)(board, source, target, extra, team)
                                    else:
                                        raise ValueError(f'Must specify a property to set')
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case 'allies':
                            raise ValueError('Allies is not mutable')
                        case _:
                            raise ValueError(f'Invalid key: {key}')
                case 'target':
                    match split_key[1]:
                        case 'position':
                            raise ValueError('Position is not mutable')
                        case 'tile':
                            match split_key[2]:
                                case 'type':
                                    if len(split_key) > 3:
                                        raise ValueError(f'Tile type is not mutable')
                                    else:
                                        mutated_target['tile'].types = util.parse(value, loaded)(board, source, target, extra, team)
                                        mutated_target['tile'].types_mutated = True
                                case 'properties':
                                    if len(split_key) > 3:
                                        mutated_target['tile'].properties['.'.join(split_key[3:])] = util.parse(value, loaded)(board, source, target, extra, team)
                                    else:
                                        raise ValueError(f'Must specify a property to set')
                                case 'piece':
                                    raise ValueError(f"Access piece using 'target.piece' instead of 'target.tile.piece'")
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case 'piece':
                            match split_key[2]:
                                case 'type':
                                    if len(split_key) > 3:
                                        raise ValueError(f'Piece type is not mutable')
                                    else:
                                        mutated_target['piece'].piece_type = util.parse(value, loaded)(board, source, target, extra, team)
                                        mutated_target['piece'].type_mutated = True
                                case 'teams':
                                    mutated_target['piece'].teams = util.parse(value, loaded)(board, source, target, extra, team)
                                case 'facing':
                                    mutated_target['piece'].facing = util.parse(value, loaded)(board, source, target, extra, team)
                                case 'has_moved':
                                    mutated_target['piece'].has_moved = util.parse(value, loaded)(board, source, target, extra, team)
                                case 'properties':
                                    if len(split_key) > 3:
                                        mutated_target['piece'].properties['.'.join(split_key[3:])] = util.parse(value, loaded)(board, source, target, extra, team)
                                    else:
                                        raise ValueError(f'Must specify a property to set')
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case 'allies':
                            raise ValueError('Allies is not mutable')
                        case _:
                            raise ValueError(f'Invalid key: {key}')
                case 'extra':
                    index = int(split_key[1])
                    if index >= len(extra):
                        raise ValueError(f'Index [{index}] out of range')
                    match split_key[2]:
                        case 'position':
                            raise ValueError('Position is not mutable')
                        case 'tile':
                            match split_key[3]:
                                case 'type':
                                    if len(split_key) > 4:
                                        raise ValueError(f'Tile type is not mutable')
                                    else:
                                        mutated_extra[index]['tile'].types = util.parse(value, loaded)(board, source, target, extra, team)
                                        mutated_extra[index]['tile'].types_mutated = True
                                case 'properties':
                                    if len(split_key) > 4:
                                        mutated_extra[index]['tile'].properties['.'.join(split_key[4:])] = util.parse(value, loaded)(board, source, target, extra, team)
                                    else:
                                        raise ValueError(f'Must specify a property to set')
                                case 'piece':
                                    raise ValueError(f"Access piece using 'extra.piece' instead of 'extra.tile.piece'")
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case 'piece':
                            match split_key[3]:
                                case 'type':
                                    if len(split_key) > 4:
                                        raise ValueError(f'Piece type is not mutable')
                                    else:
                                        mutated_extra[index]['piece'].piece_type = util.parse(value, loaded)(board, source, target, extra, team)
                                        mutated_extra[index]['piece'].type_mutated = True
                                case 'teams':
                                    mutated_extra[index]['piece'].teams = util.parse(value, loaded)(board, source, target, extra, team)
                                case 'facing':
                                    mutated_extra[index]['piece'].facing = util.parse(value, loaded)(board, source, target, extra, team)
                                case 'has_moved':
                                    mutated_extra[index]['piece'].has_moved = util.parse(value, loaded)(board, source, target, extra, team)
                                case 'properties':
                                    if len(split_key) > 4:
                                        mutated_extra[index]['piece'].properties['.'.join(split_key[4:])] = util.parse(value, loaded)(board, source, target, extra, team)
                                    else:
                                        raise ValueError(f'Must specify a property to set')
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case _:
                            raise ValueError(f'Invalid key: {key}')
                case 'team':
                    match split_key[1]:
                        case 'type':
                            raise ValueError('Team type is not mutable')
                        case 'allies':
                            mutated_team.allies = util.parse(value, loaded)(board, source, target, extra, team)
                        case 'properties':
                            if len(split_key) > 2:
                                mutated_team.properties['.'.join(split_key[2:])] = util.parse(value, loaded)(board, source, target, extra, team)
                            else:
                                raise ValueError(f'Must specify a property to set')
                        case _:
                            raise ValueError(f'Invalid key: {key}')
                case _:
                    raise ValueError(f'Invalid key: {key}')
                
        for key, value in self.append_values.items():
            split_key = key.split(".")
            match split_key[0]:
                case 'board':
                    raise ValueError('Board is not mutable')
                case 'source':
                    match split_key[1]:
                        case 'position':
                            raise ValueError('Position is not mutable')
                        case 'tile':
                            match split_key[2]:
                                case 'types':
                                    if len(split_key) > 3:
                                        raise ValueError(f'Tile type is not mutable')
                                    else:
                                        mutated_source['tile'].types.append(util.parse(value, loaded)(board, source, target, extra, team))
                                        mutated_source['tile'].type_mutated = True
                                case 'properties':
                                    if len(split_key) > 3:
                                        if type(mutated_source['tile'].properties[split_key[3]]) == list:
                                            mutated_source['tile'].properties[split_key[3]].append(util.parse(value, loaded)(board, source, target, extra, team))
                                        else:
                                            raise ValueError(f'tile.properties.{split_key[3]} is not appendable')
                                    else:
                                        raise ValueError(f'Must specify a property to append')
                                case 'piece':
                                    raise ValueError(f"Access piece using 'source.piece' instead of 'source.tile.piece'")
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case 'piece':
                            match split_key[2]:
                                case 'type':
                                    if len(split_key) > 3:
                                        raise ValueError(f'Piece type is not mutable')
                                    else:
                                        raise ValueError(f'piece.type is not appendable')
                                case 'teams':
                                    mutated_source['piece'].teams.append(util.parse(value, loaded)(board, source, target, extra, team))
                                case 'facing':
                                    raise ValueError(f'piece.facing is not appendable')
                                case 'has_moved':
                                    raise ValueError(f'piece.has_moved is not appendable')
                                case 'properties':
                                    if len(split_key) > 3:
                                        if type(mutated_source['piece'].properties[split_key[3]]) == list:
                                            mutated_source['piece'].properties[split_key[3]].append(util.parse(value, loaded)(board, source, target, extra, team))
                                        else:
                                            raise ValueError(f'piece.properties.{split_key[3]} is not appendable')
                                    else:
                                        raise ValueError(f'Must specify a property to append')
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case 'allies':
                            raise ValueError('Allies is not mutable')
                        case _:
                            raise ValueError(f'Invalid key: {key}')
                case 'target':
                    match split_key[1]:
                        case 'position':
                            raise ValueError('Position is not mutable')
                        case 'tile':
                            match split_key[2]:
                                case 'type':
                                    if len(split_key) > 3:
                                        raise ValueError(f'Tile type is not mutable')
                                    else:
                                        mutated_target['tile'].types.append(util.parse(value, loaded)(board, source, target, extra, team))
                                        mutated_target['tile'].type_mutated = True
                                case 'properties':
                                    if len(split_key) > 3:
                                        if type(mutated_target['tile'].properties[split_key[3]]) == list:
                                            mutated_target['tile'].properties[split_key[3]].append(util.parse(value, loaded)(board, source, target, extra, team))
                                        else:
                                            raise ValueError(f'tile.properties.{split_key[3]} is not appendable')
                                    else:
                                        raise ValueError(f'Must specify a property to append')
                                case 'piece':
                                    raise ValueError(f"Access piece using 'target.piece' instead of 'target.tile.piece'")
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case 'piece':
                            match split_key[2]:
                                case 'type':
                                    if len(split_key) > 3:
                                        raise ValueError(f'Piece type is not mutable')
                                    else:
                                        raise ValueError(f'piece.type is not appendable')
                                case 'teams':
                                    mutated_target['piece'].teams.append(util.parse(value, loaded)(board, source, target, extra, team))
                                case 'facing':
                                    raise ValueError(f'piece.facing is not appendable')
                                case 'has_moved':
                                    raise ValueError(f'piece.has_moved is not appendable')
                                case 'properties':
                                    if len(split_key) > 3:
                                        if type(mutated_target['piece'].properties[split_key[3]]) == list:
                                            mutated_target['piece'].properties[split_key[3]].append(util.parse(value, loaded)(board, source, target, extra, team))
                                        else:
                                            raise ValueError(f'piece.properties.{split_key[3]} is not appendable')
                                    else:
                                        raise ValueError(f'Must specify a property to append')
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case 'allies':
                            raise ValueError('Allies is not mutable')
                        case _:
                            raise ValueError(f'Invalid key:  {key}')
                case 'extra':
                    index = int(split_key[1])
                    if index >= len(extra):
                        raise ValueError(f'Index [{index}] out of range')
                    match split_key[2]:
                        case 'position':
                            raise ValueError('Position is not mutable')
                        case 'tile':
                            match split_key[3]:
                                case 'type':
                                    if len(split_key) > 4:
                                        raise ValueError(f'Tile type is not mutable')
                                    else:
                                        mutated_extra[index]['tile'].types.append(util.parse(value, loaded)(board, source, target, extra, team))
                                        mutated_extra[index]['tile'].types_mutated = True
                                case 'properties':
                                    if len(split_key) > 4:
                                        if type(mutated_extra[index]['tile'].properties[split_key[4]]) == list:
                                            mutated_extra[index]['tile'].properties[split_key[4]].append(util.parse(value, loaded)(board, source, target, extra, team))
                                        else:
                                            raise ValueError(f'tile.properties.{split_key[4]} is not appendable')
                                    else:
                                        raise ValueError(f'Must specify a property to append')
                                case 'piece':
                                    raise ValueError(f"Access piece using 'extra.piece' instead of 'extra.tile.piece'")
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case 'piece':
                            match split_key[3]:
                                case 'type':
                                    if len(split_key) > 4:
                                        raise ValueError(f'Piece type is not mutable')
                                    else:
                                        raise ValueError(f'piece.type is not appendable')
                                case 'teams':
                                    mutated_extra[index]['piece'].teams.append(util.parse(value, loaded)(board, source, target, extra, team))
                                case 'facing':
                                    raise ValueError(f'piece.facing is not appendable')
                                case 'has_moved':
                                    raise ValueError(f'piece.has_moved is not appendable')
                                case 'properties':
                                    if len(split_key) > 4:
                                        if type(mutated_extra[index]['piece'].properties[split_key[4]]) == list:
                                            mutated_extra[index]['piece'].properties[split_key[4]].append(util.parse(value, loaded)(board, source, target, extra, team))
                                        else:
                                            raise ValueError(f'piece.properties.{split_key[4]} is not appendable')
                                    else:
                                        raise ValueError(f'Must specify a property to append')
                                case _:
                                    raise ValueError(f'Invalid key: {key}')
                        case _:
                            raise ValueError(f'Invalid key: {key}')
                case 'team':
                    match split_key[1]:
                        case 'type':
                            raise ValueError('Team type is not mutable')
                        case 'allies':
                            mutated_team.allies.append(util.parse(value, loaded)(board, source, target, extra, team))
                        case 'properties':
                            if len(split_key) > 2:
                                if type(mutated_team.properties['.'.join(split_key[2:])]) == list:
                                    mutated_team.properties['.'.join(split_key[2:])].append(util.parse(value, loaded)(board, source, target, extra, team))
                                else:
                                    raise ValueError(f'team.properties.{split_key[2]} is not appendable')
                            else:
                                raise ValueError(f'Must specify a property to append')
                        case _:
                            raise ValueError(f'Invalid key: {key}')
                case _:
                    raise ValueError(f'Invalid key: {key}')

        swap_tiles = []
        if self.swap['tile']:
            for key in self.swap['tile']:
                if key['tile1'] == key['tile2']:
                    warnings.warn('Swapping a tile with itself is redundant. Perhaps you made a mistake?')
                    continue
                index1 = None
                tile1 = None
                if key['tile1'] == 'source':
                    tile1 = mutated_source
                elif key['tile1'] == 'target':
                    tile1 = mutated_target
                elif key['tile1'].split(".")[0] == 'extra':
                    index1 = int(key['tile1'].split(".")[1])
                    if index1 >= len(extra):
                        raise ValueError(f'Index [{index1}] out of range')
                    tile1 = mutated_extra[index1]
                else:
                    raise ValueError(f'Invalid key: {key}')
                index2 = None
                tile2 = None
                if key['tile2'] == 'source':
                    tile2 = mutated_source
                elif key['tile2'] == 'target':
                    tile2 = mutated_target
                elif key['tile2'].split(".")[0] == 'extra':
                    index2 = int(key['tile2'].split(".")[1])
                    if index2 >= len(extra):
                        raise ValueError(f'Index [{index2}] out of range')
                    tile2 = mutated_extra[index2]
                properties = key['properties']

                for prop in properties:
                    if prop == 'full':
                        swap_tiles.append((key['tile1'], key['tile2']))
                    else:
                        prop.split(".")
                        match prop:
                            case 'type':
                                if len(prop) > 1:
                                    raise ValueError(f'Tile type is not mutable')
                                else:
                                    tile1['tile'].types, tile2['tile'].types = tile2['tile'].types, tile1['tile'].types
                                    tile1['tile'].types_mutated = True
                                    tile2['tile'].types_mutated = True
                            case 'properties':
                                if len(prop) > 1:
                                    tile1['tile'].properties[".".join(prop[1:])], tile2['tile'].properties[".".join(prop[1:])] = tile2['tile'].properties[".".join(prop[1:])], tile1['tile'].properties[".".join(prop[1:])]
                                else:
                                    raise ValueError(f'Must specify a property to swap')
                            case _:
                                raise ValueError(f'Invalid key: {prop}')
                if key['tile1'] == 'source':
                    mutated_source = tile1
                elif key['tile1'] == 'target':
                    mutated_target = tile1
                elif key['tile1'].split(".")[0] == 'extra':
                    mutated_extra[index1] = tile1
                if key['tile2'] == 'source':
                    mutated_source = tile2
                elif key['tile2'] == 'target':
                    mutated_target = tile2
                elif key['tile2'].split(".")[0] == 'extra':
                    mutated_extra[index2] = tile2

            for swap in swap_tiles:
                if swap[0] == 'source':
                    if swap[1] == 'target':
                        mutated_source, mutated_target = mutated_target, mutated_source
                    elif swap[1].split(".")[0] == 'extra':
                        index = int(swap[1].split(".")[1])
                        if index >= len(extra):
                            raise ValueError(f'Index [{index}] out of range')
                        mutated_source, mutated_extra[index] = mutated_extra[index], mutated_source
                    else:
                        raise ValueError(f'Invalid key: {swap[1]}')
                elif swap[0] == 'target':
                    if swap[1] == 'source':
                        mutated_target, mutated_source = mutated_source, mutated_target
                    elif swap[1].split(".")[0] == 'extra':
                        index = int(swap[1].split(".")[1])
                        if index >= len(extra):
                            raise ValueError(f'Index [{index}] out of range')
                        mutated_target, mutated_extra[index] = mutated_extra[index], mutated_target
                    else:
                        raise ValueError(f'Invalid key: {swap[1]}')
                elif swap[0].split(".")[0] == 'extra':
                    index1 = int(swap[0].split(".")[1])
                    if index1 >= len(extra):
                        raise ValueError(f'Index [{index1}] out of range')
                    if swap[1] == 'source':
                        mutated_extra[index1], mutated_source = mutated_source, mutated_extra[index1]
                    elif swap[1] == 'target':
                        mutated_extra[index1], mutated_target = mutated_target, mutated_extra[index1]
                    elif swap[1].split(".")[0] == 'extra':
                        index2 = int(swap[1].split(".")[1])
                        if index2 >= len(extra):
                            raise ValueError(f'Index [{index2}] out of range')
                        if index1 == index2:
                            warnings.warn(f'Swapping a tile with itself is redundant. Perhaps you made a mistake?')
                            continue
                        mutated_extra[index1], mutated_extra[index2] = mutated_extra[index2], mutated_extra[index1]
                    else:
                        raise ValueError(f'Invalid key: {swap[1]}')
        
        swap_pieces = [] 
        if self.swap['piece']:
            for key in self.swap['piece']:
                if key['piece1'] == key['piece2']:
                    warnings.warn('Swapping a piece with itself is redundant. Perhaps you made a mistake?')
                    continue
                index1 = None
                piece1 = None
                if key['piece1'] == 'source':
                    piece1 = mutated_source
                elif key['piece1'] == 'target':
                    piece1 = mutated_target
                elif key['piece1'].split(".")[0] == 'extra':
                    index1 = int(key['piece1'].split(".")[1])
                    if index1 >= len(extra):
                        raise ValueError(f'Index [{index1}] out of range')
                    piece1 = mutated_extra[index1]
                else:
                    raise ValueError(f'Invalid key: {key}')
                index2 = None
                piece2 = None
                if key['piece2'] == 'source':
                    piece2 = mutated_source
                elif key['piece2'] == 'target':
                    piece2 = mutated_target
                elif key['piece2'].split(".")[0] == 'extra':
                    index2 = int(key['piece2'].split(".")[1])
                    if index2 >= len(extra):
                        raise ValueError(f'Index [{index2}] out of range')
                    piece2 = mutated_extra[index2]
                properties = key['properties']
                for prop in properties:
                    if prop == 'full':
                        swap_pieces.append((key['piece1'], key['piece2']))
                    elif piece1['piece'] == None or piece2['piece'] == None:
                        continue
                    else:
                        prop.split(".")
                        match prop:
                            case 'type':
                                if len(key) > 1:
                                    raise ValueError(f'Piece type is not mutable')
                                else:
                                    piece1['piece'].type, piece2['piece'].type = piece2['piece'].type, piece1['piece'].type
                                    piece1['piece'].type_mutated = True
                                    piece2['piece'].type_mutated = True
                            case 'teams':
                                piece1['piece'].teams, piece2['piece'].teams = piece2['piece'].teams, piece1['piece'].teams
                            case 'facing':
                                piece1['piece'].facing, piece2['piece'].facing = piece2['piece'].facing, piece1['piece'].facing
                            case 'has_moved':
                                piece1['piece'].has_moved, piece2['piece'].has_moved = piece2['piece'].has_moved, piece1['piece'].has_moved
                            case 'properties':
                                if len(prop) > 1:
                                    piece1['piece'].properties[".".join(prop[1:])], piece2['piece'].properties[".".join(prop[1:])] = piece2['piece'].properties[".".join(prop[1:])], piece1['piece'].properties[".".join(prop[1:])]
                                else:
                                    raise ValueError(f'Must specify a property to swap')
                            case _:
                                raise ValueError(f'Invalid key: {key}')
                if key['piece1'] == 'source':
                    mutated_source = piece1
                elif key['piece1'] == 'target':
                    mutated_target = piece1
                elif key['piece1'].split(".")[0] == 'extra':
                    mutated_extra[index1] = piece1

                if key['piece2'] == 'source':
                    mutated_source = piece2
                elif key['piece2'] == 'target':
                    mutated_target = piece2
                elif key['piece2'].split(".")[0] == 'extra':
                    mutated_extra[index2] = piece2
         
        for key, value in self.remove.items():
            if key == 'source':
                if value.evaluate(board, source, target, extra, team):
                    mutated_source['piece'] = None
            elif key == 'target':
                if value.evaluate(board, source, target, extra, team):
                    mutated_target['piece'] = None
            elif key.split(".")[0] == 'extra':
                index = int(key.split(".")[1])
                if index >= len(extra):
                    raise ValueError(f'Index [{index}] out of range')
                if value.evaluate(board, source, target, extra, team):
                    mutated_extra[index]['piece'] = None

        for swap in swap_pieces:
            if swap[0] == 'source':
                if swap[1] == 'target':
                    mutated_source['piece'], mutated_target['piece'] = mutated_target['piece'], mutated_source['piece']
                elif swap[1].split(".")[0] == 'extra':
                    index = int(swap[1].split(".")[1])
                    if index >= len(extra):
                        raise ValueError(f'Index [{index}] out of range')
                    mutated_source['piece'], mutated_extra[index]['piece'] = mutated_extra[index]['piece'], mutated_source['piece']
                else:
                    raise ValueError(f'Invalid key: {swap[1]}')
            elif swap[0] == 'target':
                if swap[1] == 'source':
                    mutated_target['piece'], mutated_source['piece'] = mutated_source['piece'], mutated_target['piece']
                elif swap[1].split(".")[0] == 'extra':
                    index = int(swap[1].split(".")[1])
                    if index >= len(extra):
                        raise ValueError(f'Index [{index}] out of range')
                    mutated_target['piece'], mutated_extra[index]['piece'] = mutated_extra[index]['piece'], mutated_target['piece']
                else:
                    raise ValueError(f'Invalid key: {swap[1]}')
            elif swap[0].split(".")[0] == 'extra':
                index1 = int(swap[0].split(".")[1])
                if index1 >= len(extra):
                    raise ValueError(f'Index [{index1}] out of range')
                if swap[1] == 'source':
                    mutated_extra[index1]['piece'], mutated_source['piece'] = mutated_source['piece'], mutated_extra[index1]['piece']
                elif swap[1] == 'target':
                    mutated_extra[index1]['piece'], mutated_target['piece'] = mutated_target['piece'], mutated_extra[index1]['piece']
                elif swap[1].split(".")[0] == 'extra':
                    index2 = int(swap[1].split(".")[1])
                    if index2 >= len(extra):
                        raise ValueError(f'Index [{index2}] out of range')
                    if index1 == index2:
                        warnings.warn(f'Swapping a piece with itself is redundant. Perhaps you made a mistake?')
                        continue
                    mutated_extra[index1]['piece'], mutated_extra[index2]['piece'] = mutated_extra[index2]['piece'], mutated_extra[index1]['piece']
                else:
                    raise ValueError(f'Invalid key: {swap[1]}')

        mutated_source['tile'].piece = mutated_source['piece']
        mutated_target['tile'].piece = mutated_target['piece']
        for extra_piece in mutated_extra:
            extra_piece['tile'].piece = extra_piece['piece']

        return mutated_source, mutated_target, mutated_extra, mutated_team
            
    
    def __str__(self) -> str:
        string = "mutator:\n ├ set:\n"
        for key, value, i in zip(self.set_values.keys(), self.set_values.values(), range(len(self.set_values))):
            if i == len(self.set_values) - 1:
                string += f" │ └ {key}: {value}\n"
            else:
                string += f" │ ├ {key}: {value}\n"
        string += " ├ swap:\n"
        for key, value, i in zip(self.swap.keys(), self.swap.values(), range(len(self.swap))):
            if i == len(self.swap) - 1:
                string += f" │ └ {key}: {value}\n"
            else:
                string += f" │ ├ {key}: {value}\n"
        string += " └ remove:\n"
        for key, value, i in zip(self.remove.keys(), self.remove.values(), range(len(self.remove))):
            if i == len(self.remove) - 1:
                string += f"   └ {key}: {value}"
            else:
                string += f"   ├ {key}: {value}\n"
        return string

                

