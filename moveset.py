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

from boards import StandardBoard
from typing import Optional, List, Tuple, Callable, Any

class Moveset:
    def __init__(self, moves, move_distance: int = -1, first_move_boost: int = -1, can_move_empty: bool = True, can_capture: bool = True, condition_override: Optional[List[Tuple[Callable[[StandardBoard, str, str, List[Any]], bool], Any]]] = None):
        self.moves = moves
        self.move_distance = move_distance
        self.first_move_boost = first_move_boost
        self.can_move_empty = can_move_empty
        self.can_capture = can_capture
        self.condition_override = condition_override

    def get_moves(self, board: StandardBoard, tile: str, team: str, teams):
        if self.condition_override != None:
            for condition, moveset in self.condition_override:
                if condition(board, tile, team, teams):
                    return moveset.moves, moveset.move_distance, moveset.first_move_boost, moveset.can_move_empty, moveset.can_capture
        return self.moves, self.move_distance, self.first_move_boost, self.can_move_empty, self.can_capture

class MovesetPresets:
    PAWN_MOVE = Moveset([(1, 0)], 1, 2, True, False)
    PAWN_CAPTURE = Moveset([(1, -1), (1, 1)], 1, 0, False, True)
    ROOK = Moveset([(0, 1), (0, -1), (1, 0), (-1, 0)])
    BISHOP = Moveset([(-1, -1), (-1, 1), (1, -1), (1, 1)])
    KNIGHT = Moveset([(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)], 1, 0, True, True)
    QUEEN = Moveset([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
    KING = Moveset([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], 1)
    LONG_KNIGHT = Moveset([(3, 1), (3, -1), (-3, 1), (-3, -1), (1, 3), (1, -3), (-1, 3), (-1, -3)], 1, 0, True, True)