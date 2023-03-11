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
from team import Team
from tile import Tile
from rule_set import RuleSet
import pygame
import copy

class Board:
    def __init__(self, white_first=True, board_state=None, rulesets=None):
        if board_state == None:
            self.board = [[Tile('rook', Team.WHITE), Tile('knight', Team.WHITE), Tile('bishop', Team.WHITE), Tile('queen', Team.WHITE), Tile('king', Team.WHITE), Tile('bishop', Team.WHITE), Tile('knight', Team.WHITE), Tile('rook', Team.WHITE)],
                            [Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE)],
                            [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                            [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                            [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                            [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                            [Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK)],
                            [Tile('rook', Team.BLACK), Tile('knight', Team.BLACK), Tile('bishop', Team.BLACK), Tile('queen', Team.BLACK), Tile('king', Team.BLACK), Tile('bishop', Team.BLACK), Tile('knight', Team.BLACK), Tile('rook', Team.BLACK)]]
        else:
            self.board = board_state

        self.white_first = white_first
        self.rulesets = RuleSet.rule_dict(
            RuleSet('pawn', [(1, 0)], [(1, -1), (1, 1)], True, False, True, 'queen'),
            RuleSet('rook', [(0, 1), (0, -1), (1, 0), (-1, 0)], None, False, True, False),
            RuleSet('bishop', [(-1, -1), (-1, 1), (1, -1), (1, 1)], None, False, True, False),
            RuleSet('knight', [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)], None, False, False, False),
            RuleSet('queen', [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], None, False, True, False),
            RuleSet('king', [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], None, False, False, False)
        )
        if rulesets != None:
            self.rulesets.update(rulesets)

    def copy(self):
        copy_board = Board(copy.deepcopy(self.board), self.white_first, self.rulesets)
        return copy_board

    def tile_to_index(tile):
        column = tile[0]
        row = int(tile[1:])-1
        column_index = ord(column.lower()) - 97
        return row, column_index

    def index_to_tile(row, column):
        return chr(column + 97) + str(row+1)

    def get_tile(self, tile):
        row, column = Board.tile_to_index(tile)
        try:
            return self.board[row][column]
        except:
            print('Not a valid tile')
            return Tile()

    def __str__(self) -> str:
        return f"{self.board}"
