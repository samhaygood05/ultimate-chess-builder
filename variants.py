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
from teams.team import Team
from teams.team import TeamPresets as tp
from rule_set import RuleSet
from rule_engines.square_rule_engine import SquareRuleEngine
from boards.square_board import SquareBoard
import pickle
import os

class Variants:
    def save(name, board_state, rule_engine):
        path = f"presets/{name}.chess"
        try:
            with open(path, 'xb') as f:
                pickle.dump((board_state, rule_engine), f)
        except:
            with open(path, 'wb') as f:
                pickle.dump((board_state, rule_engine), f)
        print('Preset Saved')

    def load(name):
        path = f"presets/{name}.chess"
        with open(path, 'rb') as f:
            preset = pickle.load(f)
        print(f'{name} Preset Loaded')
        return preset
    

    MISC_FANTASY_RULESET = RuleSet.rule_dict(
        RuleSet('zebra', [(3, 2), (3, -2), (-3, 2), (-3, -2), (2, 3), (2, -3), (-2, 3), (-2, -3)], None, False, 0, False),
        RuleSet('giraffe', [(4, 1), (4, -1), (-4, 1), (-4, -1), (1, 4), (1, -4), (-1, 4), (-1, -4)], None, False, 0, False),
        RuleSet('unicorn', [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)], None, False, 0, True)
    )

    def create_standard_board(team1, team2, distance):
        team1_area = [[Tile('rook', team1), Tile('knight', team1), Tile('bishop', team1), Tile('queen', team1), Tile('king', team1), Tile('bishop', team1), Tile('knight', team1), Tile('rook', team1)],
                    [Tile('pawn', team1), Tile('pawn', team1), Tile('pawn', team1), Tile('pawn', team1), Tile('pawn', team1), Tile('pawn', team1), Tile('pawn', team1), Tile('pawn', team1)]]
        
        team2_area = [[Tile('pawn', team2), Tile('pawn', team2), Tile('pawn', team2), Tile('pawn', team2), Tile('pawn', team2), Tile('pawn', team2), Tile('pawn', team2), Tile('pawn', team2)],
                    [Tile('rook', team2), Tile('knight', team2), Tile('bishop', team2), Tile('queen', team2), Tile('king', team2), Tile('bishop', team2), Tile('knight', team2), Tile('rook', team2)]]

        empty_area = [[Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()]] * distance
        return team1_area + empty_area + team2_area
