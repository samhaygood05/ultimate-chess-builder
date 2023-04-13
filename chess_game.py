import sys
from graph_board import GraphBoard, GraphPresets as gp
from render_engines import *
from rule_engines import GraphRuleEngine
from movement import RuleSet, RulePresets as rp, Moveset, MovesetPresets as mp, Move
from teams import Team, TeamPresets as tp
from piece import Piece
from variants import Variants
import pygame
import matplotlib.pyplot as plt
import math
from tile import Tile


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    pygame.init()

    game = 'square/4player_knight_allience'

    renderer = Variants.load(game)

    renderer.initialize((800, 800), 1.0, {
        'blue': 'minmax_lib_smart-8',
        'red': 'minmax_sib-8',
        'yellow': 'minmax_sib_smart-8',
        'green': 'random'
    })

    plt.show()
