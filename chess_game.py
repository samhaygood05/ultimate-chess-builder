from boards.square_board import SquareBoard
from render_engines.square_render_engine import SquareRenderEngine
from rule_set import RuleSet
from rule_engines.square_rule_engine import SquareRuleEngine
from variants import Variants
from tile import Tile
from teams.team import Team, TeamPresets as tp

if __name__ == "__main__":
    renderer = SquareRenderEngine((800, 600), SquareBoard(board_state=Variants.create_standard_board(tp.WHITE, tp.BLACK, 6)))
