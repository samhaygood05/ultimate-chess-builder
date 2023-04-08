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

from tile import Tile

class TileNode:
    def __init__(self, position, tile: Tile=None, adjacency_types=None, render_polygon=None, texture_quad=None):
        self.position = position
        self.tile = tile
        if adjacency_types == None:
            self.adjacencies = {'edge': dict(), 'vertex': dict()}
        else:
            self.adjacencies = {adjacency : dict() for adjacency in adjacency_types}
        if render_polygon == None:
            self.render_polygon = (
                (position[1] - 1/2, -position[0] - 1/2, 0), 
                (position[1] + 1/2, -position[0] - 1/2, 0),
                (position[1] + 1/2, -position[0] + 1/2, 0),
                (position[1] - 1/2, -position[0] + 1/2, 0)
            )
        else:
            self.render_polygon = render_polygon

        if texture_quad == None or len(texture_quad) != 4:
            center = (
                sum(polygon[0] for polygon in self.render_polygon)/len(self.render_polygon), 
                sum(polygon[1] for polygon in self.render_polygon)/len(self.render_polygon), 
                sum(polygon[2] for polygon in self.render_polygon)/len(self.render_polygon)
            )
            self.texture_quad = (
                (center[0] - 1/2, center[1] - 1/2, center[2]),
                (center[0] + 1/2, center[1] - 1/2, center[2]),
                (center[0] + 1/2, center[1] + 1/2, center[2]),
                (center[0] - 1/2, center[1] + 1/2, center[2])
            )
        else:
            self.texture_quad = texture_quad

    def set_piece(self, piece):
        self.tile.piece = piece

    def set_tile(self, tile):
        self.tile = tile

    def copy(self):
        copy = TileNode(self.position, self.tile.copy(), self.adjacencies.keys())
        copy.adjacencies = self.adjacencies
        return copy

    def __str__(self) -> str:
        return f'Node({self.position}, {self.tile})'
    
    def __repr__(self) -> str:
        return self.__str__()

    