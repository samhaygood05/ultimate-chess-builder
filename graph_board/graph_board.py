'''
Copyright 2023 Sam A. Haygood

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from graph_board.direction_graph import DirectionGraph, DirectionPresets as dp
from nodes import TileNode
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from tile import Tile
from piece import Piece
import math


class GraphBoard:
    def __init__(self, adjacency_types: List[str]=None, directions: DirectionGraph=None, current_team_index=0):
        self.nodes: Dict[Any, TileNode] = dict()
        self.current_team_index = current_team_index
        self.royal_tiles = dict()
        if adjacency_types == None:
            self.adjacency_graphs = {'edge': dict(), 'vertex': dict()}
        else:
            self.adjacency_graphs = {adjacency : dict() for adjacency in adjacency_types}

        if directions == None:
            self.directions = dp.cartesian_2d()
        else:
            self.directions = directions

        self.tile_textures = []

    def get_direction_from_relative(self, forward_direction, relative_direction):
        return self.directions.get_direction_from_relative(forward_direction, relative_direction)

    def add_node(self, position, tile: Tile=None, tint=None, render_polygon=None, texture_quad=None, texture_size=1/2):
        if tint == None:
            tint = (0.9, 0.9, 0.9) if (position[0] + position[1]) % 2 == 0 else (0.7, 0.7, 0.7)
        tile.tint = tint
        node = TileNode(position, tile, render_polygon=render_polygon, texture_quad=texture_quad, texture_size=texture_size)
        self.nodes[position] = node
        if tile != None and tile.piece != None and tile.piece.is_royal:
            for team in tile.piece.get_team_names():
                if team not in self.royal_tiles:
                    self.royal_tiles[team] = []
                self.royal_tiles[team].append(position)

        if tile != None and tile.texture not in self.tile_textures:
            self.tile_textures.append(tile.texture)

    def combine_graphs(self, other_graph):
        # Combine the nodes from the other graph into this graph
        self.nodes.update(other_graph.nodes)
        
        # Combine adjacency graphs of each adjacency type from the other graph into this graph
        for adjacency_type, other_adjacency_graph in other_graph.adjacency_graphs.items():
            if adjacency_type not in self.adjacency_graphs:
                self.adjacency_graphs[adjacency_type] = dict()
            
            self.adjacency_graphs[adjacency_type].update(other_adjacency_graph)

        # Combine royal tiles from the other graph into this graph
        for team, other_royal_tiles in other_graph.royal_tiles.items():
            if team not in self.royal_tiles:
                self.royal_tiles[team] = []
            
            self.royal_tiles[team].extend(other_royal_tiles)

        # Combine tile textures from the other graph into this graph
        for texture in other_graph.tile_textures:
            if texture not in self.tile_textures:
                self.tile_textures.append(texture)

    def add_adjacency(self, position1, position2, adjacency_type, direction, change_direction_to='f'):
        if adjacency_type not in self.adjacency_graphs.keys():
            self.adjacency_graphs[adjacency_type] = dict()
        if adjacency_type not in self.nodes[position1].adjacencies.keys():
            self.nodes[position1].adjacencies[adjacency_type] = dict()
        if direction not in self.nodes[position1].adjacencies[adjacency_type].keys():
            self.nodes[position1].adjacencies[adjacency_type][direction] = []
        self.nodes[position1].adjacencies[adjacency_type][direction].append((self.nodes[position2], position2, change_direction_to))
        self.adjacency_graphs[adjacency_type][(position1, position2)] = (self.nodes[position1], self.nodes[position2])

    def remove_adjacency(self, position1, position2, adjacency_type, direction):
        self.nodes[position1].adjacencies[adjacency_type][direction].pop((self.nodes[position2], position2, 'f'))
        self.adjacency_graphs[adjacency_type].pop((position1, position2))

    def get_node_adjacencies(self, position, adjacency_type):
        position = position
        adjacency_type = adjacency_type
        if adjacency_type not in self.nodes[position].adjacencies.keys():
            return dict()
        return self.nodes[position].adjacencies[adjacency_type]

    def get_node(self, position):
        return self.nodes[position]
    
    def init_hull(self):
        points_set = []
        for node in self.nodes.values():
            polygon = node.render_polygon
            for vertex in polygon:
                points_set.append(vertex)

        points = list(set(points_set))

        def polygon_centroid(vertices):
            area = 0
            x_sum = 0
            y_sum = 0
            z_min = None
            for i in range(len(vertices)):
                j = (i + 1) % len(vertices)
                cross_product = vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
                area += cross_product
                x_sum += (vertices[i][0] + vertices[j][0]) * cross_product
                y_sum += (vertices[i][1] + vertices[j][1]) * cross_product
                if z_min == None:
                    z_min = vertices[i][2]
                else:
                    z_min = min(z_min, vertices[i][2])

            area *= 0.5
            x_centroid = x_sum / (6 * area)
            y_centroid = y_sum / (6 * area)

            return (x_centroid, y_centroid, z_min)

        def orientation(p, q, r):
            return (r[1] - p[1]) * (q[0] - p[0]) - (r[0] - p[0]) * (q[1] - p[1])

        def quickhull(points):
            if len(points) <= 1:
                return points

            def partition(points, a, b):
                return [p for p in points if orientation(a, b, p) > 0]

            def extend_hull(points, a, b):
                if not points:
                    return [b]

                c = max(points, key=lambda p: orientation(a, b, p))
                p1, p2 = partition(points, a, c), partition(points, c, b)
                return extend_hull(p1, a, c) + extend_hull(p2, c, b)

            a = min(points, key=lambda p: p[0])
            b = max(points, key=lambda p: p[0])
            p1, p2 = partition(points, a, b), partition(points, b, a)
            return [a] + extend_hull(p1, a, b) + [b] + extend_hull(p2, b, a)

        hull = quickhull(points)
        hull_tuple = tuple(hull)
        center = polygon_centroid(hull)

        return (hull_tuple, center)


    def copy(self):
        new_board = GraphBoard(self.adjacency_graphs.keys(), self.directions, self.current_team_index)
        for position, node in self.nodes.items():
            new_board.add_node(position, node.tile.copy(), node.tile.tint, node.render_polygon, node.texture_quad)
            new_board.get_node(position).adjacencies = node.adjacencies

        new_board.adjacency_graphs = self.adjacency_graphs
        for team in self.royal_tiles:
            if team not in new_board.royal_tiles:
                new_board.royal_tiles[team] = []
        return new_board
    
    def clear_pieces(self):
        for position in self.nodes.keys():
            self.get_node_tile(position).piece = None

    def get_node_tile(self, position) -> Tile:
        return self.nodes[position].tile
    
    def set_node_tile(self, position, tile, tint=None):
        if tint == None:
            tint = self.nodes[position].tile.tint
        tile.tint = tint
        self.nodes[position].tile = tile
        if tile != None and tile.piece != None and tile.piece.is_royal:
            for team in tile.piece.get_team_names():
                if team not in self.royal_tiles:
                    self.royal_tiles[team] = []
                self.royal_tiles[team].append(position)
        elif tile != None and tile.piece != None and not tile.piece.is_royal:
            for team in tile.piece.get_team_names():
                if team in self.royal_tiles:
                    try:
                        self.royal_tiles[team].remove(position)
                    except:
                        pass

        if tile != None and tile.texture not in self.tile_textures:
            self.tile_textures.append(tile.texture)

    def get_node_piece(self, position) -> Piece:
        if self.nodes[position].tile == None:
            return None
        return self.nodes[position].tile.piece

    def set_node_piece(self, position, piece):
        self.nodes[position].tile.piece = piece
        if piece != None and piece.is_royal:
            for team in piece.get_team_names():
                if team not in self.royal_tiles:
                    self.royal_tiles[team] = []
                if position not in self.royal_tiles[team]:
                    self.royal_tiles[team].append(position)
        else:
            for team in self.royal_tiles.keys():
                try:
                    self.royal_tiles[team].remove(position)
                except:
                    pass

    def get_piece_teams(self, position):
        piece = self.get_node_piece(position)
        if piece != None:
            return piece.get_team_names()
        return []

    def get_team_pieces(self, team):
        positions = []
        for position in self.nodes.keys():
            if team in self.get_piece_teams(position):
                positions.append(position)
        return positions
    
    def get_node_type(self, position):
        if self.nodes[position].tile == None:
            return None
        return self.nodes[position].tile.type
    
    def set_node_rendering(self, position, render_polygon=None, texture_quad=None, texture_size=1/2):
        if render_polygon != None:
            self.nodes[position].render_polygon = render_polygon
        if texture_quad != None:
            self.nodes[position].texture_quad = texture_quad
        elif render_polygon != None:
            def polygon_centroid(vertices):
                area = 0
                x_sum = 0
                y_sum = 0
                z_min = min(vertex[2] for vertex in vertices)
                for i in range(len(vertices)):
                    j = (i + 1) % len(vertices)
                    cross_product = vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
                    area += cross_product
                    x_sum += (vertices[i][0] + vertices[j][0]) * cross_product
                    y_sum += (vertices[i][1] + vertices[j][1]) * cross_product

                area *= 0.5
                x_centroid = x_sum / (6 * area)
                y_centroid = y_sum / (6 * area)

                return (x_centroid, y_centroid, z_min)
            center = polygon_centroid(render_polygon)
            self.nodes[position].texture_quad = (
                (center[0] - texture_size, center[1] - texture_size, center[2]),
                (center[0] + texture_size, center[1] - texture_size, center[2]),
                (center[0] + texture_size, center[1] + texture_size, center[2]),
                (center[0] - texture_size, center[1] + texture_size, center[2])
            )

    def clear_node_rendering(self):
        for position in self.nodes.keys():
            quad = (
                (position[1] - 1/2, -position[0] - 1/2, 0), 
                (position[1] + 1/2, -position[0] - 1/2, 0),
                (position[1] + 1/2, -position[0] + 1/2, 0),
                (position[1] - 1/2, -position[0] + 1/2, 0)
            )
            self.set_node_rendering(position, quad)

    def __str__(self) -> str:
        return f'GraphBoard({self.nodes}, {self.edges})'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def visualize_graph_board(self, adjacency='edge'):
        edge_graph = nx.DiGraph()

        for position, node in self.nodes.items():
            if adjacency not in node.adjacencies.keys():
                continue
            edge_graph.add_node(position)
            for edges in node.adjacencies[adjacency].values():
                for neightbor_direction, neighbor_position, change_direction in edges:
                    edge_graph.add_edge(position, neighbor_position)

        edge_pos = nx.kamada_kawai_layout(edge_graph)

        nx.draw(edge_graph, edge_pos, with_labels=True, node_size=400, font_size=10, node_color="skyblue", font_color="black")
        plt.title(f'{adjacency} adjacency graph')

        plt.show()


class GraphPresets:

    def empty_rectangular_grid(i, j, br=(0,0), tint1=(0.7, 0.7, 0.7), tint2=(0.9, 0.9, 0.9)) -> GraphBoard:
        board = GraphBoard()

        def shift(position_x, position_y):
            position = (position_x, position_y)
            if shift == (0, 0):
                return position
            return (position[0] + br[0], position[1] + br[1])

        # Add nodes for each position on the ixj grid
        for row in range(i):
            for col in range(j):
                position = shift(row, col)
                if (position[0] + position[1]) % 2 == 0:
                    tint = tint1
                else:
                    tint = tint2
                board.add_node(position, Tile(), tint)

        # Add edges between neighboring nodes
        for row in range(i):
            for col in range(j):
                position = shift(row, col)

                # Neighboring positions
                north = shift(row + 1, col)
                northeast = shift(row + 1, col - 1)
                east = shift(row, col - 1)
                southeast = shift(row - 1, col - 1)
                south = shift(row - 1, col)
                southwest = shift(row - 1, col + 1)
                west = shift(row, col + 1)
                northwest = shift(row + 1, col + 1)

                # Add edges if neighbors are within the grid
                if north[0] in range(br[0], br[0]+i):
                    board.add_adjacency(position, north, 'edge', 'n')
                if east[1] in range(br[1], br[1]+j):
                    board.add_adjacency(position, east, 'edge', 'e')
                if south[0] in range(br[0], br[0]+i):
                    board.add_adjacency(position, south, 'edge', 's')
                if west[1] in range(br[1], br[1]+j):
                    board.add_adjacency(position, west, 'edge', 'w')
                if northeast[0] in range(br[0], br[0]+i) and northeast[1] in range(br[1], br[1]+j):
                    board.add_adjacency(position, northeast, 'vertex', 'ne')
                if southeast[0] in range(br[0], br[0]+i) and southeast[1] in range(br[1], br[1]+j):
                    board.add_adjacency(position, southeast, 'vertex', 'se')
                if southwest[0] in range(br[0], br[0]+i) and southwest[1] in range(br[1], br[1]+j):
                    board.add_adjacency(position, southwest, 'vertex', 'sw')
                if northwest[0] in range(br[0], br[0]+i) and northwest[1] in range(br[1], br[1]+j):
                    board.add_adjacency(position, northwest, 'vertex', 'nw')

        return board
    
    def half_board(team = 'white', br=(0,0), i=2, tint1=(0.7, 0.7, 0.7), tint2=(0.9, 0.9, 0.9)) -> GraphBoard:
        board = GraphPresets.empty_rectangular_grid(2+i, 8, br, tint1, tint2)

        def shift(position_x, position_y):
            position = (position_x, position_y)
            if shift == (0, 0):
                return position
            return (position[0] + br[0], position[1] + br[1])


        # Add Team Pieces
        first_row = [Tile(Piece('rook', team, facing='n')), Tile(Piece('knight', team, facing='n')), Tile(Piece('bishop', team, facing='n')), Tile(Piece('queen', team, facing='n')), Tile(Piece('king', team, facing='n', is_royal=True)), Tile(Piece('bishop', team, facing='n')), Tile(Piece('knight', team, facing='n')), Tile(Piece('rook', team, facing='n'))]
        second_row = [Tile(Piece('pawn', team, facing='n')) for i in range(8)]
        for i in range(8):
            board.set_node_tile(shift(0, i), first_row[i])
            board.set_node_tile(shift(1, i), second_row[i])

        return board


    def corner_board(team1 = 'white', team2 = 'red', br=(0,0), tint1=(0.7, 0.7, 0.7), tint2=(0.9, 0.9, 0.9)):
        board = GraphPresets.empty_rectangular_grid(7, 4, br, tint1, tint2)
        board2 = GraphPresets.empty_rectangular_grid(4, 3, (br[0], br[1]+4), tint1, tint2)

        board.combine_graphs(board2)

        for i in range(4):
            board.add_adjacency((i+br[0], 3+br[1]), (i+br[0], 4+br[1]), 'edge', 'w')
            board.add_adjacency((i+br[0], 4+br[1]), (i+br[0], 3+br[1]), 'edge', 'e')
            board.add_adjacency((i+1+br[0], 3+br[1]), (i+br[0], 4+br[1]), 'vertex', 'sw')
            board.add_adjacency((i+br[0], 4+br[1]), (i+1+br[0], 3+br[1]), 'vertex', 'ne')
        
        for i in range(3):
            board.add_adjacency((i+br[0], 3+br[1]), (i+1+br[0], 4+br[1]), 'vertex', 'nw')
            board.add_adjacency((i+1+br[0], 4+br[1]), (i+br[0], 3+br[1]), 'vertex', 'se')

        for i in range(4):
            if team1:
                board.set_node_piece((5+br[0], i+br[1]), Piece('pawn', team1, 's'))
            if team2:
                board.set_node_piece((i+br[0], 5+br[1]), Piece('pawn', team2, 'e'))
        if team1:
            board.set_node_piece((6+br[0], 3+br[1]), Piece('rook', team1, 's'))
            board.set_node_piece((6+br[0], 2+br[1]), Piece('knight', team1, 's'))
            board.set_node_piece((6+br[0], 1+br[1]), Piece('bishop', team1, 's'))
            board.set_node_piece((6+br[0], 0+br[1]), Piece('queen', team1, 's'))

        if team2:
            board.set_node_piece((3+br[0], 6+br[1]), Piece('rook', team2, 'e'))
            board.set_node_piece((2+br[0], 6+br[1]), Piece('knight', team2, 'e'))
            board.set_node_piece((1+br[0], 6+br[1]), Piece('bishop', team2, 'e'))
            board.set_node_piece((0+br[0], 6+br[1]), Piece('king', team2, 'e', is_royal=True))

        return board

    def standard_board(team1 = 'white', team2 = 'black', distance = 4) -> GraphBoard:
        # Create empty board
        board = GraphPresets.empty_rectangular_grid(4+distance, 8)

        # Add Team1 Pieces
        first_row = [Tile(Piece('rook', team1, facing='n')), Tile(Piece('knight', team1, facing='n')), Tile(Piece('bishop', team1, facing='n')), Tile(Piece('queen', team1, facing='n')), Tile(Piece('king', team1, facing='n', is_royal=True)), Tile(Piece('bishop', team1, facing='n')), Tile(Piece('knight', team1, facing='n')), Tile(Piece('rook', team1, facing='n'))]
        second_row = [Tile(Piece('pawn', team1, facing='n')) for i in range(8)]
        for i in range(8):
            board.set_node_tile((0, i), first_row[i])
            board.set_node_tile((1, i), second_row[i])

        # Add Team2 Pieces
        last_row = [Tile(Piece('rook', team2, facing='s')), Tile(Piece('knight', team2, facing='s')), Tile(Piece('bishop', team2, facing='s')), Tile(Piece('queen', team2, facing='s')), Tile(Piece('king', team2, facing='s', is_royal=True)), Tile(Piece('bishop', team2, facing='s')), Tile(Piece('knight', team2, facing='s')), Tile(Piece('rook', team2, facing='s'))]
        second_last_row = [Tile(Piece('pawn', team2, facing='s')) for i in range(8)]
        for i in range(8):
            board.set_node_tile((3+distance, i), last_row[i])
            board.set_node_tile((2+distance, i), second_last_row[i])

        return board
    
    def empty_hexagonal_grid(i, j, k, tint1=(0.9, 0.9, 0.9), tint2=(0.8, 0.8, 0.8), tint3=(0.7, 0.7, 0.7)) -> GraphBoard:
        board = GraphBoard(directions=dp.hexagonal_2d())
        dq = (0 , -1, 1 )
        dr = (1 , 0 , -1)
        ds = (-1, 1 , 0 )

        ndq = (0 , 1 , -1)
        ndr = (-1, 0 , 1 )
        nds = (1 , -1, 0 )

        def add(position1, position2):
            return tuple(map(sum, zip(position1, position2)))
        
        def scale(position, scalar):
            return tuple(map(lambda x: x * scalar, position))

        def hexagon(i, j):
            x = 3/2 * j + 3/2 * i
            y = math.sqrt(3)/2.0 * j - math.sqrt(3)/2.0 * i
            angles = [60*k*math.pi/180 for k in range(6)]
            hexagon = [(x + math.cos(angle), -y - math.sin(angle), 0) for angle in angles]
            return hexagon
        size_x = i // 2
        size_y = j // 2
        size_z = k // 2
        
        if i % 2 == 0:
            x_mod = 0
        else:
            x_mod = 1

        if j % 2 == 0:
            y_mod = 0
        else:
            y_mod = 1

        if k % 2 == 0:
            z_mod = 0
        else:
            z_mod = 1

        # Add nodes for each position on the ixjxk grid
        for q in range(-size_x, size_x + x_mod):
            for r in range(-size_y, size_y + y_mod):
                for s in range(-size_z, size_z + z_mod):
                    dx = add(add(scale(dq, q), scale(dr, r)), scale(ds, s))
                    if dx not in board.nodes:
                        if (dx[0] - dx[1]) % 3 == 0:
                            color = tint1
                        elif (dx[0] - dx[1]) % 3 == 1:
                            color = tint2
                        else:
                            color = tint3
                        board.add_node(dx, Tile(), color, hexagon(dx[1], dx[2]))

        for position in board.nodes:
            edge_neighbors = [
                (add(position, dq), 'n'),
                (add(position, dr), 'se'),
                (add(position, ds), 'sw'),
                (add(position, ndq), 's'),
                (add(position, ndr), 'nw'),
                (add(position, nds), 'ne')
            ]
            vertex_neighbors = [
                (add(add(position, dq), ndr), 'nnw'),
                (add(add(position, dr), nds), 'e'),
                (add(add(position, ds), ndq), 'ssw'),
                (add(add(position, ndq), dr), 'sse'),
                (add(add(position, ndr), ds), 'w'),
                (add(add(position, nds), dq), 'nne')
            ]
            for neighbor in edge_neighbors:
                if neighbor[0] in board.nodes:
                    board.add_adjacency(position, neighbor[0], 'edge', neighbor[1])

            for neighbor in vertex_neighbors:
                if neighbor[0] in board.nodes:
                    board.add_adjacency(position, neighbor[0], 'vertex', neighbor[1])
        
        return board

    def empty_hexagonal_vertex_grid(i, j, k, tint1=(0.9, 0.9, 0.9), tint2=(0.8, 0.8, 0.8), tint3=(0.7, 0.7, 0.7)) -> GraphBoard:

        board = GraphBoard(directions=dp.hexagonal_2d())
        dq = (0 , -1, 1 )
        dr = (1 , 0 , -1)
        ds = (-1, 1 , 0 )

        ndq = (0 , 1 , -1)
        ndr = (-1, 0 , 1 )
        nds = (1 , -1, 0 )

        def add(position1, position2):
            return tuple(map(sum, zip(position1, position2)))
        
        def scale(position, scalar):
            return tuple(map(lambda x: x * scalar, position))

        def rot30(p):
            theta = math.radians(-30)
            return (p[0]*math.cos(theta) - p[1]*math.sin(theta), p[0]*math.sin(theta) + p[1]*math.cos(theta), 0)

        def hexagon(i, j):
            x = 3/2 * j + 3/2 * i
            y = math.sqrt(3)/2.0 * j - math.sqrt(3)/2.0 * i
            angles = [60*k*math.pi/180 for k in range(6)]
            hexagon = [(x + math.cos(angle), -y - math.sin(angle), 0) for angle in angles]
            hexagon = [rot30(vertex) for vertex in hexagon]
            return hexagon
        size_x = i // 2
        size_y = j // 2
        size_z = k // 2
        
        if i % 2 == 0:
            x_mod = 0
        else:
            x_mod = 1

        if j % 2 == 0:
            y_mod = 0
        else:
            y_mod = 1

        if k % 2 == 0:
            z_mod = 0
        else:
            z_mod = 1

        # Add nodes for each position on the ixjxk grid
        for q in range(-size_x, size_x + x_mod):
            for r in range(-size_y, size_y + y_mod):
                for s in range(-size_z, size_z + z_mod):
                    dx = add(add(scale(dq, q), scale(dr, r)), scale(ds, s))
                    if dx not in board.nodes:
                        if (dx[0] - dx[1]) % 3 == 0:
                            color = tint1
                        elif (dx[0] - dx[1]) % 3 == 1:
                            color = tint2
                        else:
                            color = tint3
                        board.add_node(dx, Tile(), color, hexagon(dx[1], dx[2]))

        for position in board.nodes:
            edge_neighbors = [
                (add(position, dq), 'n'),
                (add(position, dr), 'se'),
                (add(position, ds), 'sw'),
                (add(position, ndq), 's'),
                (add(position, ndr), 'nw'),
                (add(position, nds), 'ne')
            ]
            vertex_neighbors = [
                (add(add(position, dq), ndr), 'nnw'),
                (add(add(position, dr), nds), 'e'),
                (add(add(position, ds), ndq), 'ssw'),
                (add(add(position, ndq), dr), 'sse'),
                (add(add(position, ndr), ds), 'w'),
                (add(add(position, nds), dq), 'nne')
            ]
            for neighbor in edge_neighbors:
                if neighbor[0] in board.nodes:
                    board.add_adjacency(position, neighbor[0], 'edge', neighbor[1])

            for neighbor in vertex_neighbors:
                if neighbor[0] in board.nodes:
                    board.add_adjacency(position, neighbor[0], 'vertex', neighbor[1])
        
        return board