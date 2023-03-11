from board import Board
from render_engine import RenderEngine
from rule_engine import RuleEngine
from variants import Variants

if __name__ == "__main__":
    renderer = RenderEngine(*Variants.WILDERBEAST)
    renderer.render_board(tile_size=50)
