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

class SquareRenderEngine(AbstractRenderEngine):
    def __init__(self, screen_size, board: Board = None, rule_engine: RuleEngine = None):
        if board == None:
            self.board = Board()
        else:
            self.board = board
        if rule_engine == None:
            self.rule_engine = RuleEngine()
        else:
            self.rule_engine = rule_engine

        pygame.init()
        self.display = screen_size
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)

        gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 100.0)
        glTranslatef(0, 0, -2)  # move camera back along Z-axis
        glRotatef(180, 1, 0, 0)
        self.camera_pos = [0, 0, -2]
        self.main_loop()
    
    def draw_board(self, x=0, y=0):
        rows = len(self.board.board)
        columns = len(self.board.board[0])

        square_size = 1 / 10
        border_width = 0.3 * square_size # set the width of the border
        board_width = columns * square_size
        board_height = rows * square_size

        # Draw the border rectangle
        glColor3f(0.3, 0.3, 0.3) # black
        glBegin(GL_QUADS)
        glVertex3f(x - border_width, y - border_width, 0.0)
        glVertex3f(x + board_width + border_width, y - border_width, 0.0)
        glVertex3f(x + board_width + border_width, y + board_height + border_width, 0.0)
        glVertex3f(x - border_width, y + board_height + border_width, 0.0)
        glEnd()


        quads = []
        # Draw the checkerboard
        for row in range(rows):
            for column in range(columns):
                if (row + column) % 2 == 0:
                    color = (0.9, 0.9, 0.9) # light gray
                else:
                    color = (0.7, 0.7, 0.7) # dark gray

                x_pos = x + column * square_size
                y_pos = y + row * square_size

                glBegin(GL_QUADS)
                glColor3fv(color)
                glVertex3fv((x_pos, y_pos, 0))
                glVertex3fv((x_pos + square_size, y_pos, 0))
                glVertex3fv((x_pos + square_size, y_pos + square_size, 0))
                glVertex3fv((x_pos, y_pos + square_size, 0))
                glEnd()
                quads.append(((x_pos, y_pos, 0), (x_pos + square_size, y_pos, 0), (x_pos + square_size, y_pos + square_size, 0), (x_pos, y_pos + square_size, 0)))
        
        return tuple(quads)

    def highlight_tiles(self, tiles, screen, highlight_color=(255, 255, 0, 128), tile_size=90):
        pass

    def draw_pieces(self, x=0, y=0):
        rows = len(self.board.board)
        columns = len(self.board.board[0])

        square_size = 1 / 10

        for row in range(rows):
            for column in range(columns):
                tile = Board.index_to_tile(row, column)
                piece = self.board.get_tile(tile)
                if piece is None:
                    piece_path = f'images/blank.png'
                elif piece.piece is 'empty':
                    continue
                else:
                    piece_path = piece.get_file_name()
                try:
                    with open(piece_path, "rb") as file:
                        img = Image.open(file).convert('RGBA')
                        piece_data = np.asarray(img, dtype=np.uint8)

                        x_pos = x + column * square_size
                        y_pos = y + (rows - row - 1) * square_size

                        texture_id = glGenTextures(1)
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
                        glVertex3fv((x_pos, y_pos, -0.01))
                        glTexCoord2f(1.0, 0.0)
                        glVertex3fv((x_pos + square_size, y_pos, -0.01))
                        glTexCoord2f(1.0, 1.0)
                        glVertex3fv((x_pos + square_size, y_pos + square_size, -0.01))
                        glTexCoord2f(0.0, 1.0)
                        glVertex3fv((x_pos, y_pos + square_size, -0.01))
                        glEnd()
                        glDisable(GL_TEXTURE_2D)
                except FileNotFoundError:
                    pass
    
    def main_loop(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 and self.camera_pos[2] < -0.2:
                        self.camera_pos[2] -= 1 * (self.camera_pos[2] / 10)
                    elif event.button == 5:
                        self.camera_pos[2] += 1 * (self.camera_pos[2] / 10)

            keys = pygame.key.get_pressed()
            if (keys[pygame.K_w] or keys[pygame.K_UP]):
                self.camera_pos[1] += 0.3 * (self.camera_pos[2] / 10)
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
                self.camera_pos[1] -= 0.3 * (self.camera_pos[2] / 10)
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                self.camera_pos[0] -= 0.3 * (self.camera_pos[2] / 10)
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                self.camera_pos[0] += 0.3 * (self.camera_pos[2] / 10)
            if keys[pygame.K_e] and self.camera_pos[2] < -0.2:
                self.camera_pos[2] -= 0.5 * (self.camera_pos[2] / 10)
            if keys[pygame.K_q]:
                self.camera_pos[2] += 0.5 * (self.camera_pos[2] / 10)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 100.0)
            glTranslatef(self.camera_pos[0], self.camera_pos[1], self.camera_pos[2])
            glRotatef(180, 1, 0, 0)
            glClearColor(0.7, 0.8, 0.9, 1.0) # light blue-gray
            quads = self.draw_board()
            self.draw_pieces()
            pygame.display.flip()
            pygame.time.wait(10)


    def __str__(self) -> str:
        return f"Board: {self.board}\nRules: {self.rule_engine}"
