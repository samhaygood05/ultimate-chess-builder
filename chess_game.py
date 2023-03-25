from boards.standard_board import StandardBoard
from boards.poly_board import PolyBoard
from render_engines.timetravel_render_engine import TimeTravelRenderEngine
from render_engines.square_render_engine import SquareRenderEngine
from render_engines.hex_render_engine import HexRenderEngine
from rule_set import RuleSet
from rule_engines.standard_rule_engine import StandardRuleEngine
from piece import Piece
from variants import Variants
from tile import Tile
from teams.team import Team, TeamPresets as tp

if __name__ == "__main__":

    renderer = Variants.load('square/4player')
    renderer.initialize((800, 600), {'white': 'minmax-8', 'red': 'minmax-8', 'black': 'minmax-8', 'green': 'minmax-8'}, 1)
    # SquareRenderEngine((800, 600)).initialize((800, 600), {'white': 'minmax-2', 'black': 'minmax-1'}, 2)

