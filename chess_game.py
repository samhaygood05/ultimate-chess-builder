import sys
from graph_board import GraphBoard, DirectionGraph, GraphPresets as gp
from nodes import DirectionNode
from render_engines import *
from rule_engines import GraphRuleEngine
from movement import RuleSet, RulePresets as rp, Moveset, MovesetPresets as mp, Move
from board_builder_utils import BoardBuilderUtils as bbu
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

    board = gp.empty_rectangular_grid(18, 4, tint1=(0.9, 0.9, 0.9), tint2=(0.7, 0.7, 0.7))

    for i in range(4):
        board.add_adjacency((17, i), (10-i, 0), 'edge', 'n', 'l')
        board.add_adjacency((10-i, 0), (17, i), 'edge', 'e', 'r')

        board.add_adjacency((0, i), (10-i, 3), 'edge', 's', 'l')
        board.add_adjacency((10-i, 3), (0, i), 'edge', 'w', 'r')

    for i in range(3):
        board.add_adjacency((10-i, 3), (0, i+1), 'vertex', 'sw', 'r')
        board.add_adjacency((0, i+1), (10-i, 3), 'vertex', 'se', 'l')
        board.add_adjacency((9-i, 3), (0, i), 'vertex', 'nw', 'r')
        board.add_adjacency((0, i), (9-i, 3), 'vertex', 'sw', 'l')

        board.add_adjacency((10-i, 0), (17, i+1), 'vertex', 'se', 'r')
        board.add_adjacency((17, i+1), (10-i, 0), 'vertex', 'ne', 'l')
        board.add_adjacency((9-i, 0), (17, i), 'vertex', 'ne', 'r')
        board.add_adjacency((17, i), (9-i, 0), 'vertex', 'nw', 'l')

    board.add_adjacency((6, 3), (0, 3), 'vertex', 'nw', 'r')
    board.add_adjacency((0, 3), (6, 3), 'vertex', 'se', 'l')
    board.add_adjacency((11, 0), (17, 0), 'vertex', 'se', 'r')
    board.add_adjacency((17, 0), (11, 0), 'vertex', 'ne', 'l')


    def lower_loop(X):
        poly = (-math.cos(3/2 * math.pi * (5-X[0])/5), math.sin(3/2 * math.pi * (5-X[0])/5))
        poly = bbu.scalet(poly, 5-X[1])

        return (poly[0]+4.5, poly[1]-5.5, X[2])

    def upper_loop(X):
        poly = (math.cos(3/2 * math.pi * X[0]/5), -math.sin(3/2 * math.pi * X[0]/5))
        poly = bbu.scalet(poly, X[1]+1)

        return (poly[0]-1.5, poly[1]-11.5, X[2])

    def rot(X):
        s = math.sqrt(2)/2
        return (X[0]*s - X[1]*s, X[0]*s + X[1]*s, X[2])

    for i in range(5):
        for j in range(4):
            render_polygon = (
                (i, j, 0),
                (i+1/3, j, 0),
                (i+2/3, j, 0),
                (i+1, j,0),
                (i+1, j+1, 0),
                (i+2/3, j+1, 0),
                (i+1/3, j+1, 0),
                (i, j+1, 0)
            )

            lower_polygon = tuple(lower_loop(vertex) for vertex in render_polygon)
            board.set_node_rendering((i+1, j), lower_polygon)

            upper_polygon = tuple(upper_loop(vertex) for vertex in render_polygon)
            board.set_node_rendering((i+12, j), upper_polygon)

    for i in range(4):
        render_polygon = (
            (3.5, -6.5-i, 0),
            (3.5, -7.5-i, 0),
            (4.5, -7.5-i, 0),
            (4.5, -6.5-i, 0)
        )
        board.set_node_rendering((0, 3-i), render_polygon)
        render_polygon = (
            (-1.5, -10.5+i, 0),
            (-0.5, -10.5+i, 0),
            (-0.5, -9.5+i, 0),
            (-1.5, -9.5+i, 0)
        )
        board.set_node_rendering((17, i), render_polygon)

    for position in board.nodes.keys():
        render_polygon = board.get_node(position).render_polygon
        rot_poly = tuple(rot(vertex) for vertex in render_polygon)
        shift_poly = tuple(bbu.sumt(vertex, (0, 15, 0)) for vertex in rot_poly)
        board.set_node_rendering(position, shift_poly)


    for i in range(4):
        board.set_node_piece((2, i), Piece('pawn', 'white', 's'))
        board.set_node_piece((5, i), Piece('pawn', 'white'))

        board.set_node_piece((12, i), Piece('pawn', 'black', 's'))
        board.set_node_piece((15, i), Piece('pawn', 'black'))
    
    board.set_node_piece((4, 0), Piece('queen', 'white'))
    board.set_node_piece((3, 0), Piece('king', 'white', is_royal=True))

    board.set_node_piece((14, 3), Piece('queen', 'black'))
    board.set_node_piece((13, 3), Piece('king', 'black', is_royal=True))

    for i in range(2):
        board.set_node_piece((3+i, 1), Piece('bishop', 'white'))
        board.set_node_piece((3+i, 2), Piece('knight', 'white'))
        board.set_node_piece((3+i, 3), Piece('rook', 'white'))

        board.set_node_piece((13+i, 2), Piece('bishop', 'black'))
        board.set_node_piece((13+i, 1), Piece('knight', 'black'))
        board.set_node_piece((13+i, 0), Piece('rook', 'black'))

    condition = 'lambda board, position, team, teams:'
    right = 'position in [(7+i, 3) for i in range(4)]'
    left = 'position in [(7+i, 0) for i in range(4)]'
    front = 'position in [(10, i) for i in range(4)]'
    back = 'position in [(7, i) for i in range(4)]'
    center = 'position in [(7+i, j) for i in range(4) for j in range(4)]'

    north = 'board.get_node_piece(position).facing == "n"'
    south = 'board.get_node_piece(position).facing == "s"'
    east = 'board.get_node_piece(position).facing == "e"'
    west = 'board.get_node_piece(position).facing == "w"'

    white = '"white" in team'
    black = '"black" in team'

    def orc(*conditions):
        return ' or '.join(conditions)

    PAWN_CAPTURE_LEFT = Moveset([Move(('fr', 'vertex'))], 1, False, True, condition_requirement=f'{condition} not ({" and ".join([left, north, black])}) and not ({" and ".join([right, south, white])}) and not ({" and ".join([back, east, white])}) and not ({" and ".join([front, west, black])})')
    PAWN_CAPTURE_RIGHT = Moveset([Move(('fl', 'vertex'))], 1, False, True, condition_requirement=f'{condition} not ({" and ".join([right, north, white])}) and not ({" and ".join([left, south, black])}) and not ({" and ".join([front, east, black])}) and not ({" and ".join([back, west, white])})')

    PAWN_MOVE_LEFT = Moveset([Move(('r', 'edge'), end_direction='r')], 1, True, False, condition_requirement=f'{condition} {" and ".join([center, f"({orc(north, south)})"])}')
    PAWN_MOVE_RIGHT = Moveset([Move(('l', 'edge'), end_direction='l')], 1, True, False, condition_requirement=f'{condition} {" and ".join([center, f"({orc(east, west)})"])}')

    rule_eninge = GraphRuleEngine(RuleSet.rule_dict(
        RuleSet('pawn', 10, [mp.PAWN_MOVE, PAWN_MOVE_LEFT, PAWN_MOVE_RIGHT, PAWN_CAPTURE_LEFT, PAWN_CAPTURE_RIGHT], 'queen')
    ),
        promotion_tiles={
        'white': [(13, i) for i in range(4)] + [(14, i) for i in range(4)],
        'black': [(3, i) for i in range(4)] + [(4, i) for i in range(4)]
    })

    renderer = GraphRenderEngine(board, rule_eninge)

    print(board.get_node((14, 3)).render_polygon)

    renderer.initialize((800, 800), 1.0)

    plt.show()
