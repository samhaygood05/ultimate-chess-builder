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

from rule_set import RuleSet
from boards.standard_board import StandardBoard as Board
from teams.team import Team
from tile import Tile
from teams.team import TeamPresets as tp
from rule_engines.abstract_rule_engine import AbstractRuleEngine

class StandardRuleEngine(AbstractRuleEngine):
    def __init__(self, rulesets: dict = None, teams = None, promotion_tiles = None, turn_order = None, multiteam_capture_ally = False, hexagonal=False):
        if hexagonal:
            self.rulesets = RuleSet.rule_dict(
            RuleSet('pawn', [(1, 1)], [(0, 1), (1, 0)], True, 2, False, 'queen'),
            RuleSet('rook', [(1,0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)], None, False, 0, True),
            RuleSet('bishop', [(2, 1), (1, 2), (-1, 1), (1, -1), (-2, -1), (-1, -2)], None, False, 0, True),
            RuleSet('knight', [(1, 3), (2, 3), (3, 2), (3, 1), (2, -1), (1, -2), (-1, -3), (-2, -3), (-3, -2), (-3, -1), (-2, 1), (-1, 2)], None, False, 0, False),
            RuleSet('queen', [(1, -1), (-1, 1), (1,0), (-1, 0), (0, 1), (0, -1), (2, 1), (1, 2), (1, 1), (-1, -1), (-2, -1), (-1, -2)], None, False, 0, True),
            RuleSet('king', [(1, -1), (-1, 1), (1,0), (-1, 0), (0, 1), (0, -1), (2, 1), (1, 2), (1, 1), (-1, -1), (-2, -1), (-1, -2)], None, False, 0, False)
        )
        else:
            self.rulesets = RuleSet.rule_dict(
                RuleSet('pawn', [(1, 0)], [(1, -1), (1, 1)], True, 2, False, 'queen'),
                RuleSet('rook', [(0, 1), (0, -1), (1, 0), (-1, 0)], None, False, 0, True),
                RuleSet('bishop', [(-1, -1), (-1, 1), (1, -1), (1, 1)], None, False, 0, True),
                RuleSet('knight', [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)], None, False, 0, False),
                RuleSet('queen', [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], None, False, 0, True),
                RuleSet('king', [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], None, False, 0, False)
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

    def add_ruleset(self, tile, board: Board, ruleset: RuleSet):
        piece = board.get_tile(tile)
        team = piece.team
        if piece.has_moved and self.multiteam_capture_ally:
            allies = piece.get_allies_intersection()
            multiteam_capture_ally = True
        else:
            allies = piece.get_allies_union()
            multiteam_capture_ally = False

        piece_name = ruleset.name
        moveset = ruleset.moveset
        captureset = ruleset.captureset
        first_move = ruleset.first_move
        first_move_boost = ruleset.first_move_boost
        multimove = ruleset.multimove

        if captureset == None:
            captureset = moveset

        row, col = Board.tile_to_index(tile)
        legal_moves = []
        direction = team.direction
        side_direction = team.perpendicular

        if piece.piece == piece_name:
            # Logic for Moveset
            for delta_forward, delta_right in moveset:
                delta = (delta_forward*direction[0] + delta_right*side_direction[0], delta_forward*direction[1] + delta_right*side_direction[1])

                new_row = row + delta[0]
                new_col = col + delta[1]
                if multimove:
                    while (new_row in range(len(board.board))) and (new_col in range(len(board.board[new_row]))):
                        target = board.board[new_row][new_col]
                        if target == None:
                            break
                        if target.piece == 'empty':
                            legal_moves.append(Board.index_to_tile(new_row, new_col))
                        else:
                            break
                        new_row += delta[0]
                        new_col += delta[1]
                else:
                    if (new_row in range(len(board.board))) and (new_col in range(len(board.board[new_row]))):
                        target = board.board[new_row][new_col]
                        if target != None:
                            if target.piece == 'empty':
                                legal_moves.append(Board.index_to_tile(new_row, new_col))
                                if first_move and not piece.has_moved:
                                    for i in range(first_move_boost - 1):
                                        new_row += delta[0]
                                        new_col += delta[1]
                                        try:
                                            target = board.board[new_row][new_col]
                                            if target.piece == 'empty':
                                                legal_moves.append(Board.index_to_tile(new_row, new_col))
                                        except:
                                            break
            # Logic for Capture Set
            for delta_forward, delta_right in captureset:
                delta = (delta_forward*direction[0] + delta_right*side_direction[0], delta_forward*direction[1] + delta_right*side_direction[1])

                new_row = row + delta[0]
                new_col = col + delta[1]
                if multimove:
                    while (new_row in range(len(board.board))) and (new_col in range(len(board.board[new_row]))):
                        target = board.board[new_row][new_col]
                        if target == None:
                            break
                        if target.piece == 'empty':
                            pass
                        elif not target.is_allies(allies, not multiteam_capture_ally):
                            legal_moves.append(Board.index_to_tile(new_row, new_col))
                            break
                        else:
                            break
                        new_row += delta[0]
                        new_col += delta[1]
                else:
                    if (new_row in range(len(board.board))) and (new_col in range(len(board.board[new_row]))):
                        target = board.board[new_row][new_col]
                        if target != None:
                            if not target.is_allies(allies, not multiteam_capture_ally):
                                legal_moves.append(Board.index_to_tile(new_row, new_col))
        return legal_moves


    def get_legal_moves(self, tile, board: Board, check=False):
        piece = board.get_tile(tile)
        legal_moves = []

        # None Tiles
        if piece == None:
            return legal_moves

        # Empy Tile
        if piece.piece == 'empty':
            return legal_moves

        # All Other Pieces
        legal_moves.extend(self.add_ruleset(tile, board, self.rulesets[piece.piece]))

        if check and piece.is_royal:
            board_copy = board.copy()
            for move in legal_moves:
                board_moved = self.play_move(board_copy, tile, move, check=False)
                for royal_tile in board_moved.royal_tiles:
                    if self.is_in_check(royal_tile, board_moved):
                        legal_moves.remove(move)
                        break


        return legal_moves

    def is_in_check(self, tile, board: Board):
        return False

    def all_legal_moves(self, team, board: Board):
        legal_moves = []
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                tile = board.board[row][col]
                if team == tile.team.name:
                    legal_moves.extend(self.get_legal_moves(tile, board))
        return legal_moves

    def play_move(self, board: Board, start_tile, end_tile, illegal_moves=False, check=True) -> Board:
        if not illegal_moves:
            legal_moves = self.get_legal_moves(start_tile, board, check)
            if end_tile not in legal_moves:
                print("Illegal Move")
                return board
        
        if board.current_team not in board.get_tile(start_tile).get_team_names():
            print("You Can't Play Your Opponent's Pieces")
            return board
            
        start = Board.tile_to_index(start_tile)
        end = Board.tile_to_index(end_tile)

        piece = board.get_tile(start_tile).piece

        royal_tiles = board.royal_tiles
        if board.get_tile(start_tile).is_royal:
            royal_tiles.remove(start_tile)
            royal_tiles.append(end_tile)

        new_board = board.board
        new_board[end[0]][end[1]] = board.get_tile(start_tile).moved()
        new_board[start[0]][start[1]] = Tile()


        ruleset = self.rulesets[piece]
        promotion = ruleset.promotion
        if promotion != None:
            if end_tile in self.promotion_tiles[board.current_team]:
                new_board[end[0]][end[1]] = new_board[end[0]][end[1]].promote(promotion)

        next_index = self.turn_order.index(board.current_team) + 1
        if next_index in range(len(self.turn_order)):
            next_team = self.turn_order[next_index]
        else:
            next_team = self.turn_order[0]
        return Board(next_team, new_board, royal_tiles)
    
    def __str__(self):
        return str(self.rulesets)

    def __repr__(self) -> str:
        return repr(self.rulesets)