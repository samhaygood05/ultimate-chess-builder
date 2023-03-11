from board import Board
from render_engine import RenderEngine
from rule_set import RuleSet
from rule_engine import RuleEngine
from variants import Variants
from tile import Tile
from team import Team, TeamPresets as tp

if __name__ == "__main__":
    renderer = RenderEngine(*Variants.load('2team_4player'))
    renderer.render_board(tile_size=90)
