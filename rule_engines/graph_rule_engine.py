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

from graph_board import GraphBoard
from movement import RuleSet, RulePresets as rp
from typing import List, Dict, Any
from teams import Team, TeamPresets as tp
import copy


class GraphRuleEngine:
    def __init__(self, rulesets: Dict[str, RuleSet] = None, teams: Dict[str, Team] = None, promotion_tiles: Dict[str, Any] = None, turn_order: List[str] = None, multiteam_capture_ally = False):
        if rulesets == None:
            self.rulesets = rp.STANDARD
        else:
            self.rulesets = rulesets

        if teams == None:
            self.teams = Team.team_dict(tp.WHITE, tp.BLACK)
        else:
            self.teams = teams

        if promotion_tiles == None:
            self.promotion_tiles = {
                'white': [(7, i) for i in range(8)],
                'black': [(0, i) for i in range(8)]
            }
        else:
            self.promotion_tiles = promotion_tiles

        if turn_order == None:
            self.turn_order = ['white', 'black']
        else:
            self.turn_order = turn_order

        self.multiteam_capture_ally = multiteam_capture_ally

    def copy(self):
        return GraphRuleEngine(self.rulesets, self.teams, self.promotion_tiles, copy.copy(self.turn_order), self.multiteam_capture_ally)
    
    def add_ruleset(self, position, board: GraphBoard, ruleset: RuleSet):
        tile = board.get_node_tile(position)
        if tile == None or tile.piece == None:
            return []
        piece = tile.piece

        team = self.teams[piece.team]
        if piece.has_moved and self.multiteam_capture_ally:
            allies = piece.get_allies_intersection(self.teams)
            multiteam_capture_ally = True
        else:
            allies = piece.get_allies_union(self.teams)
            multiteam_capture_ally = False

        piece_name = ruleset.name
        legal_moves = []

        if piece.name == piece_name:
            for moveset in ruleset.movesets:
                if moveset.meets_requirements(board, position, team, self.teams):
                    moves, move_distance, can_move_empty, can_capture = moveset.get_moves(board, position, team, self.teams)

                    for move in moves:
                        new_position = position
                        new_facing = piece.facing
                        i = 0
                        while i in range(move_distance) or move_distance == -1:
                            i += 1
                            new_position, new_facing = move.get_end_position(board, new_position, new_facing)
                            if new_position == None:
                                break
                            target = board.get_node_tile(new_position)
                            if target == None:
                                break
                            try:
                                disallowed_pieces = target.disallowed_pieces
                            except:
                                disallowed_pieces = []

                            if piece.name in disallowed_pieces:
                                break
                            if target.piece == None and can_move_empty:
                                legal_moves.append(new_position)
                            elif target.piece != None:
                                if can_capture and not target.piece.is_allies(allies, not multiteam_capture_ally):
                                    legal_moves.append(new_position)
                                break

        return legal_moves
    
    def get_legal_moves(self, position, board: GraphBoard, check=False):
        tile = board.get_node_tile(position)
        legal_moves = []

        if tile == None or tile.piece == None:
            return legal_moves
        
        legal_moves.extend(self.add_ruleset(position, board, self.rulesets[tile.piece.name]))

        return legal_moves
    
    def get_all_legal_moves(self, team, board: GraphBoard, check=False):
        legal_moves = []
        for position in board.nodes.keys():
            if board.get_node_piece(position) != None and team in board.get_node_piece(position).get_team_names():
                legal_moves.extend(self.get_legal_moves(position, board, check))

        return legal_moves

    def play_move(self, board: GraphBoard, start_pos, end_pos, illegal_moves=False, check=True) -> GraphBoard:
        if not illegal_moves:
            legal_moves = self.get_legal_moves(start_pos, board, check)
            if end_pos not in legal_moves:
                print("Illegal Move")
                return board
        
        if self.turn_order[board.current_team_index] not in board.get_node_piece(start_pos).get_team_names():
            print("Not your turn")
            return board
        
        piece = board.get_node_piece(start_pos)

        royal_tiles = board.royal_tiles
        if piece.is_royal:
            for team in piece.get_team_names():
                royal_tiles[team].remove(start_pos)
                royal_tiles[team].append(end_pos)

        new_board = board.copy()
        new_board.set_node_piece(end_pos, piece)
        new_board.set_node_piece(start_pos, None)

        promotion = self.rulesets[piece.name].promotion

        for team in piece.get_team_names():
            if end_pos in self.promotion_tiles[team]:
                new_board.set_node_piece(end_pos, piece.promote(promotion))

        new_board.current_team_index = (new_board.current_team_index + 1) % len(self.turn_order)

        return new_board