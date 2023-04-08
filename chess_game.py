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

    game = 'hex/glinski'

    renderer = Variants.load(game)

    renderer.initialize((800, 800), 1.0)

    plt.show()
