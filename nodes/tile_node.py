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
    def __init__(self, position, tile: Tile=None, adjacency_types=None, render_polygon=None, texture_quad=None, texture_size=1/2):
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

        if texture_quad == None:
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
                        z_min = min(vertices[i][2], z_min)

                area *= 0.5
                x_centroid = x_sum / (6 * area)
                y_centroid = y_sum / (6 * area)

                return (x_centroid, y_centroid, z_min)
            center = polygon_centroid(self.render_polygon)
            self.texture_quad = (
                (center[0] - texture_size, center[1] - texture_size, center[2]),
                (center[0] + texture_size, center[1] - texture_size, center[2]),
                (center[0] + texture_size, center[1] + texture_size, center[2]),
                (center[0] - texture_size, center[1] + texture_size, center[2])
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

    