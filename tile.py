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
from piece import Piece

class TileType:
    def __init__(self, name, file_path, texture_path, properties=None, movesets=None, lazy_loaded=False):
        self.lazy_loaded = lazy_loaded
        self.name = name
        self.file_path = file_path
        self.texture_path = texture_path
        self.properties = properties
        self.movesets = movesets

    # we build the movesets seperately from the tile type because we need to pass in the tile types to the movesets
    def build_movesets(self, loaded: dict):
        if self.lazy_loaded:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                movesets = [Moveset.build(moveset, loaded) for moveset in data['movesets']]
                self.lazy_loaded = False
        return self
    
    @staticmethod
    def build(file_path):
        try:
            with open(file_path, 'r') as file:
                # make sure the file path has the right structure: ../{namespace}/tiles/{name}.json
                split_path = file_path.split('/')
                if split_path[-2] != 'tiles' or split_path[-3] != 'data' or split_path[-1].split('.')[-1] != 'json':
                    raise ValueError('Invalid file path for tile type')

                data = json.load(file)
                # use file_path to get the name of the tile type
                namespace = split_path[-4]
                name = split_path[-1].split('.')[0]
                texture = None
                lazy_loaded = False
                properties = []
                if 'texture' in data:
                    texture = data['texture']
                if 'properties' in data:
                    properties = data['properties']
                if 'movesets' in data and len(data['movesets']) > 0:
                    lazy_loaded = True
                return TileType(f'{namespace}:{name}', file_path, texture, properties, lazy_loaded=lazy_loaded)
        except FileNotFoundError:
            raise FileNotFoundError(f"[{file_path}] is missing")
        
    def __str__(self) -> str:
        string = f"{self.name}\n├ texture: {self.texture_path}\n├ properties:"
        if self.properties:
            string += "\n"
            for key, i in zip(self.properties, range(len(self.properties))):
                if i == len(self.properties) - 1:
                    string += f"│ └ {key}\n"
                else:
                    string += f"│ ├ {key}\n"
        else:
            string += " None\n"
        string += "└ movesets:"
        if self.movesets:
            string += "\n"
            for moveset, i in zip(self.movesets, range(len(self.movesets))):
                moveset_string = moveset.__str__()
                if i == len(self.moveset) - 1:
                    moveset_string = moveset_string.replace("\n", "\n   ")
                    string += f"  └ {moveset_string}"
                else:
                    moveset_string = moveset_string.replace("\n", "\n │ ")
                    moveset_string += f"  ├ {moveset_string}\n"
        else:
            string += " None"
        return string
        
class Tile:
    def __init__(self, types: list[str], piece: Piece = None, tile_types = {}, **properties):
        if type(types) == str:
            types = [types]
        self.types = types
        self.types_mutated = False
        self.piece = piece
        self.properties = {}

        if len(tile_types) == 0:
            self.properties = properties
        else:
            all_properties = {}

            # we need to get all the properties from the tile types
            for type1 in types:
                if type1 not in tile_types:
                    raise ValueError(f"[{type1}]: Invalid tile type")
                tile_type_properties = tile_types[type1].properties
                for key, value in tile_type_properties.items():
                    all_properties[key] = value
            
            for key, value in properties.items():
                if key in all_properties:
                    self.properties[key] = value
                else:
                    raise ValueError(f"[{key}]: Invalid property for tile type")
            for key, value in all_properties.items():
                if key not in properties:
                    self.properties[key] = value

    def update_properties(self, tile_types):
        if self.types_mutated:
            all_properties = {}

            for type1 in self.types:
                if type not in tile_types:
                    raise ValueError(f"[{type1}]: Invalid tile type")
                tile_type_properties = tile_types[type1].properties
                for key, value in tile_type_properties.items():
                    all_properties[key] = value
            
            for key in self.properties:
                if key not in all_properties:
                    del self.properties[key]

            for key, value in all_properties.items():
                if key not in self.properties:
                    self.properties[key] = value

    def __copy__(self):
        return Tile(self.types, self.piece.__copy__() if self.piece != None else None, {}, **self.properties.copy())
    
    def __str__(self) -> str:
        string = f"{self.types}\n"
        if self.piece != None:
            string += f"├ piece:\n"
            piece_string = str(self.piece)
            piece_string = piece_string.replace("\n", "\n│   ")
            string += f"│ └ {piece_string}\n"
        string += "└ properties:"
        if self.properties:
            string += "\n"
            for key, i in zip(self.properties, range(len(self.properties))):
                if i == len(self.properties) - 1:
                    string += f"  └ {key}: {self.properties[key]}\n"
                else:
                    string += f"  ├ {key}: {self.properties[key]}\n"
        else:
            string += " None\n"
        return string