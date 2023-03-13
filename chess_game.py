from boards.square_board import SquareBoard
from boards.poly_board import PolyBoard
from render_engines.timetravel_render_engine import TimeTravelRenderEngine
from rule_set import RuleSet
from rule_engines.square_rule_engine import SquareRuleEngine
from variants import Variants
from tile import Tile
from teams.time_team import TimeTeam, TimeTeamPresets as tp

if __name__ == "__main__":
    renderer = TimeTravelRenderEngine((800, 600), PolyBoard(boards={
        (0, 0): SquareBoard(board_state=Variants.create_standard_board(tp.WHITE, tp.BLACK))
    },
    active_boards=[(0,0)]))