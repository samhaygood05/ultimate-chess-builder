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

from boards.abstract_board import AbstractBoard
from tile import Tile
from teams.team import TeamPresets as tp
import copy

class StandardBoard(AbstractBoard):
    def __init__(self, current_team='white', board_state=None, royal_tiles=None, hexagonal=False):
        if board_state == None:
            if hexagonal:
                self.board = [
                [None, None, None, None, None, Tile(), Tile('pawn', tp.WHITE), Tile('rook', tp.WHITE), Tile('knight', tp.WHITE), Tile('king', tp.WHITE), Tile('bishop', tp.WHITE)],
                [None, None, None, None, Tile(), Tile(), Tile('pawn', tp.WHITE), Tile(), Tile(), Tile('bishop', tp.WHITE), Tile('queen', tp.WHITE)],
                [None, None, None, Tile(), Tile(), Tile(), Tile('pawn', tp.WHITE), Tile(), Tile('bishop', tp.WHITE), Tile(), Tile('knight', tp.WHITE)],
                [None, None, Tile(), Tile(), Tile(), Tile(), Tile('pawn', tp.WHITE), Tile(), Tile(), Tile(), Tile('rook', tp.WHITE)],
                [None, Tile(), Tile(), Tile(), Tile(), Tile(), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE)],
                [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                [Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile(), Tile(), Tile(), Tile(), Tile(), None],
                [Tile('rook', tp.BLACK), Tile(), Tile(), Tile(), Tile('pawn', tp.BLACK), Tile(), Tile(), Tile(), Tile(), None, None],
                [Tile('knight', tp.BLACK), Tile(), Tile('bishop', tp.BLACK), Tile(), Tile('pawn', tp.BLACK), Tile(), Tile(), Tile(), None, None, None],
                [Tile('king', tp.BLACK), Tile('bishop', tp.BLACK), Tile(), Tile(), Tile('pawn', tp.BLACK), Tile(), Tile(), None, None, None, None],
                [Tile('bishop', tp.BLACK), Tile('queen', tp.BLACK), Tile('knight', tp.BLACK), Tile('rook', tp.BLACK), Tile('pawn', tp.BLACK), Tile(), None, None, None, None, None]
            ]
            else:
                self.board = [[Tile('rook', tp.WHITE), Tile('knight', tp.WHITE), Tile('bishop', tp.WHITE), Tile('queen', tp.WHITE), Tile('king', tp.WHITE), Tile('bishop', tp.WHITE), Tile('knight', tp.WHITE), Tile('rook', tp.WHITE)],
                                [Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE)],
                                [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                                [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                                [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                                [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                                [Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK)],
                                [Tile('rook', tp.BLACK), Tile('knight', tp.BLACK), Tile('bishop', tp.BLACK), Tile('queen', tp.BLACK), Tile('king', tp.BLACK), Tile('bishop', tp.BLACK), Tile('knight', tp.BLACK), Tile('rook', tp.BLACK)]]
        else:
            self.board = board_state

        self.current_team = current_team

        if royal_tiles == None:
            self.royal_tiles = []
            for row in range(len(self.board)):
                for col in range(len(self.board[0])):
                    if self.board[row][col] != None:
                        if self.board[row][col].is_royal:
                            self.royal_tiles.append(StandardBoard.index_to_tile(row, col))
        else:
            self.royal_tiles = royal_tiles

    def copy(self):
        copy_board = StandardBoard(self.current_team, copy.deepcopy(self.board))
        return copy_board

    def get_tile(self, tile):
        row, column = StandardBoard.tile_to_index(tile)
        try:
            return self.board[row][column]
        except:
            print('Not a valid tile')
            return Tile()

    def __str__(self) -> str:
        return f"{self.board}"
