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
    def __init__(self, name, moveset, captureset, first_move, first_move_boost, multimove, promotion=None, team_overrides=None):
        self.name = name
        self.moveset = moveset
        if captureset == None:
            self.captureset = moveset
        else:
            self.captureset = captureset
        self.first_move = first_move
        self.first_move_boost = first_move_boost
        self.multimove = multimove
        self.promotion = promotion
        self.team_overrides = team_overrides

    def rule_dict(*rulesets):
        dictionary: dict = {}
        for ruleset in rulesets:
            dictionary.update({ruleset.name: ruleset})
        return dictionary

    def reverse_captureset(self):
        inverse_captureset = [tuple(-x for x in move) for move in self.captureset]
        return inverse_captureset

    def __str__(self):
        return f"Name: {self.name}, Moveset: {self.moveset}, Captureset: {self.captureset}, First Move: {self.first_move} {self.first_move_boost}, Multimove: {self.multimove}, Promotion: {self.promotion}"

    def __repr__(self):
        return f"Name: {self.name}, Moveset: {self.moveset}, Captureset: {self.captureset}, First Move: {self.first_move} {self.first_move_boost}, Multimove: {self.multimove}, Promotion: {self.promotion}"