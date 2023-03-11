'''
Copyright 2023 Sam A. Haygood

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

class RuleSet:
    def __init__(self, name, moveset, captureset, first_move, multimove, directional, promotion=None, promotion_row=0):
        self.name = name
        self.moveset = moveset
        self.captureset = captureset
        self.first_move = first_move
        self.multimove = multimove
        self.directional = directional
        self.promotion = promotion
        self.promotion_row = promotion_row

    def rule_dict(*rulesets):
        dictionary: dict = {}
        for ruleset in rulesets:
            dictionary.update({ruleset.name: ruleset})
        return dictionary

    def __str__(self):
        return f"Name: {self.name}, Moveset: {self.moveset}, Captureset: {self.captureset}, First Move: {self.first_move}, Multimove: {self.multimove}, Directional: {self.directional}, Promotion: {self.promotion}, Promotion Row: {self.promotion_row}"

    def __repr__(self):
        return f"Name: {self.name}, Moveset: {self.moveset}, Captureset: {self.captureset}, First Move: {self.first_move}, Multimove: {self.multimove}, Directional: {self.directional}, Promotion: {self.promotion}, Promotion Row: {self.promotion_row}"