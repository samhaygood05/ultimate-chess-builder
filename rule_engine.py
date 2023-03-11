from rule_set import RuleSet
from board import Board
from team import Team
from tile import Tile

class RuleEngine:
    def __init__(self, rulesets: dict = None):
        self.rulesets = RuleSet.rule_dict(
            RuleSet('pawn', [(1, 0)], [(1, -1), (1, 1)], True, False, True, 'queen'),
            RuleSet('rook', [(0, 1), (0, -1), (1, 0), (-1, 0)], None, False, True, False),
            RuleSet('bishop', [(-1, -1), (-1, 1), (1, -1), (1, 1)], None, False, True, False),
            RuleSet('knight', [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)], None, False, False, False),
            RuleSet('queen', [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], None, False, True, False),
            RuleSet('king', [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], None, False, False, False)
        )
        if rulesets != None:
            self.rulesets.update(rulesets)

    def add_ruleset(self, tile, board: Board, ruleset: RuleSet):
        piece = board.get_tile(tile)
        team = piece.team
        piece_name = ruleset.name
        moveset = ruleset.moveset
        captureset = ruleset.captureset
        first_move = ruleset.first_move
        multimove = ruleset.multimove
        directional = ruleset.directional

        if captureset == None:
            captureset = moveset
        enemy = Team.EMPTY
        if team == Team.WHITE:
            enemy = Team.BLACK
        elif team == Team.BLACK:
            enemy = Team.WHITE
        row, col = Board.tile_to_index(tile)
        legal_moves = []
        direction = 1
        if directional and team == Team.BLACK:
            direction = -1

        if piece.piece == piece_name:
            # Logic for Moveset
            for delta_row, delta_col in moveset:
                new_row = row + delta_row*direction
                new_col = col + delta_col
                if multimove:
                    while (new_row in range(len(board.board))) and (new_col in range(len(board.board[new_row]))):
                        target = board.board[new_row][new_col]
                        if target == None:
                            break
                        if target.piece == 'empty':
                            legal_moves.append(Board.index_to_tile(new_row, new_col))
                        else:
                            break
                        new_row += delta_row*direction
                        new_col += delta_col
                else:
                    if (new_row in range(len(board.board))) and (new_col in range(len(board.board[new_row]))):
                        target = board.board[new_row][new_col]
                        if target != None:
                            if target.piece == 'empty':
                                legal_moves.append(Board.index_to_tile(new_row, new_col))
                                if first_move and not piece.has_moved:
                                    while new_row < len(board.board) / 2 - 1 or new_row > len(board.board) / 2:
                                        new_row += delta_row*direction
                                        new_col += delta_col
                                        try:
                                            target = board.board[new_row][new_col]
                                            if target.piece == 'empty':
                                                legal_moves.append(Board.index_to_tile(new_row, new_col ))
                                        except:
                                            break
            # Logic for Capture Set
            for delta_row, delta_col in captureset:
                new_row = row + delta_row*direction
                new_col = col + delta_col
                if multimove:
                    while (new_row in range(len(board.board))) and (new_col in range(len(board.board[new_row]))):
                        target = board.board[new_row][new_col]
                        if target == None:
                            break
                        if target.piece == 'empty':
                            pass
                        elif target.team == enemy:
                            legal_moves.append(Board.index_to_tile(new_row, new_col))
                            break
                        else:
                            break
                        new_row += delta_row*direction
                        new_col += delta_col
                else:
                    if (new_row in range(len(board.board))) and (new_col in range(len(board.board[new_row]))):
                        target = board.board[new_row][new_col]
                        if target != None:
                            if target.team == enemy:
                                legal_moves.append(Board.index_to_tile(new_row, new_col))
        return legal_moves


    def get_legal_moves(self, tile, board: Board):
        piece = board.get_tile(tile)
        legal_moves = []

        # None Tiles
        if piece == None:
            return legal_moves

        # Empy Tile
        if piece.piece == 'empty':
            return legal_moves

        # All Other Pieces
        for name, rules in self.rulesets.items():
            legal_moves.extend(self.add_ruleset(tile, board, rules))

        return legal_moves

    def is_in_check(self, team):
        pass
    
    def all_legal_moves(self, team, board: Board):
        legal_moves = []
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                tile = board.board[row][col]
                if team == tile.team:
                    legal_moves.extend(self.get_legal_moves(tile, board))
        return legal_moves

    def play_move(self, board: Board, start_tile, end_tile, illegal_moves=False) -> Board:
        if board.white_first:
            current_team = Team.WHITE
        else:
            current_team = Team.BLACK
        if not illegal_moves:
            legal_moves = self.get_legal_moves(start_tile, board)
            if end_tile not in legal_moves:
                print("Illegal Move")
                return board
        
        if board.get_tile(start_tile).team != current_team:
            print("You Can't Play Your Opponent's Pieces")
            return board
            
        start = Board.tile_to_index(start_tile)
        end = Board.tile_to_index(end_tile)

        piece = board.get_tile(start_tile).piece

        new_board = board.board
        new_board[end[0]][end[1]] = board.get_tile(start_tile).moved()
        new_board[start[0]][start[1]] = Tile()

        ruleset = self.rulesets[piece]
        promotion, promotion_row = ruleset.promotion, ruleset.promotion_row
        if promotion != None:
            if (end[0] == len(board.board) - 1 - promotion_row and current_team == Team.WHITE) or (end[0] == promotion_row and current_team == Team.BLACK):
                new_board[end[0]][end[1]] = new_board[end[0]][end[1]].promote(promotion)

        return Board(not board.white_first, new_board)
    
    def __str__(self):
        return str(self.rulesets)

    def __repr__(self) -> str:
        return repr(self.rulesets)