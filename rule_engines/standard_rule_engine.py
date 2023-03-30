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

from unittest import skip
from rule_set import RuleSet
from boards import StandardBoard
from rule_engines import AbstractRuleEngine
from teams import Team
from teams import TeamPresets as tp
from moveset import Moveset, MovesetPresets as mp
import random
import copy

class StandardRuleEngine(AbstractRuleEngine):
    def __init__(self, rulesets: dict = None, teams = None, promotion_tiles = None, turn_order = None, multiteam_capture_ally = False, hexagonal=False):
        if hexagonal:
            self.rulesets = RuleSet.rule_dict(
            RuleSet('pawn', 10, [Moveset([(1, 1)], 1, 2, True, False), Moveset([(0, 1), (1, 0)], 1, 0, False, True)], 'queen'),
            RuleSet('rook', 50, [Moveset([(1,0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)])]),
            RuleSet('bishop', 30, [Moveset([(2, 1), (1, 2), (-1, 1), (1, -1), (-2, -1), (-1, -2)])]),
            RuleSet('knight', 30, [Moveset([(1, 3), (2, 3), (3, 2), (3, 1), (2, -1), (1, -2), (-1, -3), (-2, -3), (-3, -2), (-3, -1), (-2, 1), (-1, 2)], 1)]),
            RuleSet('queen', 90, [Moveset([(1, -1), (-1, 1), (1,0), (-1, 0), (0, 1), (0, -1), (2, 1), (1, 2), (1, 1), (-1, -1), (-2, -1), (-1, -2)])]),
            RuleSet('king', 900, [Moveset([(1, -1), (-1, 1), (1,0), (-1, 0), (0, 1), (0, -1), (2, 1), (1, 2), (1, 1), (-1, -1), (-2, -1), (-1, -2)], 1)])
        )
        else:
            self.rulesets = RuleSet.rule_dict(
                RuleSet('pawn', 10, [mp.PAWN_MOVE, mp.PAWN_CAPTURE], 'queen'),
                RuleSet('rook', 50, [mp.ROOK]),
                RuleSet('bishop', 30, [mp.BISHOP]),
                RuleSet('knight', 30, [mp.KNIGHT]),
                RuleSet('queen', 90, [mp.QUEEN]),
                RuleSet('king', 900, [mp.KING])
            )
        if rulesets != None:
            self.rulesets.update(rulesets)
        if teams == None:
            self.teams = Team.team_dict(tp.WHITE, tp.BLACK)
        else:
            self.teams = teams
        if promotion_tiles == None:
            if hexagonal:
                self.promotion_tiles = {
                    'white': ['a6', 'a7', 'a8', 'a9', 'a10', 'a11', 'b11', 'c11', 'd11', 'e11', 'f11'],
                    'black': ['f1', 'g1', 'h1', 'i1', 'j1', 'k1', 'k2', 'k3', 'k4', 'k5', 'k6']
                }
            else:
                self.promotion_tiles = {
                    'white': ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
                    'black': ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
                }
        else:
            self.promotion_tiles = promotion_tiles
        if turn_order == None:
            self.turn_order = list(self.teams.keys())
        else:
            self.turn_order = turn_order
        
        self.multiteam_capture_ally = multiteam_capture_ally

    def copy(self):
        copy_engine = StandardRuleEngine(self.rulesets, self.teams, self.promotion_tiles, copy.copy(self.turn_order), self.multiteam_capture_ally)
        return copy_engine

    def add_ruleset(self, tile, board: StandardBoard, ruleset: RuleSet):
        piece = board.get_tile(tile).piece

        if piece == None:
            return []

        team = piece.team.name
        if piece.has_moved and self.multiteam_capture_ally:
            allies = piece.get_allies_intersection()
            multiteam_capture_ally = True
        else:
            allies = piece.get_allies_union()
            multiteam_capture_ally = False

        piece_name = ruleset.name

        row, col = StandardBoard.tile_to_index(tile)
        legal_moves = []
        direction = self.teams[team].direction
        side_direction = self.teams[team].perpendicular

        if piece.name == piece_name:
            for moveset in ruleset.movesets:
                moves, move_distance, first_move_boost, can_move_empty, can_capture = moveset.get_moves(board, tile, team, self.teams)

                # Logic for Moveset
                for delta_forward, delta_right in moves:
                    delta = (delta_forward*direction[0] + delta_right*side_direction[0], delta_forward*direction[1] + delta_right*side_direction[1])

                    new_row = row + delta[0]
                    new_col = col + delta[1]
                    steps = 0
                    while (new_row in range(len(board.board))) and (new_col in range(len(board.board[new_row]))) and (steps < move_distance or move_distance == -1):
                        target = board.board[new_row][new_col]
                        try:
                            disallowed_pieces = target.disallowed_pieces
                        except:
                            disallowed_pieces = []
                        try:
                            if piece.name in disallowed_pieces:
                                break
                            elif target.piece == None and can_move_empty:
                                legal_moves.append(StandardBoard.index_to_tile(new_row, new_col))
                            else:
                                if can_capture and not target.piece.is_allies(allies, not multiteam_capture_ally):
                                    legal_moves.append(StandardBoard.index_to_tile(new_row, new_col))
                                break
                        except:
                            break
                        if first_move_boost > 1 and not piece.has_moved:
                            for i in range(first_move_boost - 1):
                                new_row += delta[0]
                                new_col += delta[1]
                                try:
                                    target = board.board[new_row][new_col]
                                    if target.piece == None:
                                        legal_moves.append(StandardBoard.index_to_tile(new_row, new_col))
                                except:
                                    break
                        new_row += delta[0]
                        new_col += delta[1]
                        steps += 1
                    
        return legal_moves


    def get_legal_moves(self, tile, board: StandardBoard, check=False):
        piece = board.get_tile(tile)
        current_team = board.current_team
        legal_moves = []

        # None Tiles
        if piece == None:
            return legal_moves

        # Empy Tile
        if piece.piece == None:
            return legal_moves

        # All Other Pieces
        legal_moves.extend(self.add_ruleset(tile, board, self.rulesets[piece.piece.name]))

        return legal_moves

    def is_in_check(self, team, board: StandardBoard):
        return False

    def all_legal_moves(self, team, board: StandardBoard, filter_capture=False):
        legal_moves = []
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                tile = board.board[row][col]
                if tile != None and tile.piece != None and team == tile.piece.team.name:
                    moves = self.get_legal_moves(StandardBoard.index_to_tile(row, col), board)
                    if moves:
                        if filter_capture:
                            filtered_moves = [move for move in moves if board.get_tile(move).piece != None]
                            if filtered_moves:
                                legal_moves += [(StandardBoard.index_to_tile(row, col), move) for move in filtered_moves]
                        else:
                            legal_moves += [(StandardBoard.index_to_tile(row, col), move) for move in moves]
        return legal_moves

    def get_board_score(self, board):
        scores = dict()
        for team in self.teams:
            scores[team] = 0

        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                tile = board.board[row][col]
                if tile != None and tile.piece != None:
                    for team in tile.piece.get_team_names():
                        scores[team] += self.rulesets[tile.piece.name].points
        
        return scores
    
    def get_move_score(self, board: StandardBoard, start_tile, end_tile):
        scores = dict()
        for team in self.teams:
            scores[team] = 0
        
        if start_tile == end_tile:
            return scores

        if board.get_tile(start_tile) != None and board.get_tile(start_tile).piece != None:
            start_tile_point = self.rulesets[board.get_tile(start_tile).piece.name].points
            start_tile_teams = board.get_tile(start_tile).piece.get_team_names()
        else:
            start_tile_point = 0
            start_tile_teams = []

        if board.get_tile(end_tile) != None and board.get_tile(end_tile).piece != None:
            end_tile_point = self.rulesets[board.get_tile(end_tile).piece.name].points
            end_tile_teams = board.get_tile(end_tile).piece.get_team_names()
        else:
            end_tile_point = 0
            end_tile_teams = []
        
        for team in end_tile_teams:
            scores[team] -= end_tile_point

        if board.get_tile(start_tile) != None and board.get_tile(start_tile).piece != None:
            for team in start_tile_teams:
                if self.rulesets[board.get_tile(start_tile).piece.name].promotion != None and end_tile in self.promotion_tiles[team]:
                    promotion_points = self.rulesets[self.rulesets[board.get_tile(start_tile).piece.name].promotion].points
                    scores[team] += promotion_points - start_tile_point

        return scores

    def play_move(self, board: StandardBoard, start_tile, end_tile, illegal_moves=False, check=True, simulated_move=False) -> StandardBoard:
        if not illegal_moves:
            legal_moves = self.get_legal_moves(start_tile, board, check)
            if end_tile not in legal_moves:
                print("Illegal Move")
                return board
        
        if board.current_team not in board.get_tile(start_tile).piece.get_team_names():
            print("You Can't Play Your Opponent's Pieces")
            return board
            
        start = StandardBoard.tile_to_index(start_tile)
        end = StandardBoard.tile_to_index(end_tile)

        piece = board.get_tile(start_tile).piece

        royal_tiles = board.royal_tiles
        if board.get_tile(start_tile).piece.is_royal:
            royal_tiles.remove(start_tile)
            royal_tiles.append(end_tile)

        new_board = board.board
        new_board[end[0]][end[1]], new_board[start[0]][start[1]] = board.get_tile(end_tile).transfer_piece(board.get_tile(start_tile))


        ruleset = self.rulesets[piece.name]
        promotion = ruleset.promotion
        if promotion != None:
            if end_tile in self.promotion_tiles[board.current_team]:
                new_board[end[0]][end[1]] = new_board[end[0]][end[1]].promote(promotion)

        next_index = self.turn_order.index(board.current_team) + 1
        if next_index in range(len(self.turn_order)):
            next_team = self.turn_order[next_index]
        else:
            next_team = self.turn_order[0]
        new_board_obj = StandardBoard(next_team, new_board, royal_tiles)
        # if not simulated_move:
        #     print(f'{board.current_team} moved {piece.name} from {start_tile} to {end_tile}')
        return new_board_obj
    
    def ai_play(self, board: StandardBoard, check=True, ai_type='random', simulated_move=False, return_move_score=False):
        start_board = board
        new_board = board
        ai_start_tile, ai_end_tile = ('a1', 'a1')
        if ai_type == 'random_prioritize_capture':
            ai_legal_moves = self.all_legal_moves(board.current_team, board, True)
            if ai_legal_moves:
                ai_start_tile, ai_end_tile = random.choice(ai_legal_moves)
                new_board = self.play_move(board, ai_start_tile, ai_end_tile, False, check, simulated_move)
            else:
                new_board = self.ai_play(board, check, 'random')
        elif ai_type == 'random':
            ai_legal_moves = self.all_legal_moves(board.current_team, board)
            if ai_legal_moves:
                ai_start_tile, ai_end_tile = random.choice(ai_legal_moves)
                new_board = self.play_move(board, ai_start_tile, ai_end_tile, False, check, simulated_move)
        elif ai_type[:6] == 'minmax':
            mode = ai_type.split('-')[0].split('_')[1:]
            strength = int(ai_type.split('-')[1])
            try:
                opponent_strength = int(ai_type.split('-')[2])
            except:
                opponent_strength = 0
            opponent_strength = min(opponent_strength, strength - 1)
            opponent_strength = max(opponent_strength, 0)
            ai_legal_moves = self.all_legal_moves(board.current_team, board)
            max_scoring_move = None
            scores = []
            if strength == 0 and ai_legal_moves:
                for ai_start_tile, ai_end_tile in ai_legal_moves:
                    team_points = self.get_move_score(new_board, ai_start_tile, ai_end_tile)
                    maximize = 0
                    for team in team_points:
                        if team not in self.turn_order:
                            continue
                        elif team in self.teams[board.current_team].allies:
                            maximize += team_points[team]
                        else:
                            maximize -= team_points[team]
                    scores += [maximize]
                    if max_scoring_move == None:
                        max_scoring_move = maximize
                    else:
                        max_scoring_move = max(maximize, max_scoring_move)

                filtered_moves = [ai_legal_moves[i] for i in range(len(ai_legal_moves)) if scores[i] == max_scoring_move]
                if filtered_moves:
                    ai_start_tile, ai_end_tile = random.choice(filtered_moves)
                    new_board = self.play_move(board, ai_start_tile, ai_end_tile, False, check, simulated_move)
            elif ai_legal_moves:
                for ai_start_tile, ai_end_tile in ai_legal_moves:
                    skip_move = False
                    maximize = 0
                    accumulated_scores = self.get_move_score(new_board, ai_start_tile, ai_end_tile)
                    try:
                        if mode[1] == 'smart' and accumulated_scores[board.current_team] == -900:
                            scores += -99999
                            continue
                        elif mode[1] == 'smart' and -900 in accumulated_scores.values():
                            scores += 99999
                            continue
                    except:
                        pass
                    new_board = self.play_move(board.copy(), ai_start_tile, ai_end_tile, False, check, True)
                    for i in range(strength):
                        new_board, turn_score = self.ai_play(new_board, check, f'{ai_type.split("-"[0])}-{opponent_strength}-{opponent_strength-1}', True, True)
                        try:
                            if mode[1] == 'smart' and turn_score[board.current_team] == -900:
                                skip_move = False
                                break
                        except:
                            pass
                        strength_factor = 1
                        if mode[0] == 'sib': # Sooner is Better
                            strength_factor = max(0, min(1, 1/(1 + (i+1)//len(self.turn_order))))
                        elif mode[0] == 'lib': # Later is Better
                            strength_factor = max(0, min(1, 1 - 1/(1 + (i+1)//len(self.turn_order))))
                        for team in accumulated_scores:
                            accumulated_scores[team] += turn_score[team] * strength_factor
                    if skip_move:
                        scores += -99999
                        continue
                    for team in accumulated_scores:
                        if team not in self.turn_order:
                            continue
                        elif team in self.teams[board.current_team].allies:
                            maximize += accumulated_scores[team]
                        else:
                            maximize -= accumulated_scores[team]
                    scores += [maximize]
                    if max_scoring_move == None:
                        max_scoring_move = maximize
                    else:
                        max_scoring_move = max(maximize, max_scoring_move)
                filtered_moves = [ai_legal_moves[i] for i in range(len(scores)) if scores[i] == max_scoring_move]
                if filtered_moves:
                    ai_start_tile, ai_end_tile = random.choice(filtered_moves)
                    new_board = self.play_move(board, ai_start_tile, ai_end_tile, False, check, simulated_move)
        if return_move_score:
            return new_board, self.get_move_score(start_board, ai_start_tile, ai_end_tile)
        return new_board

    def __str__(self):
        return str(self.rulesets)

    def __repr__(self) -> str:
        return repr(self.rulesets)