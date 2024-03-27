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

class Function:
    def __init__(self, name, unbuilt_function, function):
        self.name = name
        self.unbuilt_function = unbuilt_function
        self.function = function

    @staticmethod
    def build(dictionary, piece_types, tile_types, conditions, functions, in_building=None):
        if type(dictionary) == str:
            if dictionary in functions:
                return functions[dictionary]
            else:
                seperated = dictionary.split(":")
                if len(seperated) == 2:
                    file_path = f"games/{seperated[0]}/data/functions/{seperated[1]}.json"
                    if in_building != None:
                        if file_path in in_building:
                            raise Exception("Circular references are not allowed")
                    else:
                        in_building = []
                    return Function.build_from_file(file_path, piece_types, tile_types, conditions, functions, in_building.append(file_path))
        else:
            name = None
            if 'name' in dictionary:
                name = dictionary['name']
            if 'function' in dictionary:
                function = dictionary['function']
                if function == "sum":
                    values = dictionary['values']
                    
        
