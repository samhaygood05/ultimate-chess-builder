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

from piece import Piece

class Tile:
    def __init__(self, piece: Piece=None, type=None, tint=(1.0, 1.0, 1.0), texture=None, disallowed_pieces=None):
        self.piece = piece
        self.type = type
        self.tint = tint
        if texture == None:
            self.texture = type
        else:
            self.texture = texture
        if disallowed_pieces == None:
            self.disallowed_pieces = []
        else:
            self.disallowed_pieces = disallowed_pieces

    def copy(self):
        return Tile(self.piece, self.type, self.tint, self.texture, self.disallowed_pieces)

    def transfer_piece(self, start_tile):
        new_end = Tile(start_tile.piece.moved(), self.type)
        new_start = Tile(None, start_tile.type)
        return new_end, new_start

    def set_texture(self, texture):
        self.texture = texture

    def promote(self, promotion):
        self.piece.promote(promotion)
        return self