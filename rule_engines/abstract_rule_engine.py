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

from abc import ABC, abstractmethod
from boards.abstract_board import AbstractBoard
from rule_set import RuleSet

class AbstractRuleEngine(ABC):
    @abstractmethod
    def add_ruleset(self, tile, board: AbstractBoard, ruleset: RuleSet):
        pass

    @abstractmethod
    def get_legal_moves(self, tile, board: AbstractBoard):
        pass

    @abstractmethod
    def is_in_check(self, team):
        pass

    @abstractmethod
    def play_move(self, board: AbstractBoard, start_tile, end_tile, illegal_moves=False):
        pass