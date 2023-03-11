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
from team import Team
from rule_set import RuleSet
from rule_engine import RuleEngine
from board import Board



class Variants:

    WILDERBEAST = (Board(board_state=
        [[Tile('rook', Team.WHITE), Tile('knight', Team.WHITE), Tile('bishop', Team.WHITE), Tile('bishop', Team.WHITE), Tile('queen', Team.WHITE), Tile('king', Team.WHITE), Tile('dragon', Team.WHITE), Tile('long_knight', Team.WHITE), Tile('long_knight', Team.WHITE), Tile('knight', Team.WHITE), Tile('rook', Team.WHITE)],
        [Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE)],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK)],
        [Tile('rook', Team.BLACK), Tile('knight', Team.BLACK), Tile('long_knight', Team.BLACK), Tile('long_knight', Team.BLACK), Tile('dragon', Team.BLACK), Tile('king', Team.BLACK), Tile('queen', Team.BLACK), Tile('bishop', Team.BLACK), Tile('bishop', Team.BLACK), Tile('knight', Team.BLACK), Tile('rook', Team.BLACK)]]
    ),
    RuleEngine(RuleSet.rule_dict(
        RuleSet('long_knight', [(3, 1), (3, -1), (-3, 1), (-3, -1), (1, 3), (1, -3), (-1, 3), (-1, -3)], None, False, False, False),
        RuleSet('dragon', [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (3, 1), (3, -1), (-3, 1), (-3, -1), (1, 3), (1, -3), (-1, 3), (-1, -3)], None, False, False, False)
    )))

    MISC_FANTASY_RULESET = RuleSet.rule_dict(
        RuleSet('zebra', [(3, 2), (3, -2), (-3, 2), (-3, -2), (2, 3), (2, -3), (-2, 3), (-2, -3)], None, False, False, False),
        RuleSet('giraffe', [(4, 1), (4, -1), (-4, 1), (-4, -1), (1, 4), (1, -4), (-1, 4), (-1, -4)], None, False, False, False),
        RuleSet('unicorn', [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)], None, False, True, False)
    )

    CHESS12x12 = (Board(board_state=
        [[Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile('rook', Team.WHITE), Tile('knight', Team.WHITE), Tile('bishop', Team.WHITE), Tile('queen', Team.WHITE), Tile('king', Team.WHITE), Tile('bishop', Team.WHITE), Tile('knight', Team.WHITE), Tile('rook', Team.WHITE), Tile(), Tile()],
        [Tile(), Tile(), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile(), Tile()],
        [Tile(), Tile(), Tile('rook', Team.BLACK), Tile('knight', Team.BLACK), Tile('bishop', Team.BLACK), Tile('queen', Team.BLACK), Tile('king', Team.BLACK), Tile('bishop', Team.BLACK), Tile('knight', Team.BLACK), Tile('rook', Team.BLACK), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()]]
    ),
    RuleEngine(RuleSet.rule_dict(RuleSet('pawn', [(1, 0)], [(1, -1), (1, 1)], True, False, True, 'queen', 2))))

    DOUBLE_CHESS = (Board(board_state=
        [[Tile('rook', Team.WHITE), Tile('knight', Team.WHITE), Tile('bishop', Team.WHITE), Tile('queen', Team.WHITE), Tile('king', Team.WHITE), Tile('bishop', Team.WHITE), Tile('knight', Team.WHITE), Tile('rook', Team.WHITE), Tile('rook', Team.WHITE), Tile('knight', Team.WHITE), Tile('bishop', Team.WHITE), Tile('queen', Team.WHITE), Tile('king', Team.WHITE), Tile('bishop', Team.WHITE), Tile('knight', Team.WHITE), Tile('rook', Team.WHITE)],
        [Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE)],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
        [Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK)],
        [Tile('rook', Team.BLACK), Tile('knight', Team.BLACK), Tile('bishop', Team.BLACK), Tile('queen', Team.BLACK), Tile('king', Team.BLACK), Tile('bishop', Team.BLACK), Tile('knight', Team.BLACK), Tile('rook', Team.BLACK), Tile('rook', Team.BLACK), Tile('knight', Team.BLACK), Tile('bishop', Team.BLACK), Tile('queen', Team.BLACK), Tile('king', Team.BLACK), Tile('bishop', Team.BLACK), Tile('knight', Team.BLACK), Tile('rook', Team.BLACK)]]
    ), RuleEngine())