import sys
from graph_board import GraphBoard, DirectionGraph, GraphPresets as gp
from nodes import DirectionNode
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

    # def sumt(a, b):
    #     return tuple(map(sum, zip(a, b)))
    
    # def scalet(a, s):
    #     return tuple(x*s for x in a)

    # def linear_transform(X, y, x):
    #     shift_x = (X[0] + 1/2)
    #     shift_y = (X[1] - 1/2)
    #     tuple = sumt(scalet(x, shift_x), scalet(y, -shift_y))
    #     return (tuple[0], tuple[1], X[2])

    # def linear_nskew(n):
    #     transforms = [(-math.sin(2*math.pi*i/n), math.cos(2*math.pi*i/n)) for i in range(n)]
    #     return transforms
    
    # def apply_nskew(X, i, transforms):
    #     x = transforms[i]
    #     y = transforms[(i+1)%len(transforms)]
    #     return linear_transform(X, x, y)

    # board = gp.corner_board('white', 'red', (0, 0))
    # board2 = gp.corner_board('red', 'black', (0, 7))
    # board3 = gp.corner_board('black', 'white', (0, 14))
    # board.combine_graphs(board2)
    # board.combine_graphs(board3)



    # for i in range(7):
    #     board.add_adjacency((i, 0), (0, 14+i), 'edge', 'e', 'l')
    #     board.add_adjacency( (0, 14+i), (i, 0), 'edge', 's', 'r')

    #     board.add_adjacency((i, 7), (0, i), 'edge', 'e', 'l')
    #     board.add_adjacency((0, i), (i, 7), 'edge', 's', 'r')

    #     board.add_adjacency((i, 14), (0, 7+i), 'edge', 'e', 'l')
    #     board.add_adjacency((0, 7+i), (i, 14), 'edge', 's', 'r')

    # for i in range(6):
    #     board.add_adjacency((i, 0), (0, 15+i), 'vertex', 'ne', 'l') # white se diagonal
    #     board.add_adjacency((0, 15+i), (i, 0), 'vertex', 'se', 'r') # white nw diagonal
    #     board.add_adjacency((0, 14+i), (i+1, 0), 'vertex', 'sw', 'r') # white sw diagonal
    #     board.add_adjacency((i+1, 0), (0, 14+i), 'vertex', 'se', 'l') # white ne diagonal

    #     board.add_adjacency((i, 7), (0, i+1), 'vertex', 'ne', 'l') # red sw diagonal
    #     board.add_adjacency((0, i+1), (i, 7), 'vertex', 'se', 'r') # red ne diagonal
    #     board.add_adjacency((0, i), (i+1, 7), 'vertex', 'sw', 'r') # red nw diagonal
    #     board.add_adjacency((i+1, 7), (0, i), 'vertex', 'se', 'l') # red se diagonal

    #     board.add_adjacency((i, 14), (0, 8+i), 'vertex', 'ne', 'l') # black ne diagonal
    #     board.add_adjacency((0, 8+i), (i, 14), 'vertex', 'se', 'r') # black sw diagonal
    #     board.add_adjacency((0, 7+i), (i+1, 14), 'vertex', 'sw', 'r') # black se diagonal
    #     board.add_adjacency((i+1, 14), (0, 7+i), 'vertex', 'se', 'l') # black nw diagonal
        
    # transforms = linear_nskew(3)

    # for i in range(7):
    #     for j in range(7):
    #         try:
    #             render_polygon = board.get_node((i, j)).render_polygon
    #             transformed_polygons = [tuple(apply_nskew(render_polygon[k], l, transforms) for k in range(len(render_polygon))) for l in range(3)]
    #             board.set_node_rendering((i, j), render_polygon=transformed_polygons[0], texture_size=4/9)
    #             board.set_node_rendering((i, j+7), render_polygon=transformed_polygons[1], texture_size=4/9)
    #             board.set_node_rendering((i, j+14), render_polygon=transformed_polygons[2], texture_size=4/9)
    #         except:
    #             continue
    
    # for i in range(3,7):
    #     for j in range(4):
    #         if (i + j) % 2 == 0:
    #             tint = (0.9, 0.9, 0.9)
    #         else:
    #             tint = (0.7, 0.7, 0.7)
    #         board.get_node_tile((i, j)).tint = tint
    
    # for i, j in [(0,0), (1,0), (1,1), (2,0), (2,1), (2,2)]:
    #     if (i + j) % 2 == 0:
    #         tint = (0.9, 0.9, 0.9)
    #     else:
    #         tint = (0.7, 0.7, 0.7)
    #     board.get_node_tile((i, j)).tint = tint

    # for i in range(3, 7):
    #     for j in range(14, 18):
    #         if (i + j) % 2 == 0:
    #             tint = (0.7, 0.7, 0.7)
    #         else:
    #             tint = (0.8, 0.8, 0.8)
    #         board.get_node_tile((i, j)).tint = tint

    # for i in range(4):
    #     for j in range(10, 14):
    #         if (i + j) % 2 == 0:
    #             tint = (0.7, 0.7, 0.7)
    #         else:
    #             tint = (0.8, 0.8, 0.8)
    #         board.get_node_tile((i, j)).tint = tint

    # for i, j in [(0, 9), (0, 7), (1, 8), (2, 9), (2, 15), (1, 14)]:
    #     board.get_node_tile((i, j)).tint = (0.8, 0.8, 0.8)

    # for i in range(4):
    #     for j in range(3, 7):
    #         if (i + j) % 2 == 0:
    #             tint = (0.9, 0.9, 0.9)
    #         else:
    #             tint = (0.8, 0.8, 0.8)
    #         board.get_node_tile((i, j)).tint = tint

    # for i, j in [(0, 1), (0, 2), (1, 2), (1, 7), (2, 7), (2, 8)]:
    #     if (i + j) % 2 == 0:
    #         tint = (0.9, 0.9, 0.9)
    #     else:
    #         tint = (0.8, 0.8, 0.8)
    #     board.get_node_tile((i, j)).tint = tint

    # for i in range(3, 7):
    #     for j in range(7, 11):
    #         if (i + j) % 2 == 0:
    #             tint = (0.9, 0.9, 0.9)
    #         else:
    #             tint = (0.8, 0.8, 0.8)
    #         board.get_node_tile((i, j)).tint = tint

    
    # white_promotion = [(6, i) for i in range(4)] + [(i, 20) for i in range(4)]
    # red_promotion = [(6, i+7) for i in range(4)] + [(i, 6) for i in range(4)]
    # black_promotion = [(6, 14+i) for i in range(4)] + [(i, 13) for i in range(4)]

    # right = 'lambda board, position, team, teams: position in ([(i, 0) for i in range(7)] + [(i, 7) for i in range(7)] + [(i, 14) for i in range(7)])'
    # facing_west = ' and board.get_node_piece(position).facing == "e"'
    # left = 'lambda board, position, team, teams: position in ([(0, 14+i) for i in range(7)] + [(0, i) for i in range(7)] + [(0, 7+i) for i in range(7)])'
    # facing_north = ' and board.get_node_piece(position).facing == "s"'


    # PAWN_CAPTURE_LEFT = Moveset([Move(('fr', 'vertex'))], 1, False, True)
    # PAWN_CAPTURE_RIGHT = Moveset([Move(('fl', 'vertex'))], 1, False, True)

    # PAWN_CAPTURE_LEFT_OE = Moveset([Move(('fr', 'vertex'), end_direction='r')], 1, False, True)
    # PAWN_CAPTURE_RIGHT_OE = Moveset([Move(('fl', 'vertex'), end_direction='l')], 1, False, True)

    # PAWN_CAPTURE_RIGHT.add_condition(right, PAWN_CAPTURE_RIGHT_OE)
    # PAWN_CAPTURE_LEFT.add_condition(left, PAWN_CAPTURE_LEFT_OE)

    # PAWN_MOVE_ORE = Moveset([Move(('f', 'edge'), end_direction='l')], 1, True, False)
    # PAWN_MOVE_OLE = Moveset([Move(('f', 'edge'), end_direction='r')], 1, True, False)

    # mp.PAWN_MOVE.add_condition(right + facing_west, PAWN_MOVE_ORE).add_condition(left + facing_north, PAWN_MOVE_OLE)

    # rule_engine = GraphRuleEngine(rulesets=RuleSet.rule_dict(
    #     RuleSet('pawn', 10, [mp.PAWN_MOVE, PAWN_CAPTURE_LEFT, PAWN_CAPTURE_RIGHT], 'queen')
    # ), teams=Team.team_dict(tp.WHITE, tp.RED, tp.BLACK), promotion_tiles={
    #     'white': red_promotion+black_promotion,
    #     'red': black_promotion+white_promotion,
    #     'black': white_promotion+red_promotion
    # })

    renderer = Variants.load('cube/3player')

    renderer.initialize((800, 800), 1.0)

    plt.show()
