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

    def add_node(self, position, tile: Tile=None):
        node = TileNode(position, tile)
        self.nodes[position] = node
        if tile != None and tile.piece != None and tile.piece.is_royal:
            for team in tile.piece.get_team_names():
                if team not in self.royal_tiles:
                    self.royal_tiles[team] = []
                self.royal_tiles[team].append(position)

        if tile != None and tile.texture not in self.tile_textures:
            self.tile_textures.append(tile.texture)


    def add_adjacency(self, position1, position2, adjacency_type, direction):
        if adjacency_type not in self.adjacency_graphs.keys():
            self.adjacency_graphs[adjacency_type] = dict()
        if adjacency_type not in self.nodes[position1].adjacencies.keys():
            self.nodes[position1].adjacencies[adjacency_type] = dict()
        self.nodes[position1].adjacencies[adjacency_type][direction] = (self.nodes[position2], position2)
        self.adjacency_graphs[adjacency_type][(position1, position2)] = (self.nodes[position1], self.nodes[position2])

    def remove_adjacency(self, position1, position2, adjacency_type, direction):
        self.nodes[position1].adjacencies[adjacency_type].pop(direction)
        self.adjacency_graphs[adjacency_type].pop((position1, position2))

    def get_node_adjacencies(self, position, adjacency_type):
        position = position
        adjacency_type = adjacency_type
        if adjacency_type not in self.nodes[position].adjacencies.keys():
            return dict()
        return self.nodes[position].adjacencies[adjacency_type]

    def get_node(self, position):
        return self.nodes[position]
    
    def copy(self):
        new_board = GraphBoard(self.adjacency_graphs.keys(), self.directions, self.current_team_index)
        for position, node in self.nodes.items():
            new_board.add_node(position, node.tile)
            new_board.get_node(position).adjacencies = node.adjacencies

        new_board.adjacency_graphs = self.adjacency_graphs
        return new_board
    
    def get_node_tile(self, position) -> Tile:
        return self.nodes[position].tile
    
    def set_node_tile(self, position, tile):
        self.nodes[position].tile = tile

    def get_node_piece(self, position) -> Piece:
        if self.nodes[position].tile == None:
            return None
        return self.nodes[position].tile.piece
    
    def set_node_piece(self, position, piece):
        self.nodes[position].tile.piece = piece
    
    def get_node_type(self, position):
        if self.nodes[position].tile == None:
            return None
        return self.nodes[position].tile.type

    def __str__(self) -> str:
        return f'GraphBoard({self.nodes}, {self.edges})'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def visualize_graph_board(self, adjacency='edge'):
        edge_graph = nx.DiGraph()

        for position, node in self.nodes.items():
            edge_graph.add_node(position)
            for neightbor_direction, neighbor_position in node.adjacencies[adjacency].values():
                edge_graph.add_edge(position, neighbor_position)

        edge_pos = nx.kamada_kawai_layout(edge_graph)

        nx.draw(edge_graph, edge_pos, with_labels=True, node_size=400, font_size=10, node_color="skyblue", font_color="black")
        plt.title(f'{adjacency} adjacency graph')

        plt.show()


class GraphPresets:

    def create_empty_rectangular_grid(i, j) -> GraphBoard:
        board = GraphBoard()

        # Add nodes for each position on the ixj grid
        for row in range(i):
            for col in range(j):
                position = (row, col)
                board.add_node(position, Tile())

        # Add edges between neighboring nodes
        for row in range(i):
            for col in range(j):
                position = (row, col)

                # Neighboring positions
                north = (row + 1, col)
                northeast = (row + 1, col - 1)
                east = (row, col - 1)
                southeast = (row - 1, col - 1)
                south = (row - 1, col)
                southwest = (row - 1, col + 1)
                west = (row, col + 1)
                northwest = (row + 1, col + 1)

                # Add edges if neighbors are within the grid
                if north[0] in range(i):
                    board.add_adjacency(position, north, 'edge', 'n')
                if east[1] in range(j):
                    board.add_adjacency(position, east, 'edge', 'e')
                if south[0] in range(i):
                    board.add_adjacency(position, south, 'edge', 's')
                if west[1] in range(j):
                    board.add_adjacency(position, west, 'edge', 'w')
                if northeast[0] in range(i) and northeast[1] in range(j):
                    board.add_adjacency(position, northeast, 'vertex', 'ne')
                if southeast[0] in range(i) and southeast[1] in range(j):
                    board.add_adjacency(position, southeast, 'vertex', 'se')
                if southwest[0] in range(i) and southwest[1] in range(j):
                    board.add_adjacency(position, southwest, 'vertex', 'sw')
                if northwest[0] in range(i) and northwest[1] in range(j):
                    board.add_adjacency(position, northwest, 'vertex', 'nw')

        return board
    
    def create_standard_board(team1 = 'white', team2 = 'black', distance = 4) -> GraphBoard:
        # Create empty board
        board = GraphPresets.create_empty_rectangular_grid(4+distance, 8)

        # Add Team1 Pieces
        first_row = [Tile(Piece('rook', team1, facing='n')), Tile(Piece('knight', team1, facing='n')), Tile(Piece('bishop', team1, facing='n')), Tile(Piece('queen', team1, facing='n')), Tile(Piece('king', team1, facing='n')), Tile(Piece('bishop', team1, facing='n')), Tile(Piece('knight', team1, facing='n')), Tile(Piece('rook', team1, facing='n'))]
        second_row = [Tile(Piece('pawn', team1, facing='n')) for i in range(8)]
        for i in range(8):
            board.set_node_tile((0, i), first_row[i])
            board.set_node_tile((1, i), second_row[i])

        # Add Team2 Pieces
        last_row = [Tile(Piece('rook', team2, facing='s')), Tile(Piece('knight', team2, facing='s')), Tile(Piece('bishop', team2, facing='s')), Tile(Piece('queen', team2, facing='s')), Tile(Piece('king', team2, facing='s')), Tile(Piece('bishop', team2, facing='s')), Tile(Piece('knight', team2, facing='s')), Tile(Piece('rook', team2, facing='s'))]
        second_last_row = [Tile(Piece('pawn', team2, facing='s')) for i in range(8)]
        for i in range(8):
            board.set_node_tile((3+distance, i), last_row[i])
            board.set_node_tile((2+distance, i), second_last_row[i])

        return board
    
    def create_empty_hexagonal_grid(i, j, k) -> GraphBoard:
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
                        board.add_node(dx)

        for position in board.nodes:
            edge_neighbors = [
                (add(position, dq), '+q'),
                (add(position, dr), '+r'),
                (add(position, ds), '+s'),
                (add(position, ndq), '-q'),
                (add(position, ndr), '-r'),
                (add(position, nds), '-s')
            ]
            vertex_neighbors = [
                (add(add(position, dq), ndr), '+q-r'),
                (add(add(position, dr), nds), '+r-s'),
                (add(add(position, ds), ndq), '+s-q'),
                (add(add(position, ndq), dr), '-q+r'),
                (add(add(position, ndr), ds), '-r+s'),
                (add(add(position, nds), dq), '-s+q')
            ]
            for neighbor in edge_neighbors:
                if neighbor in board.nodes:
                    board.add_adjacency(position, neighbor[0], 'edge', neighbor[1])

            for neighbor in vertex_neighbors:
                if neighbor in board.nodes:
                    board.add_adjacency(position, neighbor[0], 'vertex', neighbor[1])
        
        return board
