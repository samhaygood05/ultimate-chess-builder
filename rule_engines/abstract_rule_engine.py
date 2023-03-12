from abc import ABC, abstractmethod

class AbstractRuleEngine(ABC):
    @abstractmethod
    def add_ruleset(self, tile, board, ruleset):
        pass

    @abstractmethod
    def get_legal_moves(self, tile, board):
        pass

    @abstractmethod
    def is_in_check(self, team):
        pass

    @abstractmethod
    def play_move(self, board, start_tile, end_tile, illegal_moves=False):
        pass