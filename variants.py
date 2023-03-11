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

from render_engine import RenderEngine
from tile import Tile
from team import Team
from team import TeamPresets as tp
from rule_set import RuleSet
from rule_engine import RuleEngine
from board import Board

class Variants:

    WILDERBEAST = (Board(board_state=
        [[Tile('rook', tp.WHITE), Tile('knight', tp.WHITE), Tile('bishop', tp.WHITE), Tile('bishop', tp.WHITE), Tile('queen', tp.WHITE), Tile('king', tp.WHITE), Tile('dragon', tp.WHITE), Tile('long_knight', tp.WHITE), Tile('long_knight', tp.WHITE), Tile('knight', tp.WHITE), Tile('rook', tp.WHITE)],
        [Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE)],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK)],
        [Tile('rook', tp.BLACK), Tile('knight', tp.BLACK), Tile('long_knight', tp.BLACK), Tile('long_knight', tp.BLACK), Tile('dragon', tp.BLACK), Tile('king', tp.BLACK), Tile('queen', tp.BLACK), Tile('bishop', tp.BLACK), Tile('bishop', tp.BLACK), Tile('knight', tp.BLACK), Tile('rook', tp.BLACK)]]
    ),
    RuleEngine(RuleSet.rule_dict(
        RuleSet('pawn', [(1, 0)], [(1, -1), (1, 1)], True, 3, False, 'queen'),
        RuleSet('long_knight', [(3, 1), (3, -1), (-3, 1), (-3, -1), (1, 3), (1, -3), (-1, 3), (-1, -3)], None, False, 0, False),
        RuleSet('dragon', [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (3, 1), (3, -1), (-3, 1), (-3, -1), (1, 3), (1, -3), (-1, 3), (-1, -3)], None, False, 0, False)
    ), promotion_tiles={
        'white': ['a10', 'b10', 'c10', 'd10', 'e10', 'f10', 'g10', 'h10', 'i10', 'j10', 'k10'],
        'black': ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'i1', 'j1', 'k1']
    }))

    MISC_FANTASY_RULESET = RuleSet.rule_dict(
        RuleSet('zebra', [(3, 2), (3, -2), (-3, 2), (-3, -2), (2, 3), (2, -3), (-2, 3), (-2, -3)], None, False, 0, False),
        RuleSet('giraffe', [(4, 1), (4, -1), (-4, 1), (-4, -1), (1, 4), (1, -4), (-1, 4), (-1, -4)], None, False, 0, False),
        RuleSet('unicorn', [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)], None, False, 0, True)
    )

    CHESS12x12 = (Board(board_state=
        [[Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile('rook', tp.WHITE), Tile('knight', tp.WHITE), Tile('bishop', tp.WHITE), Tile('queen', tp.WHITE), Tile('king', tp.WHITE), Tile('bishop', tp.WHITE), Tile('knight', tp.WHITE), Tile('rook', tp.WHITE), Tile(), Tile()],
        [Tile(), Tile(), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile(), Tile()],
        [Tile(), Tile(), Tile('rook', tp.BLACK), Tile('knight', tp.BLACK), Tile('bishop', tp.BLACK), Tile('queen', tp.BLACK), Tile('king', tp.BLACK), Tile('bishop', tp.BLACK), Tile('knight', tp.BLACK), Tile('rook', tp.BLACK), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()]]
    ),
    RuleEngine(RuleSet.rule_dict(RuleSet('pawn', [(1, 0)], [(1, -1), (1, 1)], True, 2, False, 'queen')),
    promotion_tiles= {
        'white': ['a10', 'b10', 'c10', 'd10', 'e10', 'f10', 'g10', 'h10', 'i10', 'j10', 'k10'],
        'black': ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 'i3', 'j3', 'k3']
    }), 
    )

    DOUBLE_CHESS = (Board(board_state=
        [[Tile('rook', tp.WHITE), Tile('knight', tp.WHITE), Tile('bishop', tp.WHITE), Tile('queen', tp.WHITE), Tile('king', tp.WHITE), Tile('bishop', tp.WHITE), Tile('knight', tp.WHITE), Tile('rook', tp.WHITE), Tile('rook', tp.WHITE), Tile('knight', tp.WHITE), Tile('bishop', tp.WHITE), Tile('queen', tp.WHITE), Tile('king', tp.WHITE), Tile('bishop', tp.WHITE), Tile('knight', tp.WHITE), Tile('rook', tp.WHITE)],
        [Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE)],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK)],
        [Tile('rook', tp.BLACK), Tile('knight', tp.BLACK), Tile('bishop', tp.BLACK), Tile('queen', tp.BLACK), Tile('king', tp.BLACK), Tile('bishop', tp.BLACK), Tile('knight', tp.BLACK), Tile('rook', tp.BLACK), Tile('rook', tp.BLACK), Tile('knight', tp.BLACK), Tile('bishop', tp.BLACK), Tile('queen', tp.BLACK), Tile('king', tp.BLACK), Tile('bishop', tp.BLACK), Tile('knight', tp.BLACK), Tile('rook', tp.BLACK)]]
    ), RuleEngine(RuleSet.rule_dict(RuleSet('pawn', [(1, 0)], [(1, -1), (1, 1)], True, 4, False, 'queen'))))

    WHITE_SIDE = Team('white', (0, 1))

    L_CHESS = (Board(board_state=
        [[Tile('rook', WHITE_SIDE), Tile('pawn', WHITE_SIDE), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile('knight', WHITE_SIDE), Tile('pawn', WHITE_SIDE), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile('bishop', WHITE_SIDE), Tile('pawn', WHITE_SIDE), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile('king', WHITE_SIDE), Tile('pawn', WHITE_SIDE), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile('queen', WHITE_SIDE), Tile('pawn', WHITE_SIDE), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile('bishop', WHITE_SIDE), Tile('pawn', WHITE_SIDE), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile('knight', WHITE_SIDE), Tile('pawn', WHITE_SIDE), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile('rook', WHITE_SIDE), Tile('pawn', WHITE_SIDE), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [None, None, None, None, None, None, None, None, Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [None, None, None, None, None, None, None, None, Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [None, None, None, None, None, None, None, None, Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [None, None, None, None, None, None, None, None, Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [None, None, None, None, None, None, None, None, Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [None, None, None, None, None, None, None, None, Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [None, None, None, None, None, None, None, None, Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK)],
        [None, None, None, None, None, None, None, None, Tile('rook', tp.BLACK), Tile('knight', tp.BLACK), Tile('bishop', tp.BLACK), Tile('queen', tp.BLACK), Tile('king', tp.BLACK), Tile('bishop', tp.BLACK), Tile('knight', tp.BLACK), Tile('rook', tp.BLACK)]]
    ),
    RuleEngine(rulesets=RuleSet.rule_dict(
        RuleSet('pawn', [(1, 0)], [(1, -1), (1, 1)], True, 6, False, 'queen')
    ),
    promotion_tiles={
        'white': ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p16'],
        'black': ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'i1', 'j1', 'k1', 'l1', 'm1', 'n1', 'o1', 'p1']
    }))
