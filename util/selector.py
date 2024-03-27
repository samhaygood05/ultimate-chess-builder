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

from util.condition import Condition
from movement.mutator import Mutator
from util import util
import random

class Selector:
    def __init__(self, selector: str, values: list, default = None, loaded: dict = {}, expected_type = None):
        if selector == "random":
            for value in values:
                if not 'weight' in values:
                    raise ValueError('Weights must be provided for random selectors')
                elif type(value['weight']) != int and type(value['weight']) != float:
                    raise ValueError('Weights must be numbers')
        elif selector == "switch":
            for value in values:
                if 'condition' not in value:
                    raise ValueError('Conditions must be provided for switch selectors')
        self.selector = selector
        self.values = values
        self.default = default
        self.build_values(loaded, expected_type)

    @staticmethod
    def build(dictionary: dict, loaded: dict, expected_type = None) -> 'Selector':
        selector = dictionary['selector']
        default = None
        if selector == 'switch':
            values = []
            for value in dictionary['cases']:
                values.append({
                    'value': value['value'],
                    'condition': Condition.build(value['condition'], loaded)
                })
            default = dictionary['default']
        elif selector == 'random':
            values = []
            for value in dictionary['values']:
                values.append({
                    'value': value['value'],
                    'weight': value['weight']
                })
        return Selector(selector, values, default, loaded, expected_type)
    
    def build_values(self, loaded: dict, expected_type = None):
        if expected_type == 'mutator':
            for value in self.values:
                unbuilt = value['value']
                value['value'] = Mutator.build(unbuilt, loaded)
            if self.default != None:
                self.default = Mutator.build(self.default, loaded)

    def evaluate(self, board, source, target, extra, team, loaded):
        if self.selector == 'switch':
            for value in self.values:
                if value['condition'].evaluate(board, source, target, extra, team):
                    if type(value['value']) == Mutator:
                        return value['value'].evaluate(board, source, target, extra, team, loaded)
                    return util.parse(value['value'])(board, source, target, extra, team, loaded)
            if type(self.default) == Mutator:
                return self.default.evaluate(board, source, target, extra, team, loaded)
            return util.parse(self.default, loaded)(board, source, target, extra, team)
        elif self.selector == 'random':
            values = []
            weights = []
            for value in self.values:
                values.append(value['value'])
                weights.append(value['weight'])
            choice = random.choices(values, weights=weights)[0]
            if type(choice) == Mutator:
                return choice.evaluate(board, source, target, extra, team, loaded)
            return util.parse(choice, loaded)(board, source, target, extra, team, loaded)
        
    def __str__(self):
        string = f'{self.selector}\n'
        if self.default != None:
            if type(self.default) == Mutator:
                string += f' ├ default:\n'
                string += " │ └ " + self.default.__str__().replace('\n', '\n │  ') + '\n'
            else:
                string += f' ├ default: {self.default}\n'
        if self.selector == 'switch':
            string += ' └ cases:\n'
            # for each case, add a string representation of the condition and the value
            for value, i in zip(self.values, range(len(self.values))):
                if i == len(self.values) - 1:
                    value_string = value['value'].__str__().replace('\n', '\n      ')
                    string += f'   └ condition: {value["condition"].__str__()}:\n'
                    string += f'     └ {value_string}'
                else:
                    value_string = value['value'].__str__().replace('\n', '\n  │   ')
                    string += f'   ├ condition: {value["condition"].__str__()}:\n'
                    string += f'     ├ {value_string}\n'
        else:
            string += ' └ values:\n'
            for value, i in zip(self.values, range(len(self.values))):
                if i == len(self.values) - 1:
                    value_string = value['value'].__str__().replace('\n', '\n    ')
                    string += f'   └ {value_string}'
                else:
                    value_string = value['value'].__str__().replace('\n', '\n  │ ')
                    string += f'   ├ {value_string}\n'
        return string