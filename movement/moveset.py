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

from movement import Move
from typing import Optional, List, Tuple, Any

class Moveset:
    def __init__(self, moves: List[Move], move_distance: int = -1, can_move_empty: bool = True, can_capture: bool = True, condition_requirement: str = 'lambda board, position, team, teams: True', condition_override: Optional[List[Tuple[str, 'Moveset']]] = None):
        self.moves = moves
        self.move_distance = move_distance
        self.can_move_empty = can_move_empty
        self.can_capture = can_capture
        self.condition_requirement = condition_requirement
        self.condition_override = condition_override

    def get_moves(self, board, tile, team, teams):
        if self.condition_override != None:
            for condition_str, moveset in self.condition_override:
                condition = eval(condition_str)
                if condition(board, tile, team, teams):
                    return moveset.moves, moveset.move_distance, moveset.can_move_empty, moveset.can_capture
        return self.moves, self.move_distance, self.can_move_empty, self.can_capture
    
    def add_condition(self, condition: str, moveset: 'Moveset'):
        if self.condition_override == None:
            self.condition_override = []
        self.condition_override.append((condition, moveset))
        return self
    
    def meets_requirements(self, board, position, team, teams):
        condition = eval(self.condition_requirement)
        return condition(board, position, team, teams)
    

class MovesetPresets:
    PAWN_DOUBLE_MOVE = Moveset([Move(('f', 'edge'))], 2, True, False)
    PAWN_MOVE = Moveset([Move(('f', 'edge'))], 1, True, False, condition_override=[('lambda board, position, team, teams: board.get_node_piece(position).has_moved == False', PAWN_DOUBLE_MOVE)])
    PAWN_CAPTURE = Moveset([Move(('fl', 'vertex')), Move(('fr', 'vertex'))], 1, False, True)
    ROOK = Moveset([Move(('f', 'edge')), Move(('b', 'edge')), Move(('l', 'edge')), Move(('r', 'edge'))])
    KNIGHT = Moveset([
        Move(('f', 'edge'), ('f', 'edge'), ('l', 'edge')),
        Move(('f', 'edge'), ('f', 'edge'), ('r', 'edge')),
        Move(('b', 'edge'), ('f', 'edge'), ('l', 'edge')),
        Move(('b', 'edge'), ('f', 'edge'), ('r', 'edge')),
        Move(('l', 'edge'), ('f', 'edge'), ('l', 'edge')),
        Move(('l', 'edge'), ('f', 'edge'), ('r', 'edge')),
        Move(('r', 'edge'), ('f', 'edge'), ('l', 'edge')),
        Move(('r', 'edge'), ('f', 'edge'), ('r', 'edge')),

        Move(('f', 'edge'), ('l', 'edge'), ('f', 'edge')),
        Move(('f', 'edge'), ('r', 'edge'), ('f', 'edge')),
        Move(('b', 'edge'), ('l', 'edge'), ('f', 'edge')),
        Move(('b', 'edge'), ('r', 'edge'), ('f', 'edge')),
        Move(('l', 'edge'), ('l', 'edge'), ('f', 'edge')),
        Move(('l', 'edge'), ('r', 'edge'), ('f', 'edge')),
        Move(('r', 'edge'), ('l', 'edge'), ('f', 'edge')),
        Move(('r', 'edge'), ('r', 'edge'), ('f', 'edge'))
        ], 1)
    BISHOP = Moveset([Move(('fl', 'vertex')), Move(('fr', 'vertex')), Move(('bl', 'vertex')), Move(('br', 'vertex'))])
    QUEEN = Moveset([
        Move(('f', 'edge')), Move(('b', 'edge')), Move(('l', 'edge')), Move(('r', 'edge')), 
        Move(('fl', 'vertex')), Move(('fr', 'vertex')), Move(('bl', 'vertex')), Move(('br', 'vertex'))])
    KING = Moveset([
        Move(('f', 'edge')), Move(('b', 'edge')), Move(('l', 'edge')), Move(('r', 'edge')), 
        Move(('fl', 'vertex')), Move(('fr', 'vertex')), Move(('bl', 'vertex')), Move(('br', 'vertex'))], 1)
    LONG_KNIGHT = Moveset([
        Move(('f', 'edge'), ('f', 'edge'), ('f', 'edge'), ('l', 'edge')),
        Move(('f', 'edge'), ('f', 'edge'), ('f', 'edge'), ('r', 'edge')),
        Move(('b', 'edge'), ('f', 'edge'), ('f', 'edge'), ('l', 'edge')),
        Move(('b', 'edge'), ('f', 'edge'), ('f', 'edge'), ('r', 'edge')),
        Move(('l', 'edge'), ('f', 'edge'), ('f', 'edge'), ('l', 'edge')),
        Move(('l', 'edge'), ('f', 'edge'), ('f', 'edge'), ('r', 'edge')),
        Move(('r', 'edge'), ('f', 'edge'), ('f', 'edge'), ('l', 'edge')),
        Move(('r', 'edge'), ('f', 'edge'), ('f', 'edge'), ('r', 'edge'))
        ], 1)
    

    PAWN_CAPTURE_GLINSKI = Moveset([Move(('fl', 'edge')), Move(('fr', 'edge'))], 1, False, True)
    ROOK_GLINSKI = Moveset([
        Move(('f', 'edge')),
        Move(('fr', 'edge')),
        Move(('br', 'edge')),
        Move(('b', 'edge')),
        Move(('bl', 'edge')),
        Move(('fl', 'edge'))
    ])
    KNIGHT_GLINSKI = Moveset([
        Move(('f', 'edge'), ('f', 'edge'), ('fl', 'edge')),
        Move(('f', 'edge'), ('f', 'edge'), ('fr', 'edge')),
        Move(('b', 'edge'), ('f', 'edge'), ('fl', 'edge')),
        Move(('b', 'edge'), ('f', 'edge'), ('fr', 'edge')),
        Move(('fl', 'edge'), ('f', 'edge'), ('fl', 'edge')),
        Move(('fl', 'edge'), ('f', 'edge'), ('fr', 'edge')),
        Move(('fr', 'edge'), ('f', 'edge'), ('fl', 'edge')),
        Move(('fr', 'edge'), ('f', 'edge'), ('fr', 'edge')),
        Move(('bl', 'edge'), ('f', 'edge'), ('fl', 'edge')),
        Move(('bl', 'edge'), ('f', 'edge'), ('fr', 'edge')),
        Move(('br', 'edge'), ('f', 'edge'), ('fl', 'edge')),
        Move(('br', 'edge'), ('f', 'edge'), ('fr', 'edge')),

        Move(('f', 'edge'), ('fl', 'edge'), ('f', 'edge')),
        Move(('f', 'edge'), ('fr', 'edge'), ('f', 'edge')),
        Move(('b', 'edge'), ('fl', 'edge'), ('f', 'edge')),
        Move(('b', 'edge'), ('fr', 'edge'), ('f', 'edge')),
        Move(('fl', 'edge'), ('fl', 'edge'), ('f', 'edge')),
        Move(('fl', 'edge'), ('fr', 'edge'), ('f', 'edge')),
        Move(('fr', 'edge'), ('fl', 'edge'), ('f', 'edge')),
        Move(('fr', 'edge'), ('fr', 'edge'), ('f', 'edge')),
        Move(('bl', 'edge'), ('fl', 'edge'), ('f', 'edge')),
        Move(('bl', 'edge'), ('fr', 'edge'), ('f', 'edge')),
        Move(('br', 'edge'), ('fl', 'edge'), ('f', 'edge')),
        Move(('br', 'edge'), ('fr', 'edge'), ('f', 'edge'))
    ], 1)
    BISHOP_GLINSKI = Moveset([
        Move(('ffr', 'vertex')),
        Move(('r', 'vertex')),
        Move(('bbr', 'vertex')),
        Move(('bbl', 'vertex')),
        Move(('l', 'vertex')),
        Move(('ffl', 'vertex'))
    ])
    QUEEN_GLINSKI = Moveset([
        Move(('f', 'edge')),
        Move(('fr', 'edge')),
        Move(('br', 'edge')),
        Move(('b', 'edge')),
        Move(('bl', 'edge')),
        Move(('fl', 'edge')),

        Move(('ffr', 'vertex')),
        Move(('r', 'vertex')),
        Move(('bbr', 'vertex')),
        Move(('bbl', 'vertex')),
        Move(('l', 'vertex')),
        Move(('ffl', 'vertex'))
    ])
    KING_GLINSKI = Moveset([
        Move(('f', 'edge')),
        Move(('fr', 'edge')),
        Move(('br', 'edge')),
        Move(('b', 'edge')),
        Move(('bl', 'edge')),
        Move(('fl', 'edge')),
        
        Move(('ffr', 'vertex')),
        Move(('r', 'vertex')),
        Move(('bbr', 'vertex')),
        Move(('bbl', 'vertex')),
        Move(('l', 'vertex')),
        Move(('ffl', 'vertex'))
    ], 1)

    WARP = Moveset([Move(('warp', 'warp'))], 1, True, False)

