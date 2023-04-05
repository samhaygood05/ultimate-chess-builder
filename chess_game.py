from graph_board import GraphBoard, GraphPresets as gp
from render_engines import *
from rule_engines import GraphRuleEngine
from movement import RuleSet, RulePresets as rp, MovesetPresets as mp
from teams import Team, TeamPresets as tp
from piece import Piece
from variants import Variants
import pygame
import matplotlib.pyplot as plt
import math

if __name__ == "__main__":
    pygame.init()

    # board = gp.create_half_board()
    # board2 = gp.create_half_board('black', (4, 0))
    # board3 = gp.create_half_board('red', (8, 0))

    # board.combine_graphs(board2)
    # board.combine_graphs(board3)

    # rule_engine = GraphRuleEngine(teams=Team.team_dict(tp.WHITE, tp.RED, tp.BLACK), 
    #                               promotion_tiles={'white': [(4, i) for i in range(8)] + [(8, i) for i in range(8)], 
    #                                                'red': [(4, i) for i in range(8)] + [(0, i) for i in range(8)],
    #                                                 'black': [(0, i) for i in range(8)] + [(8, i) for i in range(8)]
    #                                                }, turn_order=['white'])

    # for i in range(4):
    #     # Link White and Black Edges
    #     board.add_adjacency((3, i+4), (7, 3-i), 'edge', 'n', 'b')
    #     board.add_adjacency((7, 3-i), (3, i+4), 'edge', 'n', 'b')

    #     # Link White and Red Edges
    #     board.add_adjacency((11, i+4), (3, 3-i), 'edge', 'n', 'b')
    #     board.add_adjacency((3, 3-i), (11, i+4), 'edge', 'n', 'b')

    #     # Link Red and Black Edges
    #     board.add_adjacency((7, i+4), (11, 3-i), 'edge', 'n', 'b')
    #     board.add_adjacency((11, 3-i), (7, i+4), 'edge', 'n', 'b')

    # for i in range(4):
    #     # Link White and Black Vertices
    #     board.add_adjacency((3, i+3), (7, 3-i), 'vertex', 'nw', 'b')
    #     board.add_adjacency((7, 3-i), (3, i+3), 'vertex', 'nw', 'b')
    #     board.add_adjacency((3, i+4), (7, 4-i), 'vertex', 'ne', 'b')
    #     board.add_adjacency((7, 4-i), (3, i+4), 'vertex', 'ne', 'b')

    #     # Link White and Red Vertices
    #     board.add_adjacency((11, i+3), (3, 3-i), 'vertex', 'nw', 'b')
    #     board.add_adjacency((3, 3-i), (11, i+3), 'vertex', 'nw', 'b')
    #     board.add_adjacency((11, i+4), (3, 4-i), 'vertex', 'ne', 'b')
    #     board.add_adjacency((3, 4-i), (11, i+4), 'vertex', 'ne', 'b')

    #     # Link Red and Black Vertices
    #     board.add_adjacency((7, i+3), (11, 3-i), 'vertex', 'nw', 'b')
    #     board.add_adjacency((11, 3-i), (7, i+3), 'vertex', 'nw', 'b')
    #     board.add_adjacency((7, i+4), (11, 4-i), 'vertex', 'ne', 'b')
    #     board.add_adjacency((11, 4-i), (7, i+4), 'vertex', 'ne', 'b')

    #     def position_base(t):
    #         return t/2 - (t/4)*(t/4)
        
    #     def position_board_segment(i, j):
    #         return (j, position_base(j) + i)
        
    #     def position_board_segment_shift_rot(i, j, s=(0,0), r=0):
    #         board_segment = position_board_segment(i, j+0.5)
    #         rotated_segment = (board_segment[0]*math.cos(math.radians(r)) - board_segment[1]*math.sin(math.radians(r)), 
    #                            board_segment[0]*math.sin(math.radians(r)) + board_segment[1]*math.cos(math.radians(r)))
    #         return (rotated_segment[0] + s[0], rotated_segment[1] + s[1])
        
    #     def board_segment_tangent_angle(i, j, s=(0,0), r=0):
    #         board_segment = position_board_segment_shift_rot(i, j, s, r)
    #         board_segment_delta = position_board_segment_shift_rot(i, j+0.1, s, r)
    #         return math.degrees(math.atan2(board_segment_delta[0] - board_segment[0], board_segment_delta[1] - board_segment[1]))
        
    #     for i in range(4):
    #         for j in range(8):
    #             position1 = position_board_segment_shift_rot(i, j)
    #             angle1 = board_segment_tangent_angle(i, j)
    #             board.set_node_rendering((i, j), (position1[1], position1[0]), angle1)

    #             p2s = position_board_segment_shift_rot(3, 8)
    #             position2 = position_board_segment_shift_rot(i, j, (-8*math.cos(math.radians(120)) - 0.365*p2s[0], 8*math.sin(math.radians(120)) + 1.95*p2s[1]), -120)
    #             angle2 = board_segment_tangent_angle(i, j, (-math.cos(math.radians(120)), math.sin(math.radians(120))), -120)
    #             board.set_node_rendering((i+8, j), (position2[1], position2[0]), angle2)

    #             position3 = position_board_segment_shift_rot(i, j, (11.1, 5.35), 120)
    #             angle3 = board_segment_tangent_angle(i, j, (8, 0), 120)
    #             board.set_node_rendering((i+4, j), (position3[1], position3[0]), angle3)

    # renderer = SquareGraphRenderEngine(board, rule_engine)
    renderer = Variants.load('3player_square')
    # board.visualize_graph_board('vertex')
    renderer.initialize((800, 600))

    plt.show()
