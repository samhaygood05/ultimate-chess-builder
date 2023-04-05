from graph_board import GraphBoard, GraphPresets as gp
from render_engines import *
from rule_engines import GraphRuleEngine
from movement import RuleSet, RulePresets as rp, MovesetPresets as mp
from teams import Team, TeamPresets as tp
from piece import Piece
import pygame
import matplotlib.pyplot as plt
import random

if __name__ == "__main__":
    pygame.init()

    board = gp.create_empty_rectangular_grid(8, 8)
    rule_engine = GraphRuleEngine(teams={'white': tp.WHITE})

    for i in range(8):
        board.add_adjacency((i, 0), (i, 7), 'edge', 'e')
        board.add_adjacency((i, 7), (i, 0), 'edge', 'w')

    for i in range(7):
        board.add_adjacency((i, 0), (i+1, 7), 'vertex', 'ne')
        board.add_adjacency((i+1, 7), (i, 0), 'vertex', 'sw')

    for i in range(1, 8):
        board.add_adjacency((i, 0), (i-1, 7), 'vertex', 'se')
        board.add_adjacency((i-1, 7), (i, 0), 'vertex', 'nw')

    for i in range(4):
        board.add_adjacency((0, i), (0, i+4), 'edge', 's')
        board.add_adjacency((0, i+4), (0, i), 'edge', 's')
        board.add_adjacency((7, i), (7, i+4), 'edge', 'n')
        board.add_adjacency((7, i+4), (7, i), 'edge', 'n')
        board.add_adjacency((0, i), (0, i+4), 'vertex', 'se')
        board.add_adjacency((0, i), (0, i+4), 'vertex', 'sw')
        board.add_adjacency((0, i+4), (0, i), 'vertex', 'se')
        board.add_adjacency((0, i+4), (0, i), 'vertex', 'sw')
        board.add_adjacency((7, i), (7, i+4), 'vertex', 'ne')
        board.add_adjacency((7, i), (7, i+4), 'vertex', 'nw')
        board.add_adjacency((7, i+4), (7, i), 'vertex', 'ne')
        board.add_adjacency((7, i+4), (7, i), 'vertex', 'nw')

    board.set_node_piece((4, 4), Piece('bishop', 'white', 'n'))

    renderer = SquareGraphRenderEngine(board)
    # board.visualize_graph_board('vertex')
    renderer.initialize((800, 600))

    plt.show()
