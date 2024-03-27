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
from movement.moveset import Moveset

class PieceType:
    def __init__(self, name, file_path, texture_paths: dict, value, movesets, is_royal=False, properties={}, instance_properties={}, lazy_loaded=False):
        self.lazy_loaded = lazy_loaded
        self.name = name
        self.file_path = file_path
        self.texture_paths = texture_paths
        self.value = value
        self.movesets = movesets
        self.is_royal = is_royal
        self.properties = properties
        self.instance_properties = instance_properties

    # we build the moveset seperately from the piece type because we need to pass in the piece types to the moveset
    def build_movesets(self, loaded):
        if self.lazy_loaded:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                movesets = [Moveset.build(moveset, loaded) for moveset in data['movesets']]
                self.movesets = movesets
                self.lazy_loaded = False
        return self

    @staticmethod
    def build(file_path):
        try:
            with open(file_path, 'r') as file:
                # make sure the file path has the right structure: ../{namespace}/data/pieces/{name}.json
                split_path = file_path.split('/')
                if split_path[-2] != 'pieces' or split_path[-3] != 'data' or split_path[-1].split('.')[-1] != 'json':
                    raise ValueError(f'[{file_path}]: Invalid file path for piece type')

                data = json.load(file)
                # use file_path to get the name of the tile type
                namespace = split_path[-4]
                name = split_path[-1].split('.')[0]
                is_royal = False
                properties = {}
                instance_properties = {}
                if 'is_royal' in data:
                    is_royal = data['is_royal']
                if 'properties' in data:
                    properties = data['properties']
                if 'instance_properties' in data:
                    instance_properties = data['instance_properties']
                return PieceType(f'{namespace}:{name}', file_path, data['textures'], value=data['value'], movesets=None, is_royal=is_royal, properties=properties, instance_properties=instance_properties, lazy_loaded=True)
        except FileNotFoundError:
            raise FileNotFoundError(f"[{file_path}] is missing")
        
    def __str__(self):
        string = f"{self.name}\n├ textures:"
        for key, i in zip(self.texture_paths, range(len(self.texture_paths))):
            if i != len(self.texture_paths) - 1:
                string += f"\n│ ├ {key}: {self.texture_paths[key]}"
            else:
                string += f"\n│ └ {key}: {self.texture_paths[key]}"
        string += "\n├ value: {self.value}\n├ royal: {self.is_royal}\n├ properties: \n"
        for key, value, i in zip(self.properties.keys(), self.properties.values(), range(len(self.properties))):
            if i != len(self.properties) - 1:
                string += f"│ ├ {key}: {value}\n"
            else:
                string += f"│ └ {key}: {value}\n"
        string += "└ movesets:\n"
        for moveset, i in zip(self.movesets, range(len(self.movesets))):
            moveset_string = str(moveset)
            if i != len(self.movesets) - 1:
                moveset_string = moveset_string.replace("\n", "\n  │ ")
                string += f"  ├ {moveset_string}\n"
            else:
                moveset_string = moveset_string.replace("\n", "\n    ")
                string += f"  └ {moveset_string}"
        return string
    
    def __repr__(self):
        return self.__str__()



class Piece:
    def __init__(self, piece_type, teams, facing='n', has_moved=False, piece_types={}, **properties):
        self.piece_type = piece_type
        self.type_mutated = False
        self.facing = facing
        self.has_moved = has_moved
        self.teams = teams
        self.properties = {}

        if len(piece_types) == 0:
            self.properties = properties
        else:
            piece_properties = piece_types[piece_type].instance_properties
            for key, value in properties.items():
                if key in piece_properties:
                    self.properties[key] = value
                else:
                    raise ValueError(f"[{key}]: Invalid property for piece type")
                
            for key in piece_properties:
                if key not in properties:
                    self.properties[key] = piece_properties[key]

    def move(self):
        self.has_moved = True
        return self
    
    def update_properties(self, piece_types):
        if self.type_mutated:
            piece_properties = piece_types[self.piece_type].instance_properties
            for key in self.properties:
                if key not in piece_properties:
                    del self.properties[key]

            for key, value in piece_properties.items():
                if key not in self.properties:
                    self.properties[key] = value

    def __copy__(self):
        return Piece(self.piece_type, self.teams, self.facing, self.has_moved, **self.properties.copy())

    def __str__(self):
        string = f"{self.piece_type}\n├ facing: {self.facing}\n├ has moved: {self.has_moved}\n├ teams: {self.teams}\n└ properties:\n"
        for key, value, i in zip(self.properties.keys(), self.properties.values(), range(len(self.properties))):
            if i != len(self.properties) - 1:
                string += f"  ├ {key}: {value}\n"
            else:
                string += f"  └ {key}: {value}"
        return string