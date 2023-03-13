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

from render_engines.abstract_render_engine import AbstractRenderEngine
from rule_engines.square_rule_engine import SquareRuleEngine as RuleEngine
from boards.square_board import SquareBoard as Board
import pygame
from PIL import Image
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import colorsys

class SquareRenderEngine(AbstractRenderEngine):
    def __init__(self, screen_size, board: Board = None, rule_engine: RuleEngine = None, illegal_moves=False, render_on_init=True):
        if board == None:
            self.board = Board()
        else:
            self.board = board
        if rule_engine == None:
            self.rule_engine = RuleEngine()
        else:
            self.rule_engine = rule_engine

        self.illegal_moves = illegal_moves

        if render_on_init:
            pygame.init()
            self.display = screen_size
            pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)
            self.screen_ratio = self.display[0]/self.display[1]
            self.zoom = 1.0

            rows = len(self.board.board) / 20
            columns = len(self.board.board[0]) / 20

            gluOrtho2D(-self.zoom, self.zoom, -self.zoom/self.screen_ratio, self.zoom/self.screen_ratio)
            glRotatef(180, 1, 0, 0)
            self.camera_pos = [-columns, -rows, 0.5]
            self.main_loop()
    
    def draw_board(self, highlight_tiles=None, selected_tile='', hover_tile='', x=0, y=0, z=0):
        rows = len(self.board.board)
        columns = len(self.board.board[0])

        current_team = self.rule_engine.teams[self.board.current_team]

        if highlight_tiles == None:
            highlight_tiles = []

        if current_team.name == 'white':
            board_color = (0.8, 0.8, 0.8)
        elif current_team.name == 'black':
            board_color = (0.3, 0.3, 0.3)
        else:
            board_color = colorsys.hsv_to_rgb(current_team.hue/360.0, 0.5, 0.5)

        highlight_color=(1.0, 1.0, 0.0)
        selected_color=(1.0, 0.0, 0.0)
        hover_color=(0.0, 1.0, 1.0)
        hover_highlight_color=(0.0, 1.0, 0.0)
        tiles_highlight = [Board.tile_to_index(tile) for tile in highlight_tiles]
        if selected_tile != '':
            tile_selected = [Board.tile_to_index(selected_tile)]
        else:
            tile_selected = []
        if hover_tile != '':
            tile_hover = [Board.tile_to_index(hover_tile)]
        else:
            tile_hover = []

        square_size = 1 / 10
        outer_border_width = 0.3 * square_size # set the width of the border
        inner_border_width = 0.05 * square_size # set the width of the border
        board_width = columns * square_size
        board_height = rows * square_size


        # Draw the border rectangle
        glColor3f(0, 0, 0) # black
        glBegin(GL_QUADS)
        glVertex3f(x - outer_border_width - inner_border_width, y - outer_border_width - inner_border_width, z)
        glVertex3f(x + board_width + outer_border_width + inner_border_width, y - outer_border_width - inner_border_width, z)
        glVertex3f(x + board_width + outer_border_width + inner_border_width, y + board_height + outer_border_width + inner_border_width, z)
        glVertex3f(x - outer_border_width - inner_border_width, y + board_height + outer_border_width + inner_border_width, z)
        glEnd()

        # Draw the border rectangle
        glColor3f(*board_color) # black
        glBegin(GL_QUADS)
        glVertex3f(x - outer_border_width, y - outer_border_width, z)
        glVertex3f(x + board_width + outer_border_width, y - outer_border_width, z)
        glVertex3f(x + board_width + outer_border_width, y + board_height + outer_border_width, z)
        glVertex3f(x - outer_border_width, y + board_height + outer_border_width, z)
        glEnd()

        # Draw the border rectangle
        glColor3f(0, 0, 0) # black
        glBegin(GL_QUADS)
        glVertex3f(x - inner_border_width, y - inner_border_width, z)
        glVertex3f(x + board_width + inner_border_width, y - inner_border_width, z)
        glVertex3f(x + board_width + inner_border_width, y + board_height + inner_border_width, z)
        glVertex3f(x - inner_border_width, y + board_height + inner_border_width, z)
        glEnd()


        quads = dict()
        # Draw the checkerboard
        for row in range(rows):
            for column in range(columns):
                if (row + column) % 2 == 0:
                    color = (0.9, 0.9, 0.9) # light gray
                else:
                    color = (0.7, 0.7, 0.7) # dark gray

                if (rows - 1 - row, column) in tiles_highlight and (rows - 1 - row, column) in tile_hover:
                    color = ((color[0] + hover_highlight_color[0])/2, (color[1] + hover_highlight_color[1])/2, (color[2] + hover_highlight_color[2])/2)
                elif (rows - 1 - row, column) in tiles_highlight:
                    color = ((color[0] + highlight_color[0])/2, (color[1] + highlight_color[1])/2, (color[2] + highlight_color[2])/2)
                elif (rows - 1 - row, column) in tile_selected:
                    color = ((color[0] + selected_color[0])/2, (color[1] + selected_color[1])/2, (color[2] + selected_color[2])/2)
                elif (rows - 1 - row, column) in tile_hover:
                    color = ((color[0] + hover_color[0])/2, (color[1] + hover_color[1])/2, (color[2] + hover_color[2])/2)

                x_pos = x + column * square_size
                y_pos = y + row * square_size
                z_pos = z

                quad = ((x_pos, y_pos, 0), (x_pos + square_size, y_pos, 0), (x_pos + square_size, y_pos + square_size, 0), (x_pos, y_pos + square_size, 0))

                glBegin(GL_QUADS)
                glColor3fv(color)
                glVertex3fv((x_pos, y_pos, z_pos))
                glVertex3fv((x_pos + square_size, y_pos, z_pos))
                glVertex3fv((x_pos + square_size, y_pos + square_size, z_pos))
                glVertex3fv((x_pos, y_pos + square_size, z_pos))
                glEnd()

                tile_name = Board.index_to_tile(rows - 1 - row, column)

                quads[tile_name] = quad
        
        return quads

    def draw_pieces(self, x=0, y=0, z=0):
        rows = len(self.board.board)
        columns = len(self.board.board[0])

        square_size = 1 / 10

        for row in range(rows):
            for column in range(columns):
                tile = Board.index_to_tile(row, column)
                piece = self.board.get_tile(tile)
                if piece is None:
                    piece_path = f'images/blank.png'
                    piece_color = (0.0, 0.0, 0.0)
                elif piece.piece == 'empty':
                    continue
                else:
                    piece_path = piece.get_file_name()
                    if piece.team.name in ['white', 'black']:
                        piece_color = (1.0, 1.0, 1.0)
                    else:
                        piece_color = colorsys.hsv_to_rgb(self.rule_engine.teams[piece.team.name].hue/360.0, 1.0, 1.0)
                try:
                    with open(piece_path, "rb") as file:
                        img = Image.open(file).convert('RGBA')
                        piece_data = np.asarray(img, dtype=np.uint8)

                        x_pos = x + column * square_size
                        y_pos = y + (rows - row - 1) * square_size
                        z_pos = z - 0.01

                        texture_id = glGenTextures(1)
                        glColor3fv(piece_color)
                        glEnable(GL_BLEND);
                        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
                        glBindTexture(GL_TEXTURE_2D, texture_id)
                        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
                        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, piece_data)
                        glGenerateMipmap(GL_TEXTURE_2D)

                        glEnable(GL_TEXTURE_2D)
                        glBegin(GL_QUADS)
                        glTexCoord2f(0.0, 0.0)
                        glVertex3fv((x_pos, y_pos, z_pos))
                        glTexCoord2f(1.0, 0.0)
                        glVertex3fv((x_pos + square_size, y_pos, z_pos))
                        glTexCoord2f(1.0, 1.0)
                        glVertex3fv((x_pos + square_size, y_pos + square_size, z_pos))
                        glTexCoord2f(0.0, 1.0)
                        glVertex3fv((x_pos, y_pos + square_size, z_pos))
                        glEnd()
                        glDisable(GL_TEXTURE_2D)
                except FileNotFoundError:
                    pass
    
    def main_loop(self):

        hover_tile = ''
        selected_tile = ''
        while True:

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            gluOrtho2D(-self.zoom, self.zoom, -self.zoom/self.screen_ratio, self.zoom/self.screen_ratio)
            glRotatef(180, 1, 0, 0)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if selected_tile == '':
                            selected_tile = hover_tile
                        else:
                            self.board = self.rule_engine.play_move(self.board, selected_tile, hover_tile, self.illegal_moves)
                            selected_tile = ''
                    elif event.button == 3:
                        selected_tile = ''
                    elif event.button == 4 and self.zoom > 0.2:
                        self.zoom -= 1 * self.zoom
                    elif event.button == 5:
                        self.zoom += 1 * self.zoom

            keys = pygame.key.get_pressed()
            if (keys[pygame.K_w] or keys[pygame.K_UP]):
                self.camera_pos[1] += 0.3 * self.zoom / 5
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
                self.camera_pos[1] -= 0.3 * self.zoom / 5
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                self.camera_pos[0] += 0.3 * self.zoom / 5
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                self.camera_pos[0] -= 0.3 * self.zoom / 5
            if keys[pygame.K_e] and self.zoom > 0.2:
                self.zoom -= 0.5 * self.zoom / 10
            if keys[pygame.K_q]:
                self.zoom += 0.5 * self.zoom / 10

            if selected_tile != '':
                highlight_tiles = self.rule_engine.get_legal_moves(selected_tile, self.board)
            elif hover_tile != '':
                highlight_tiles = self.rule_engine.get_legal_moves(hover_tile, self.board)
            else: 
                highlight_tiles = []
            glClearColor(0.7, 0.8, 0.9, 1.0) # light blue-gray
            quads = self.draw_board(highlight_tiles, selected_tile, hover_tile, *self.camera_pos)
            self.draw_pieces(*self.camera_pos)
            pygame.display.flip()

            prjMat = (GLfloat * 16)()
            glGetFloatv(GL_PROJECTION_MATRIX, prjMat)
            
            mouse = pygame.mouse.get_pos()

            for tile, quad in quads.items():
                if SquareRenderEngine.TestRec(prjMat, mouse, self.display, self.zoom, quad):
                    hover_tile = tile
                    break
                else:
                    hover_tile = ''

            pygame.time.wait(10)


    def __str__(self) -> str:
        return f"Board: {self.board}\nRules: {self.rule_engine}"
