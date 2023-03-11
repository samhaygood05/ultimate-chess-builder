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

from tile import Tile
from team import TeamPresets as tp
import copy

class Board:
    def __init__(self, current_team='white', board_state=None):
        if board_state == None:
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
