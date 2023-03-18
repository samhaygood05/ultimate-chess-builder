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
from render_engines.square_render_engine import SquareRenderEngine
from render_engines.hex_render_engine import HexRenderEngine
from rule_engines.timetravel_rule_engine import TimeTravelRuleEngine
from boards.poly_board import PolyBoard
import pygame
from PIL import Image
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import colorsys

class TimeTravelRenderEngine(AbstractRenderEngine):
    def __init__(self, screen_size, board: PolyBoard = None, rule_engine: TimeTravelRuleEngine = None, illegal_moves=False, render_on_init=False):
        if board == None:
            self.board = PolyBoard()
        else:
            self.board = board
        if rule_engine == None:
            self.rule_engine = TimeTravelRuleEngine()
        else:
            self.rule_engine = rule_engine

        self.illegal_moves = illegal_moves

        if render_on_init:
            self.initialize(screen_size)


    def draw_board(self, highlight_tiles=None, selected_tile=(('a', 'a'), ''), hover_tile=(('a', 'a'), ''), x=0, y=0, z=0):
        max_rows = 0
        max_cols = 0
        for board in self.board.boards.values():
            max_rows = max(max_rows, len(board.board) / 10)
            max_cols = max(max_cols, len(board.board[0]) / 10)
        
        if highlight_tiles == None:
            highlight_tiles = []
        

        square_size = 1 / 10
        outer_border_width = 0.3 * square_size # set the width of the border
        inner_border_width = 0.05 * square_size # set the width of the border

        max_board_size = (max_cols + 4*inner_border_width + 2*outer_border_width, max_rows + 4*inner_border_width + 2*outer_border_width)
        board_quads = dict()
        
        for board_loc, board in self.board.boards.items():
            highlight = [tile[1] for tile in highlight_tiles if tile[0] == board_loc]
            select = ''
            hover = ''
            if selected_tile[0] == board_loc:
                select = selected_tile[1]
            if hover_tile[0] == board_loc:
                hover = hover_tile[1]

            rows = len(board.board) / 20
            cols = len(board.board[0]) / 20
            board_center = (cols + 2*inner_border_width + outer_border_width, rows + 2*inner_border_width + outer_border_width)
            if board.hexagonal:
                quads = HexRenderEngine((0, 0), board=board, render_on_init=False).draw_board(self.zoom, highlight, select, hover, x + max_board_size[0]*(board_loc[1] + 1/2) - board_center[0], y + max_board_size[1]*(1/2 - board_loc[0]) - board_center[1], z)
            else:
                quads = SquareRenderEngine((0, 0), board=board, render_on_init=False).draw_board(self.zoom, highlight, select, hover, x + max_board_size[0]*(board_loc[1] + 1/2) - board_center[0], y + max_board_size[1]*(1/2 - board_loc[0]) - board_center[1], z)
            board_quads[board_loc] = quads
        
        return board_quads
    

    def draw_pieces(self, x=0, y=0, z=0):
        max_rows = 0
        max_cols = 0
        for board in self.board.boards.values():
            max_rows = max(max_rows, len(board.board) / 10)
            max_cols = max(max_cols, len(board.board[0]) / 10)
        
        square_size = 1 / 10
        outer_border_width = 0.3 * square_size # set the width of the border
        inner_border_width = 0.05 * square_size # set the width of the border

        max_board_size = (max_cols + 4*inner_border_width + 2*outer_border_width, max_rows + 4*inner_border_width + 2*outer_border_width)

        for board_loc, board in self.board.boards.items():
            rows = len(board.board) / 20
            cols = len(board.board[0]) / 20
            board_center = (cols + 2*inner_border_width + outer_border_width, rows + 2*inner_border_width + outer_border_width)
            if board.hexagonal:
                HexRenderEngine((0, 0), board=board, render_on_init=False).draw_pieces(self.imgs, self.zoom, (x + max_board_size[0]*(board_loc[1] + 1/2) - board_center[0], y + max_board_size[1]*(1/2 - board_loc[0]) - board_center[1], z))
            else:
                SquareRenderEngine((0, 0), board=board, render_on_init=False).draw_pieces(self.imgs, self.zoom, (x + max_board_size[0]*(board_loc[1] + 1/2) - board_center[0], y + max_board_size[1]*(1/2 - board_loc[0]) - board_center[1], z))

    def initialize(self, screen_size):
        imgs = dict()
        black_imgs = dict()
        white_imgs = dict()
        for piece in self.rule_engine.rulesets.keys():
            black_files = f"images/black/{piece}.png"
            white_files = f"images/white/{piece}.png"
            with open(white_files, "rb") as file:
                img = Image.open(file).convert('RGBA')
                white_imgs[piece] = img
            with open(black_files, "rb") as file:
                img = Image.open(file).convert('RGBA')
                black_imgs[piece] = img
        
        imgs['black'] = black_imgs
        imgs['white'] = white_imgs

        self.imgs = imgs

        pygame.init()
        self.display = screen_size
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)
        self.screen_ratio = self.display[0]/self.display[1]
        self.zoom = 1.0
        rows = len(self.board.boards[(0,0)].board) / 20
        columns = len(self.board.boards[(0,0)].board[0]) / 20
        
        gluOrtho2D(-self.zoom, self.zoom, -self.zoom/self.screen_ratio, self.zoom/self.screen_ratio)
        glRotatef(180, 1, 0, 0)
        self.camera_pos = [-columns, -rows, 0.5]
        self.main_loop()

    def main_loop(self):
        hover_tile = (('a', 'a'), '')
        selected_tile = (('a', 'a'), '')
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
                        if selected_tile == (('a', 'a'), ''):
                            selected_tile = hover_tile
                        else:
                            self.board = self.rule_engine.play_move(self.board, selected_tile, hover_tile, self.illegal_moves)
                            selected_tile = (('a', 'a'), '')
                    elif event.button == 3:
                        selected_tile = (('a', 'a'), '')
                    elif event.button == 4 and self.zoom > 0.2:
                        self.zoom = max(self.zoom - 0.5 * self.zoom, 0.2)
                    elif event.button == 5:
                        self.zoom += self.zoom

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
                self.zoom -= self.zoom / 20
            if keys[pygame.K_q]:
                self.zoom += self.zoom / 20

            if selected_tile != (('a', 'a'), ''):
                highlight_tiles = self.rule_engine.get_legal_moves(selected_tile, self.board)
            elif hover_tile != (('a', 'a'), ''):
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

            break_out = False
            for board_loc, board in quads.items():
                for tile, quad in board.items():
                    if SquareRenderEngine.TestRec(prjMat, mouse, self.display, self.zoom, quad):
                        hover_tile = (board_loc, tile)
                        break_out = True
                        break
                    else:
                        hover_tile = (('a', 'a'), '')
                if break_out:
                    break

            pygame.time.wait(10)
