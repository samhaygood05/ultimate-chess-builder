from board import Board
from variants import Variants

if __name__ == "__main__":
    board = Board(board_state=Variants.WILDEBEAST_CHESS, rulesets=Variants.WILDEBEAST_RULESET)
    board.render_board(tile_size=50)
