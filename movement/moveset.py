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

from typing import List
from movement.move import Move
from movement.mutator import Mutator
from util.condition import Condition
from util.selector import Selector
import json

class Moveset:
    def __init__(self, name, moves: List[Move], min_distance=1, max_distance = -1, mutator = Mutator(None, {}, {}, {}, {}), color = 0x00FFFF88, condition = Condition(), category = 'move'):
        self.name = name
        self.moves = moves
        if min_distance < 1:
            raise ValueError('min_distance must be greater than 0')
        self.min_distance: int = min_distance
        if max_distance != -1 and max_distance < min_distance:
            raise ValueError('max_distance must be greater than or equal to min_distance')
        self.max_distance: int = max_distance
        self.mutator: Mutator|Selector = mutator # this is a mutator or a selector of mutators
        self.color: int = color # this is an RGBA color
        self.condition: Condition = condition
        self.category: str = category

    @staticmethod
    def build(data, loaded) -> 'Moveset':
        if type(data) == str:
            if data in loaded['movesets']:
                return loaded['movesets'][data]
            else:
                seperated = data.split(":")
                if len(seperated) == 2:
                    file_path = f"games/{seperated[0]}/data/movesets/{seperated[1]}.json"
                    return Moveset.build_from_file(file_path, loaded)
        name = None
        if 'moveset' in data and 'moves' in data:
            raise ValueError('Only one of moveset or moves can be in the data for a moveset')
        if 'moveset' in data:
            moveset = Moveset.build(data['moveset'], loaded)
            if 'min_distance' in data:
                moveset.min_distance = data['min_distance']
            if 'max_distance' in data:
                moveset.max_distance = data['max_distance']
            if 'mutator' in data:
                if type(data['mutator']) == dict:
                    if 'selector' in data['mutator']:
                        moveset.mutator = Selector().build(data['mutator'], loaded)
                    else:
                        moveset.mutator = Mutator.build(data['mutator'], loaded)
                else:
                    moveset.mutator = Mutator.build(data['mutator'], loaded)
            if 'color' in data:
                moveset.color = data['color']
            if 'condition' in data:
                moveset.condition = Condition.build(data['condition'], loaded)
            if 'category' in data:
                moveset.category = data['category']
            return moveset
        elif 'moves' in data:
            # if there is no target field for any of the moves, then we can just build the moves
            if all('target' not in move for move in data['moves']):
                moves = [{'target': Move.build(move), 'extra': []} for move in data['moves']]
            # if only some of the moves have a target field, this is invalid
            elif any('target' in move for move in data['moves']) and not all('target' in move for move in data['moves']):
                raise ValueError(f'{data["name"]}: Either all of the moves must be ["target": ..., "extra": ...] or none of them can be')
            # if all of the moves have a target field, then we need to build the moves and the extras
            else:
                moves = []
                for move in data['moves']:
                    try:
                        target = Move.build(move['target'])
                    except KeyError:
                        raise ValueError(f'{data["name"]}: Missing target field in move')
                    except TypeError:
                        raise TypeError(f'{data["name"]}: Invalid target field in move {move["target"]}')
                    extra = []
                    if 'extra' in move:
                        extra = [Move.build(extra_move) for extra_move in move['extra']]
                    moves.append({'target': target, 'extra': extra})
            
            min_distance = 1
            max_distance = -1
            mutator = Mutator(None, {}, {}, {}, {})
            color = 0x00FFFF88
            condition = Condition()
            category = 'move'
            if 'name' in data:
                name = data['name']
            if 'min_distance' in data:
                min_distance = data['min_distance']
            if 'max_distance' in data:
                max_distance = data['max_distance']
            if 'mutator' in data:
                if type(data['mutator']) == dict:
                    if 'selector' in data['mutator']:
                        mutator = Selector.build(data['mutator'], loaded, 'mutator')
                    else:
                        mutator = Mutator.build(data['mutator'], loaded)
                else:
                    mutator = Mutator.build(data['mutator'], loaded)
            if 'color' in data:
                color = data['color']
            if 'condition' in data:
                condition = Condition.build(data['condition'], loaded)
            if 'category' in data:
                category = data['category']
            return Moveset(name, moves, min_distance, max_distance, mutator, color, condition, category)
        else:
            raise ValueError('Invalid data for moveset')
    
    @staticmethod
    def build_from_file(file_path, loaded) -> 'Moveset':
        try:
            with open(file_path, 'r') as file:
                # make sure the file path has the right structure: ../{namespace}/data/movesets/{name}.json
                split_path = file_path.split('/')
                if split_path[-2] != 'movesets' or split_path[-3] != 'data' or split_path[-1].split('.')[-1] != 'json':
                    raise ValueError('Invalid file path for moveset')
                data = json.load(file)
                namespace = split_path[-4]
                name = split_path[-1].split('.')[0]

                moveset = Moveset.build(data, loaded)
                moveset.name = f'{namespace}:{name}'
                return moveset
        except FileNotFoundError:
            raise FileNotFoundError(f"[{file_path}] is missing")

    def __str__(self):
        string = f"{self.name}\n"
        string += "├ moves:\n"
        for move, i in zip(self.moves, range(len(self.moves))):
            move_string = str(move)
            if i != len(self.moves) - 1:
                move_string = move_string.replace("\n", "\n│ │")
                string += f"│ ├ {move_string}\n"
            else:
                move_string = move_string.replace("\n", "\n│  ")
                string += f"│ └ {move_string}\n"
        if self.min_distance != 1:
            string += f"├ min_distance: {self.min_distance}\n"
        if self.max_distance != -1:
            string += f"├ max_distance: {self.max_distance}\n"
        if self.mutator:
            mutator_string = str(self.mutator)
            mutator_string = mutator_string.replace("\n", "\n│")
            if mutator_string[:8] == "mutator:":
                mutator_string = mutator_string[8:]
            string += f"├ mutator: {mutator_string}\n"
        if self.condition:
            string += f"└ condition: {self.condition}"
        return string
    
    def __repr__(self):
        return self.__str__()

    
