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

    # board = gp.corner_board(None, 'red', (0, 0))
    # board2 = gp.corner_board('red', 'blue', (0, 7), tint1=(0.85, 0.85, 0.85), tint2=(0.95, 0.95, 0.95))
    # board3 = gp.corner_board('blue', None, (0, 14), tint1=(0.65, 0.65, 0.65), tint2=(0.75, 0.75, 0.75))
    # board4 = gp.corner_board(None, 'green', (7, 0))
    # board5 = gp.corner_board('green', 'yellow', (7, 7), tint1=(0.85, 0.85, 0.85), tint2=(0.95, 0.95, 0.95))
    # board6 = gp.corner_board('yellow', None, (7, 14), tint1=(0.65, 0.65, 0.65), tint2=(0.75, 0.75, 0.75))
    # board.combine_graphs(board2)
    # board.combine_graphs(board3)
    # board.combine_graphs(board4)
    # board.combine_graphs(board5)
    # board.combine_graphs(board6)



    # for i in range(7):
    #     board.add_adjacency((i, 0), (7, 14+i), 'edge', 'e', 'l') # red east edge
    #     board.add_adjacency( (7, 14+i), (i, 0), 'edge', 's', 'r') # red west edge

    #     board.add_adjacency((i, 7), (0, i), 'edge', 'e', 'l')
    #     board.add_adjacency((0, i), (i, 7), 'edge', 's', 'r')

    #     board.add_adjacency((i, 14), (0, 7+i), 'edge', 'e', 'l')
    #     board.add_adjacency((0, 7+i), (i, 14), 'edge', 's', 'r')

    #     board.add_adjacency((i+7, 0), (0, 14+i), 'edge', 'e', 'l')
    #     board.add_adjacency((0, 14+i), (i+7, 0), 'edge', 's', 'r')

    #     board.add_adjacency((i+7, 7), (7, i), 'edge', 'e', 'l')
    #     board.add_adjacency((7, i), (i+7, 7), 'edge', 's', 'r')

    #     board.add_adjacency((i+7, 14), (7, 7+i), 'edge', 'e', 'l')
    #     board.add_adjacency((7, 7+i), (i+7, 14), 'edge', 's', 'r')

    # for i in range(6):
    #     board.add_adjacency((i, 0), (7, 15+i), 'vertex', 'ne', 'l') # red se diagonal
    #     board.add_adjacency((7, 15+i), (i, 0), 'vertex', 'se', 'r') # red nw diagonal
    #     board.add_adjacency((7, 14+i), (i+1, 0), 'vertex', 'sw', 'r') # red sw diagonal
    #     board.add_adjacency((i+1, 0), (7, 14+i), 'vertex', 'se', 'l') # red ne diagonal

    #     board.add_adjacency((i, 7), (0, i+1), 'vertex', 'ne', 'l') # magenta sw diagonal
    #     board.add_adjacency((0, i+1), (i, 7), 'vertex', 'se', 'r') # magenta ne diagonal
    #     board.add_adjacency((0, i), (i+1, 7), 'vertex', 'sw', 'r') # magenta nw diagonal
    #     board.add_adjacency((i+1, 7), (0, i), 'vertex', 'se', 'l') # magenta se diagonal

    #     board.add_adjacency((i, 14), (0, 8+i), 'vertex', 'ne', 'l') # blue ne diagonal
    #     board.add_adjacency((0, 8+i), (i, 14), 'vertex', 'se', 'r') # blue sw diagonal
    #     board.add_adjacency((0, 7+i), (i+1, 14), 'vertex', 'sw', 'r') # blue se diagonal
    #     board.add_adjacency((i+1, 14), (0, 7+i), 'vertex', 'se', 'l') # blue nw diagonal


    #     board.add_adjacency((i+7, 0), (0, 15+i), 'vertex', 'ne', 'l') # red se diagonal
    #     board.add_adjacency((0, 15+i), (i+7, 0), 'vertex', 'se', 'r') # red nw diagonal
    #     board.add_adjacency((0, 14+i), (i+8, 0), 'vertex', 'sw', 'r') # red sw diagonal
    #     board.add_adjacency((i+8, 0), (0, 14+i), 'vertex', 'se', 'l') # red ne diagonal

    #     board.add_adjacency((i+7, 7), (7, i+1), 'vertex', 'ne', 'l') # magenta sw diagonal
    #     board.add_adjacency((7, i+1), (i+7, 7), 'vertex', 'se', 'r') # magenta ne diagonal
    #     board.add_adjacency((7, i), (i+8, 7), 'vertex', 'sw', 'r') # magenta nw diagonal
    #     board.add_adjacency((i+8, 7), (7, i), 'vertex', 'se', 'l') # magenta se diagonal

    #     board.add_adjacency((i+7, 14), (7, 8+i), 'vertex', 'ne', 'l') # blue ne diagonal
    #     board.add_adjacency((7, 8+i), (i+7, 14), 'vertex', 'se', 'r') # blue sw diagonal
    #     board.add_adjacency((7, 7+i), (i+8, 14), 'vertex', 'sw', 'r') # blue se diagonal
    #     board.add_adjacency((i+8, 14), (7, 7+i), 'vertex', 'se', 'l') # blue nw diagonal

    # board.add_adjacency((0, 0), (7, 0), 'vertex', 'se', 'b')
    # board.add_adjacency((0, 7), (7, 7), 'vertex', 'se', 'b')
    # board.add_adjacency((0, 14), (7, 14), 'vertex', 'se', 'b')
        
    # transforms = linear_nskew(6)

    # for i in range(7):
    #     for j in range(7):
    #         try:
    #             render_polygon = board.get_node((i, j)).render_polygon
    #             transformed_polygons = [tuple(apply_nskew(render_polygon[k], l, transforms) for k in range(len(render_polygon))) for l in range(6)]
    #             board.set_node_rendering((i, j), render_polygon=transformed_polygons[0], texture_size=4/9)
    #             board.set_node_rendering((i, j+7), render_polygon=transformed_polygons[1], texture_size=4/9)
    #             board.set_node_rendering((i, j+14), render_polygon=transformed_polygons[2], texture_size=4/9)
    #             board.set_node_rendering((i+7, j), render_polygon=transformed_polygons[3], texture_size=4/9)
    #             board.set_node_rendering((i+7, j+7), render_polygon=transformed_polygons[4], texture_size=4/9)
    #             board.set_node_rendering((i+7, j+14), render_polygon=transformed_polygons[5], texture_size=4/9)
    #         except:
    #             continue
    
    # rpr = [(6, i) for i in range(4)] + [(i+7, 20) for i in range(4)]
    # mpr = [(6, i+7) for i in range(4)] + [(i, 6) for i in range(4)]
    # bpr = [(6, 14+i) for i in range(4)] + [(i, 13) for i in range(4)]
    # cpr = [(13, i) for i in range(4)] + [(i, 20) for i in range(4)]
    # gpr = [(13, i+7) for i in range(4)] + [(i+7, 6) for i in range(4)]
    # ypr = [(13, i+14) for i in range(4)] + [(i+7, 13) for i in range(4)]

    # rule_engine = GraphRuleEngine(teams=Team.team_dict(
    #     Team('red', color=(1.0, 0.0, 0.0)),
    #     Team('blue', color=(0.0, 0.0, 1.0)),
    #     Team('green', color=(0.0, 1.0, 0.0)),
    #     Team('yellow', color=(1.0, 1.0, 0.0))
    # ), promotion_tiles={
    #     'red': bpr+gpr+ypr,
    #     'blue': mpr+gpr+ypr,
    #     'green': mpr+bpr+ypr,
    #     'yellow': mpr+bpr+gpr
    # })

    renderer = Variants.load('cube/3cube_2player')

    renderer.initialize((800, 800), 1.0)

    plt.show()
