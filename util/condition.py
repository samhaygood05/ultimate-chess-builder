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
from util import util

class Condition:
    
    TRUE = None
    FALSE = None


    def __init__(self, name = None, unbuilt_condition = True, condition = lambda board, source, target, extra, team: True) -> None:
        self.unbuilt_condition = unbuilt_condition
        self.condition = condition
        self.name = name

    @staticmethod
    def build(dictionary, loaded: dict, in_building=None) -> 'Condition':
        if type(dictionary) == str:
            if dictionary in loaded['conditions']:
                return loaded['conditions'][dictionary]
            else:
                seperated = dictionary.split(":")
                if len(seperated) == 2:

                    file_path = f"games/{seperated[0]}/data/conditions/{seperated[1]}.json"
                    if in_building != None:
                        if file_path in in_building:
                            raise Exception("Circular references are not allowed")
                    else:
                        in_building = []
                    return Condition.build_from_file(file_path, loaded, in_building.append(file_path))


        unbuilt_condition = dictionary
        condition = None
        if dictionary == True:
            condition = lambda board, source, target, extra, team: True
        elif dictionary == False:
            condition = lambda board, source, target, extra, team: False
        else:
            type1 = dictionary["type"]
            match type1:
                case "not":
                    unbuilt_condition['condition'] = Condition().build(dictionary["condition"], loaded).unbuilt_condition 
                    condition1 = Condition().build(dictionary["condition"], loaded).condition
                    condition = lambda board, source, target, extra, team: not condition1(board, source, target, extra, team)
                case "and":
                    unbuilt_condition['conditions'] = [Condition().build(condition, loaded).unbuilt_condition for condition in dictionary["conditions"]]
                    conditions = [Condition().build(condition, loaded).condition for condition in dictionary["conditions"]]
                    condition = lambda board, source, target, extra, team: all([condition(board, source, target, extra, team) for condition in conditions])
                case "or":
                    unbuilt_condition['conditions'] = [Condition().build(condition, loaded).unbuilt_condition for condition in dictionary["conditions"]]
                    conditions = [Condition().build(condition, loaded).condition for condition in dictionary["conditions"]]
                    condition = lambda board, source, target, extra, team: any([condition(board, source, target, extra, team) for condition in conditions])
                case "compare":
                    value1 = dictionary["value1"]
                    value2 = dictionary["value2"]
                    value1 = util.parse(value1, loaded)
                    value2 = util.parse(value2, loaded)
                    condition = lambda board, source, target, extra, team: value1(board, source, target, extra, team) == value2(board, source, target, extra, team)
                case "intersect":
                    # returns true if the intersection of the two lists is not empty
                    value1 = dictionary["value1"]
                    value2 = dictionary["value2"]
                    value1 = util.parse(value1, loaded)
                    value2 = util.parse(value2, loaded)
                    condition = lambda board, source, target, extra, team: bool(set(value1(board, source, target, extra, team)) & set(value2(board, source, target, extra, team)))
                case "contains":
                    value1 = dictionary["value1"]
                    value2 = dictionary["value2"]
                    value1 = util.parse(value1, loaded)
                    value2 = util.parse(value2, loaded)
                    condition = lambda board, source, target, extra, team: value1(board, source, target, extra, team) in value2(board, source, target, extra, team)
                case "subset":
                    value1 = dictionary["value1"]
                    value2 = dictionary["value2"]
                    value1 = util.parse(value1, loaded)
                    value2 = util.parse(value2, loaded)
                    condition = lambda board, source, target, extra, team: set(value1(board, source, target, extra, team)) <= set(value2(board, source, target, extra, team))
                case "exists":
                    value = dictionary["value"]
                    value = util.parse(value, loaded)
                    condition = lambda board, source, target, extra, team: value(board, source, target, extra, team) != None
        return Condition(None, unbuilt_condition, condition)                      

    @staticmethod
    def build_from_file(file_path, loaded: dict, in_building=None) -> 'Condition':
        try:
            with open(file_path, 'r') as file:
                # make sure the file path has the right structure: ../{namespace}/data/conditions/{name}.json
                split_path = file_path.split('/')
                if split_path[-2] != 'conditions' or split_path[-3] != 'data' or split_path[-1].split('.')[-1] != 'json':
                    raise ValueError(f'[{file_path}]: Invalid file path for condition')
                data = json.load(file)
                namespace = split_path[-4]
                name = split_path[-1].split('.')[0]

                condition = Condition.build(data, loaded, in_building)
                condition.name = f'{namespace}:{name}'
                return condition
        except FileNotFoundError:
            raise FileNotFoundError(f"[{file_path}] is missing")

    def evaluate(self, board, source, target, extra, team) -> bool:
        return self.condition(board, source, target, extra, team)
    
    def __str__(self) -> str:
        return str(self.unbuilt_condition)
    
    def __repr__(self) -> str:
        return str(self.unbuilt_condition)
    
Condition.TRUE = Condition('true', True, lambda board, source, target, extra, team: True)
Condition.FALSE = Condition('false', False, lambda board, source, target, extra, team: False)