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

from moveset import Moveset

class RuleSet:
    def __init__(self, name, points, movesets: Moveset, promotion=None):
        self.name = name
        self.points = points
        self.movesets = movesets
        self.promotion = promotion

    def rule_dict(*rulesets):
        dictionary: dict = {}
        for ruleset in rulesets:
            dictionary.update({ruleset.name: ruleset})
        return dictionary
