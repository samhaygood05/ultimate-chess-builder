from boards.square_board import SquareBoard
from render_engines.square_render_engine import SquareRenderEngine
from rule_set import RuleSet
from rule_engines.square_rule_engine import SquareRuleEngine
from variants import Variants
from tile import Tile
from teams.team import Team, TeamPresets as tp

if __name__ == "__main__":
    renderer = SquareRenderEngine((800, 600), board=SquareBoard(board_state=
                            [[Tile('rook', tp.WHITE), Tile('knight', tp.WHITE), Tile('bishop', tp.WHITE), Tile('queen', tp.WHITE), Tile('king', tp.WHITE), Tile('bishop', tp.WHITE), Tile('knight', tp.WHITE), Tile('rook', tp.WHITE)],
                            [Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE), Tile('pawn', tp.WHITE)],
                            [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                            [Tile(), Tile(), Tile(), None, Tile(), Tile(), Tile(), Tile()],
                            [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                            [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                            [Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK), Tile('pawn', tp.BLACK)],
                            [Tile('rook', tp.BLACK), Tile('knight', tp.BLACK), Tile('bishop', tp.BLACK), Tile('queen', tp.BLACK), Tile('king', tp.BLACK), Tile('bishop', tp.BLACK), Tile('knight', tp.BLACK), Tile('rook', tp.BLACK)]]))
