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

from rule_engines.abstract_rule_engine import AbstractRuleEngine
from boards.poly_board import PolyBoard
from rule_set import RuleSet
from teams.time_team import TimeTeam, TimeTeamPresets as tp
from tile import Tile
import copy

class TimeTravelRuleEngine(AbstractRuleEngine):
    def __init__(self, rulesets: dict = None, teams = None, promotion_tiles = None, turn_order = None):
        self.rulesets = RuleSet.rule_dict(
            RuleSet('pawn', [(1, 0, 0, 0), (0, 0, 1, 0)], [(1, -1, 0, 0), (1, 1, 0, 0), (0, -1, 1, 0), (0, 1, 1, 0)], True, 2, False, 'queen'),
            RuleSet('rook', [(0, 1, 0, 0), (0, -1, 0, 0), (1, 0, 0, 0), (-1, 0, 0, 0), (0, 0, 0, 1), (0, 0, 0, -1), (0, 0, 1, 0), (0, 0, -1, 0)], None, False, 0, True),
            RuleSet('bishop', [(-1, -1, 0, 0), (-1, 1, 0, 0), (1, -1, 0, 0), (1, 1, 0, 0), 
                               (-1, 0, -1, 0), (-1, 0, 1, 0), (1, 0, -1, 0), (1, 0, 1, 0),
                               (-1, 0, 0, -1), (-1, 0, 0, 1), (1, 0, 0, -1), (1, 0, 0, 1),
                               (0, -1, -1, 0), (0, -1, 1, 0), (0, 1, -1, 0), (0, 1, 1, 0),
                               (0, -1, 0, -1), (0, -1, 0, 1), (0, 1, 0, -1), (0, 1, 0, 1),
                               (0, 0, -1, -1), (0, 0, -1, 1), (0, 0, 1, -1), (0, 0, 1, 1)
                               ], None, False, 0, True),
            RuleSet('knight', [(-2, -1, 0, 0), (-2, 1, 0, 0), (2, -1, 0, 0), (2, 1, 0, 0), (-1, -2, 0, 0), (-1, 2, 0, 0), (1, -2, 0, 0), (1, 2, 0, 0),
                               (-2, 0, -1, 0), (-2, 0, 1, 0), (2, 0, -1, 0), (2, 0, 1, 0), (-1, 0, -2, 0), (-1, 0, 2, 0), (1, 0, -2, 0), (1, 0, 2, 0),
                               (-2, 0, 0, -1), (-2, 0, 0, 1), (2, 0, 0, -1), (2, 0, 0, 1), (-1, 0, 0, -2), (-1, 0, 0, 2), (1, 0, 0, -2), (1, 0, 0, 2),
                               (0, -2, -1, 0), (0, -2, 1, 0), (0, 2, -1, 0), (0, 2, 1, 0), (0, -1, -2, 0), (0, -1, 2, 0), (0, 1, -2, 0), (0, 1, 2, 0),
                               (0, -2, 0, -1), (0, -2, 0, 1), (0, 2, 0, -1), (0, 2, 0, 1), (0, -1, 0, -2), (0, -1, 0, 2), (0, 1, 0, -2), (0, 1, 0, 2),
                               (0, 0, -2, -1), (0, 0, -2, 1), (0, 0, 2, -1), (0, 0, 2, 1), (0, 0, -1, -2), (0, 0, -1, 2), (0, 0, 1, -2), (0, 0, 1, 2)
                               ], None, False, 0, False),
            RuleSet('queen', [(0, 0, 0, -1), (0, 0, 0, 1), (0, 0, -1, 0), (0, 0, 1, 0), (0, 0, -1, -1), (0, 0, -1, 1), (0, 0, 1, -1), (0, 0, 1, 1),
                              (0, -1, 0, -1), (0, -1, 0, 1), (0, -1, -1, 0), (0, -1, 1, 0), (0, -1, -1, -1), (0, -1, -1, 1), (0, -1, 1, -1), (0, -1, 1, 1),
                              (0, 1, 0, -1), (0, 1, 0, 1), (0, 1, -1, 0), (0, 1, 1, 0), (0, 1, -1, -1), (0, 1, -1, 1), (0, 1, 1, -1), (0, 1, 1, 1),
                              (-1, -1, 0, -1), (-1, -1, 0, 1), (-1, -1, -1, 0), (-1, -1, 1, 0), (-1, -1, -1, -1), (-1, -1, -1, 1), (-1, -1, 1, -1), (-1, -1, 1, 1),
                              (-1, 1, 0, -1), (-1, 1, 0, 1), (-1, 1, -1, 0), (-1, 1, 1, 0), (-1, 1, -1, -1), (-1, 1, -1, 1), (-1, 1, 1, -1), (-1, 1, 1, 1),
                              (1, -1, 0, -1), (1, -1, 0, 1), (1, -1, -1, 0), (1, -1, 1, 0), (1, -1, -1, -1), (1, -1, -1, 1), (1, -1, 1, -1), (1, -1, 1, 1),
                              (1, 1, 0, -1), (1, 1, 0, 1), (1, 1, -1, 0), (1, 1, 1, 0), (1, 1, -1, -1), (1, 1, -1, 1), (1, 1, 1, -1), (1, 1, 1, 1)
                              ], None, False, 0, True),
            RuleSet('king', [(0, 0, 0, -1), (0, 0, 0, 1), (0, 0, -1, 0), (0, 0, 1, 0), (0, 0, -1, -1), (0, 0, -1, 1), (0, 0, 1, -1), (0, 0, 1, 1),
                             (0, -1, 0, -1), (0, -1, 0, 1), (0, -1, -1, 0), (0, -1, 1, 0), (0, -1, -1, -1), (0, -1, -1, 1), (0, -1, 1, -1), (0, -1, 1, 1),
                             (0, 1, 0, -1), (0, 1, 0, 1), (0, 1, -1, 0), (0, 1, 1, 0), (0, 1, -1, -1), (0, 1, -1, 1), (0, 1, 1, -1), (0, 1, 1, 1),
                             (-1, -1, 0, -1), (-1, -1, 0, 1), (-1, -1, -1, 0), (-1, -1, 1, 0), (-1, -1, -1, -1), (-1, -1, -1, 1), (-1, -1, 1, -1), (-1, -1, 1, 1),
                             (-1, 1, 0, -1), (-1, 1, 0, 1), (-1, 1, -1, 0), (-1, 1, 1, 0), (-1, 1, -1, -1), (-1, 1, -1, 1), (-1, 1, 1, -1), (-1, 1, 1, 1),
                             (1, -1, 0, -1), (1, -1, 0, 1), (1, -1, -1, 0), (1, -1, 1, 0), (1, -1, -1, -1), (1, -1, -1, 1), (1, -1, 1, -1), (1, -1, 1, 1),
                             (1, 1, 0, -1), (1, 1, 0, 1), (1, 1, -1, 0), (1, 1, 1, 0), (1, 1, -1, -1), (1, 1, -1, 1), (1, 1, 1, -1), (1, 1, 1, 1)
                             ], None, False, 0, False)
        )
        if rulesets != None:
            self.rulesets.update(rulesets)

        if teams == None:
            self.teams = TimeTeam.team_dict(tp.WHITE, tp.BLACK)
        else:
            self.teams = teams
        if promotion_tiles == None:
            self.promotion_tiles = {
                'white': ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
                'black': ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
            }
        else: self.promotion_tiles = promotion_tiles
        if turn_order == None:
            self.turn_order = list(self.teams.keys())
        else:
            self.turn_order = turn_order

    def add_ruleset(self, tile_loc, board: PolyBoard, ruleset: RuleSet):
        piece = board.get_tile(*tile_loc)
        team = piece.team
        allies = team.allies
        piece_name = ruleset.name
        moveset = ruleset.moveset
        captureset = ruleset.captureset
        first_move = ruleset.first_move
        first_move_boost = ruleset.first_move_boost
        multimove = ruleset.multimove

        if captureset == None:
            captureset = moveset

        (board_row, board_col), tile = tile_loc

        row, col = PolyBoard.tile_to_index(tile)
        legal_moves = []
        direction = team.direction
        side_direction = team.perpendicular
        time_direction = team.time_direction

        if piece.piece == piece_name:
            # Logic for Moveset
            for delta_forward, delta_right, delta_parallel, delta_time in moveset:
                delta = (delta_forward*direction[0] + delta_right*side_direction[0], delta_forward*direction[1] + delta_right*side_direction[1], delta_parallel*time_direction, delta_time)

                new_row = row + delta[0]
                new_col = col + delta[1]
                new_board = (board_row + delta[2], board_col + delta[3])

                try:
                    target_board = board.boards[new_board]
                    if multimove:
                        while (new_row in range(len(target_board.board))) and (new_col in range(len(target_board.board[new_row]))):
                            target = target_board.board[new_row][new_col]
                            if target != None:
                                if target.piece == 'empty':
                                    legal_moves.append((new_board, PolyBoard.index_to_tile(new_row, new_col)))
                                else:
                                    break
                                new_row += delta[0]
                                new_col += delta[1]
                                new_board = (new_board[0] + delta[2], new_board[1] + delta[3])
                                target_board = board.boards[new_board]
                    else:
                        target_board = board.boards[new_board]
                        if (new_row in range(len(target_board.board))) and (new_col in range(len(target_board.board[new_row]))):
                            target = target_board.board[new_row][new_col]
                            if target != None:
                                if target.piece == 'empty':
                                    legal_moves.append((new_board, PolyBoard.index_to_tile(new_row, new_col)))
                                    if first_move and not piece.has_moved:
                                        for i in range(first_move_boost - 1):
                                            new_row += delta[0]
                                            new_col += delta[1]
                                            new_board = (new_board[0] + delta[2], new_board[1] + delta[3])
                                            try:
                                                target_board = board.boards[new_board]
                                                target = target_board.board[new_row][new_col]
                                                if target.piece == 'empty':
                                                    legal_moves.append((new_board, PolyBoard.index_to_tile(new_row, new_col)))
                                            except:
                                                break
                except:
                    pass

            # Logic for Captureset
            for delta_forward, delta_right, delta_parallel, delta_time in captureset:
                delta = (delta_forward*direction[0] + delta_right*side_direction[0], delta_forward*direction[1] + delta_right*side_direction[1], delta_parallel*time_direction, delta_time)

                new_row = row + delta[0]
                new_col = col + delta[1]
                new_board = (board_row + delta[2], board_col + delta[3])

                try:
                    target_board = board.boards[new_board]
                    if multimove:
                        while (new_row in range(len(target_board.board))) and (new_col in range(len(target_board.board[new_row]))):
                            target = target_board.board[new_row][new_col]
                            if target == None:
                                break
                            if target.piece == 'empty':
                                pass
                            elif target.team.name not in allies:
                                legal_moves.append((new_board, PolyBoard.index_to_tile(new_row, new_col)))
                                break
                            else:
                                break
                            new_row += delta[0]
                            new_col += delta[1]
                            new_board = (new_board[0] + delta[2], new_board[1] + delta[3])
                            target_board = board.boards[new_board]
                    else:
                        target_board = board.boards[new_board]
                        if (new_row in range(len(target_board.board))) and (new_col in range(len(target_board.board[new_row]))):
                            target = target_board.board[new_row][new_col]
                            if target != None:
                                if target.team.name not in allies:
                                    legal_moves.append((new_board, PolyBoard.index_to_tile(new_row, new_col)))
                except:
                    pass
            return legal_moves

    def get_legal_moves(self, tile_loc, board: PolyBoard):
        piece = board.get_tile(*tile_loc)
        legal_moves = []

        # None Tiles
        if piece == None:
            return legal_moves
        
        # Empty Tile
        if piece.piece == 'empty':
            return legal_moves
        
        # All Other Pieces
        legal_moves.extend(self.add_ruleset(tile_loc, board, self.rulesets[piece.piece]))

        return legal_moves
    
    def is_in_check(self, team):
        pass

    def play_move(self, board: PolyBoard, start_tile_loc, end_tile_loc, illegal_moves=False):
        if not illegal_moves:
            legal_moves = self.get_legal_moves(start_tile_loc, board)
            if end_tile_loc not in legal_moves:
                print("Illegal Move")
                return board
        
        start_board, start_tile = start_tile_loc

        if start_board not in board.active_boards:
            print("You Can't Play on an Inactive Board")
            return board
        
        current_team = board.boards[start_board].current_team

        if board.get_tile(*start_tile_loc).team.name != current_team:
            print("You Can't Play Your Opponent's Pieces")
            return board
        
        end_board, end_tile = end_tile_loc
        start = PolyBoard.tile_to_index(start_tile)
        end = PolyBoard.tile_to_index(end_tile)

        piece = board.get_tile(*start_tile_loc).piece

        if start_board == end_board:
            board.active_boards.remove(start_board)
            new_board = copy.deepcopy(board.boards[start_board].board)
            new_board[end[0]][end[1]] = board.boards[start_board].get_tile(start_tile).moved()
            new_board[start[0]][start[1]] = Tile()


            ruleset = self.rulesets[piece]
            promotion = ruleset.promotion
            if promotion != None:
                if end_tile in self.promotion_tiles[current_team]:
                    new_board[end[0]][end[1]] = new_board[end[0]][end[1]].promote(promotion)

            next_index = self.turn_order.index(current_team) + 1
            if next_index in range(len(self.turn_order)):
                next_team = self.turn_order[next_index]
            else:
                next_team = self.turn_order[0]

            new_board_loc = (start_board[0], start_board[1] + 1)
            new_board_object = board.boards[start_board].copy()
            new_board_object.current_team = next_team
            new_board_object.board = new_board

            board.active_boards.append(new_board_loc)

            return board.add_board(new_board_loc, new_board_object)
        else:
            new_start_board = copy.deepcopy(board.boards[start_board].board)
            new_end_board = copy.deepcopy(board.boards[end_board].board)

            board.active_boards.remove(start_board)
            try:
                board.active_boards.remove(end_board)
            except:
                pass

            new_end_board[end[0]][end[1]] = board.boards[start_board].get_tile(start_tile).moved()
            new_start_board[start[0]][start[1]] = Tile()

            ruleset = self.rulesets[piece]
            promotion = ruleset.promotion
            if promotion != None:
                if end_tile in self.promotion_tiles[current_team]:
                    new_end_board[end[0]][end[1]] = new_end_board[end[0]][end[1]].promote(promotion)

            next_index = self.turn_order.index(current_team) + 1
            if next_index in range(len(self.turn_order)):
                next_team = self.turn_order[next_index]
            else:
                next_team = self.turn_order[0]

            new_start_board_loc = (start_board[0], start_board[1] + 1)
            time_direction = board.get_tile(*start_tile_loc).team.time_direction
            new_end_board_loc = (end_board[0], end_board[1] + 1)
            while new_end_board_loc[0] in [board_a[0] for board_a in board.boards.keys()]:
                new_end_board_loc = (new_end_board_loc[0] - time_direction, new_end_board_loc[1])

            new_start_board_object = board.boards[start_board].copy()
            new_start_board_object.current_team = next_team
            new_start_board_object.board = new_start_board

            new_end_board_object = board.boards[end_board].copy()
            new_end_board_object.current_team = next_team
            new_end_board_object.board = new_end_board

            board.active_boards.append(new_start_board_loc)
            board.active_boards.append(new_end_board_loc)

            return board.add_board(new_start_board_loc, new_start_board_object).add_board(new_end_board_loc, new_end_board_object)


