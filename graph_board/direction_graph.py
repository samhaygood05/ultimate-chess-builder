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

from nodes import DirectionNode

class DirectionGraph:
    def __init__(self, included_adjacency_types=None):
        self.nodes = dict()
        self.relations = dict()
        if included_adjacency_types == None:
            self.included_adjacency_types = ['edge', 'vertex']
        else:
            self.included_adjacency_types = included_adjacency_types

    def add_node(self, node: DirectionNode):
        self.nodes[node.direction] = node

    def add_relation(self, node1: str, node2: str, relative_direction):
        self.relations[(node1, node2)] = relative_direction
        self.nodes[node1].adjacencies[relative_direction] = self.nodes[node2]

    def get_direction_from_relative(self, node1: str, relative_direction):
        return self.nodes[node1].adjacencies[relative_direction].direction
    
    def get_opposite_direction(self, direction):
        return self.get_direction_from_relative(direction, 'b')
    
class DirectionPresets:
    def cartesian_2d():
        directions = DirectionGraph()
        cardinal_directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        relative_directions = ['f', 'fr', 'r', 'br', 'b', 'bl', 'l', 'fl']
        for direction in cardinal_directions:
            directions.add_node(DirectionNode(direction))

        for direction_index in range(len(cardinal_directions)):
            for relative_direction_index in range(len(relative_directions)):
                directions.add_relation(
                    cardinal_directions[direction_index], 
                    cardinal_directions[(direction_index + relative_direction_index) % len(cardinal_directions)], 
                    relative_directions[relative_direction_index])

        return directions

    def hexagonal_2d():
        directions = DirectionGraph()
        ordinal_directions  = ['n', 'nne', 'ne', 'e', 'se', 'sse', 's', 'ssw', 'sw', 'w', 'nw', 'nnw']
        relative_directions = ['f', 'ffr', 'fr', 'r', 'br', 'bbr', 'b', 'bbl', 'bl', 'l', 'fl', 'ffl']
        for direction in ordinal_directions:
            directions.add_node(DirectionNode(direction))

        for direction_index in range(len(ordinal_directions)):
            for relative_direction_index in range(len(relative_directions)):
                directions.add_relation(
                    ordinal_directions[direction_index], 
                    ordinal_directions[(direction_index + relative_direction_index) % len(ordinal_directions)], 
                    relative_directions[relative_direction_index])
                
        return directions