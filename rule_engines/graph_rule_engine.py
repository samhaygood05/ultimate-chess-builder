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

import random
from graph_board import GraphBoard
from movement import RuleSet, RulePresets as rp
from typing import List, Dict, Any
from teams import Team, TeamPresets as tp
import copy


class GraphRuleEngine:
    def __init__(self, rulesets: Dict[str, RuleSet] = None, teams: Dict[str, Team] = None, promotion_tiles: Dict[str, Any] = None, turn_order: List[str] = None, multiteam_capture_ally = False, lose = None):
        self.rulesets = rp.STANDARD
        if rulesets != None:
            self.rulesets.update(rulesets)

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
            self.turn_order = list(self.teams.keys())
        else:
            self.turn_order = turn_order

        if lose == None:
            self.lose = {team: 'eliminate_royals' for team in self.teams.keys()}
        else:
            self.lose = lose

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
                if moveset.meets_requirements(board, position, piece.get_team_names(), self.teams):
                    moves, move_distance, can_move_empty, can_capture = moveset.get_moves(board, position, piece.get_team_names(), self.teams)

                    for move in moves:
                        new_position = position
                        new_facing = piece.facing
                        i = 0
                        while i in range(move_distance) or move_distance == -1:
                            i += 1
                            new_position, new_facing, last_movement = move.get_end_position(board, new_position, new_facing)
                            if new_position == None:
                                break
                            target = board.get_node_tile(new_position)
                            if target == None:
                                break
                            try:
                                disallowed_pieces = target.disallowed_pieces
                            except:
                                disallowed_pieces = []

                            if (new_position, new_facing, last_movement) in legal_moves:
                                break
                            if new_position in [move[0] for move in legal_moves]:
                                continue
                            if piece.name in disallowed_pieces:
                                break
                            if target.piece == None and can_move_empty:
                                legal_moves.append((new_position, new_facing, last_movement))
                            elif target.piece != None:
                                if can_capture and not target.piece.is_allies(allies, not multiteam_capture_ally):
                                    legal_moves.append((new_position, new_facing, last_movement))
                                break
        
        if legal_moves:
            pure_legal_moves = list(set([tuple(move[:2]) for move in legal_moves if None not in move]))
        else:
            pure_legal_moves = []

        return pure_legal_moves
    
    def get_legal_moves(self, position, board: GraphBoard, check=False):
        tile = board.get_node_tile(position)
        legal_moves = []

        if tile == None or tile.piece == None:
            return legal_moves
        
        name = tile.piece.name
        if name in self.rulesets.keys():
            legal_moves.extend(self.add_ruleset(position, board, self.rulesets[name]))

        return legal_moves
    
    def get_all_legal_moves(self, team, board: GraphBoard, check=False):
        legal_moves = []
        for position in board.get_team_pieces(team):
            legal_moves_pos = self.get_legal_moves(position, board, check)
            for move in legal_moves_pos:
                legal_moves.append((position, move[0]))
        return legal_moves

    def get_move_score(self, board: GraphBoard, start_pos, end_pos):
        scores = dict()
        for team in self.teams.keys():
            scores[team] = 0
        
        if start_pos == end_pos:
            return scores
        
        if board.get_node_piece(start_pos) != None:
            start_tile_point = self.rulesets[board.get_node_piece(start_pos).name].points
            start_tile_teams = board.get_piece_teams(start_pos)
        else:
            start_tile_point = 0
            start_tile_teams = []

        if board.get_node_piece(end_pos) != None:
            end_tile_point = self.rulesets[board.get_node_piece(end_pos).name].points
            end_tile_teams = board.get_piece_teams(end_pos)
        else:
            end_tile_point = 0
            end_tile_teams = []

        for team in end_tile_teams:
            scores[team] -= end_tile_point

        if board.get_node_piece(start_pos) != None:
            for team in start_tile_teams:
                if self.rulesets[board.get_node_piece(start_pos).name].promotion != None and end_pos in self.promotion_tiles[team]:
                    promotion_points = self.rulesets[self.rulesets[board.get_node_piece(start_pos).name].promotion].points
                    scores[team] += promotion_points - start_tile_point

        return scores

    def play_move(self, board: GraphBoard, start_pos, end_pos, illegal_moves=False, check=True) -> GraphBoard:
        if board.get_node_piece(start_pos) == None:
            print("Illegal Move")
            return board

        if not illegal_moves:
            legal_moves = self.get_legal_moves(start_pos, board, check)
            if end_pos not in [move[0] for move in legal_moves]:
                print("Illegal Move")
                return board
            new_facing = legal_moves[[move[0] for move in legal_moves].index(end_pos)][1]
        else:
            new_facing = None
        
        if self.turn_order[board.current_team_index] not in board.get_node_piece(start_pos).get_team_names():
            print("Not your turn")
            return board
        
        piece = board.get_node_piece(start_pos)
        piece_name = piece.name

        new_board = board.copy()
        new_board.set_node_piece(end_pos, piece.moved())
        new_board.set_node_piece(start_pos, None)


        promotion = self.rulesets[piece_name].promotion
        if new_facing != None:
            new_board.get_node_piece(end_pos).facing = new_facing

        if promotion != None:
            for team in piece.get_team_names():
                if end_pos in self.promotion_tiles[team]:
                    new_board.set_node_piece(end_pos, piece.promote(promotion))

        new_board.current_team_index = (new_board.current_team_index + 1) % len(self.turn_order)

        return new_board
    
    def ai_play(self, board: GraphBoard, ai_type = 'random', check=False, return_move_score=False):
        start_board = board
        new_board = board
        ai_start_pos, ai_end_pos = ((0, 0), (0, 0))
        team = self.turn_order[board.current_team_index]
        if ai_type == 'random':
            ai_legal_moves = self.get_all_legal_moves(team, board, check)
            if ai_legal_moves:
                ai_start_pos, ai_end_pos = random.choice(ai_legal_moves)
                new_board = self.play_move(board, ai_start_pos, ai_end_pos, check=check)
        elif ai_type[:6] == 'minmax':
            mode = ai_type.split('-')[0].split('_')[1:]
            if not len(mode):
                mode.append('')
            strength = int(ai_type.split('-')[1])
            try:
                opponent_strength = int(ai_type.split('-')[2])
            except:
                opponent_strength = 0
            opponent_strength = min(opponent_strength, strength - 1)
            opponent_strength = max(opponent_strength, 0)
            ai_legal_moves = self.get_all_legal_moves(team, board, check)
            max_scoring_move = None
            scores = []
            if strength == 0 and ai_legal_moves:
                for ai_start_pos, ai_end_pos in ai_legal_moves:
                    team_points = self.get_move_score(board, ai_start_pos, ai_end_pos)
                    maximize = 0
                    for t in team_points:
                        if t not in self.turn_order:
                            continue
                        elif t in self.teams[team].allies:
                            maximize += team_points[t]
                        else:
                            maximize -= team_points[t]
                    scores += [maximize]
                    if max_scoring_move == None:
                        max_scoring_move = maximize
                    else:
                        max_scoring_move = max(max_scoring_move, maximize)

                filtered_moves = [ai_legal_moves[i] for i in range(len(ai_legal_moves)) if scores[i] == max_scoring_move]
                if filtered_moves:
                    ai_start_pos, ai_end_pos = random.choice(filtered_moves)
                    new_board = self.play_move(board, ai_start_pos, ai_end_pos, check=check)
            
            elif ai_legal_moves:
                for ai_start_pos, ai_end_pos in ai_legal_moves:
                    skip_move = False
                    maximize = 0
                    accumulated_scores = self.get_move_score(new_board, ai_start_pos, ai_end_pos)
                    try:
                        if mode[1] == 'smart' and accumulated_scores[board.current_team] == -900:
                            scores += -99999
                            continue
                        elif mode[1] == 'smart' and -900 in accumulated_scores.values():
                            scores += 99999
                            continue
                    except:
                        pass
                    copy_board = self.play_move(board.copy(), ai_start_pos, ai_end_pos, check=check)
                    for i in range(strength):
                        copy_board, turn_score = self.ai_play(copy_board.copy(), f'{ai_type.split("-"[0])}-{opponent_strength}-{opponent_strength-1}', check, True)
                        try:
                            if mode[1] == 'smart' and turn_score[board.current_team] == -900:
                                skip_move = True
                                break
                        except:
                            pass
                        strength_factor = 1
                        try:
                            if mode[0] == 'sib': # Sooner is Better
                                strength_factor = max(0, min(1, 1/(1 + (i+1)//len(self.turn_order))))
                            elif mode[0] == 'lib': # Later is Better
                                strength_factor = max(0, min(1, 1 - 1/(1 + (i+1)//len(self.turn_order))))
                        except:
                            pass
                        for t in accumulated_scores:
                            accumulated_scores[t] += turn_score[t] * strength_factor
                    if skip_move:
                        scores += -99999
                        continue
                    for t in accumulated_scores:
                        if t not in self.turn_order:
                            continue
                        elif t in self.teams[team].allies:
                             maximize += accumulated_scores[t]
                        else:
                            maximize -= accumulated_scores[t]
                    scores += [maximize]
                    if max_scoring_move == None:
                        max_scoring_move = maximize
                    else:
                        max_scoring_move = max(maximize, max_scoring_move)
                    filtered_moves = [ai_legal_moves[i] for i in range(len(scores)) if scores[i] == max_scoring_move]
                if filtered_moves:
                    ai_start_pos, ai_end_pos = random.choice(filtered_moves)
                    new_board = self.play_move(board, ai_start_pos, ai_end_pos, check=check)

        if return_move_score:
            return new_board, self.get_move_score(start_board, ai_start_pos, ai_end_pos)
        return new_board