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
from rule_engines.standard_rule_engine import StandardRuleEngine
from boards.standard_board import StandardBoard
import pygame
from PIL import Image
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import colorsys
import math

class HexRenderEngine(AbstractRenderEngine):
    def __init__(self, screen_size, board: StandardBoard = None, rule_engine: StandardRuleEngine = None, illegal_moves=False, render_on_init=False):
        if board == None:
            self.board = StandardBoard(hexagonal=True)
        else:
            self.board = board
        if rule_engine == None:
            self.rule_engine = StandardRuleEngine(hexagonal=True)
        else:
            self.rule_engine = rule_engine

        self.illegal_moves = illegal_moves

        self.imgs = dict()

        if render_on_init:
            self.initialize(screen_size)

    def draw_board(self, zoom, highlight_tiles=None, selected_tile='', hover_tile='', x=0, y=0, z=0):
        prjMat = (GLfloat * 16)()
        glGetFloatv(GL_PROJECTION_MATRIX, prjMat)
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
            board_color = colorsys.hsv_to_rgb(colorsys.rgb_to_hsv(*current_team.color)[0], 0.5, 0.7)

        highlight_color=(1.0, 1.0, 0.0)
        selected_color=(1.0, 0.0, 0.0)
        hover_color=(0.0, 1.0, 1.0)
        hover_highlight_color=(0.0, 1.0, 0.0)
        tiles_highlight = [StandardBoard.tile_to_index(tile) for tile in highlight_tiles]
        if selected_tile != '':
            tile_selected = [StandardBoard.tile_to_index(selected_tile)]
        else:
            tile_selected = []
        if hover_tile != '':
            tile_hover = [StandardBoard.tile_to_index(hover_tile)]
        else:
            tile_hover = []

        square_size = 1 / 10 / math.sqrt(3)

        outer_border_width = 0.4 * square_size
        color_border_width = 0.35 * square_size # set the width of the border
        inner_border_width = 0.05 * square_size # set the width of the border
        quads = dict()

        x_min_max = [None, None]
        y_min_max = [None, None]
        for row in range(rows):
            for column in range(columns):
                x_col = 3/2 * column + 3/2 * row
                y_row = math.sqrt(3)/2.0 * column - math.sqrt(3)/2.0 * row
                x_pos = x + x_col * square_size
                y_pos = y + y_row * square_size
                z_pos = z

                tile = StandardBoard.index_to_tile(row, column)
                piece = self.board.get_tile(tile)
                if piece is None:
                    continue

                quad = ((x_pos, y_pos, z_pos), (x_pos + square_size, y_pos, z_pos), (x_pos + square_size, y_pos + square_size, z_pos), (x_pos, y_pos + square_size, z_pos))
                center = ((quad[0][0] + quad[2][0])/2, (quad[0][1] + quad[2][1])/2)
                angles = [60*i*math.pi/180 for i in range(6)]
                hexagon = [(center[0] + square_size * math.cos(angle), center[1] + square_size * math.sin(angle), z_pos) for angle in angles]

                for vertex in hexagon:
                    if x_min_max[0] == None or x_min_max[0] > vertex[0]:
                        x_min_max[0] = vertex[0]
                    if x_min_max[1] == None or x_min_max[1] < vertex[0]:
                        x_min_max[1] = vertex[0]
                    if y_min_max[0] == None or y_min_max[0] > vertex[1]:
                        y_min_max[0] = vertex[1]
                    if y_min_max[1] == None or y_min_max[1] < vertex[1]:
                        y_min_max[1] = vertex[1]
        
        outer_border = (
            (x_min_max[0] - outer_border_width, y_min_max[0] - outer_border_width, z),
            (x_min_max[1] + outer_border_width, y_min_max[0] - outer_border_width, z),
            (x_min_max[1] + outer_border_width, y_min_max[1] + outer_border_width, z),
            (x_min_max[0] - outer_border_width, y_min_max[1] + outer_border_width, z)
        )

        on_screen = HexRenderEngine.is_on_screen(outer_border, prjMat, zoom)
        if on_screen:
            # Draw the border rectangle
            glColor3f(0, 0, 0) # black
            glBegin(GL_QUADS)
            glVertex3f(*outer_border[0])
            glVertex3f(*outer_border[1])
            glVertex3f(*outer_border[2])
            glVertex3f(*outer_border[3])
            glEnd()

        color_border = (
            (x_min_max[0] - color_border_width, y_min_max[0] - color_border_width, z),
            (x_min_max[1] + color_border_width, y_min_max[0] - color_border_width, z),
            (x_min_max[1] + color_border_width, y_min_max[1] + color_border_width, z),
            (x_min_max[0] - color_border_width, y_min_max[1] + color_border_width, z)
        )

        on_screen = HexRenderEngine.is_on_screen(color_border, prjMat, zoom)
        if on_screen:
            # Draw the border rectangle
            glColor3f(*board_color) # black
            glBegin(GL_QUADS)
            glVertex3f(*color_border[0])
            glVertex3f(*color_border[1])
            glVertex3f(*color_border[2])
            glVertex3f(*color_border[3])
            glEnd()

        inner_border = (
            (x_min_max[0] - inner_border_width, y_min_max[0] - inner_border_width, z),
            (x_min_max[1] + inner_border_width, y_min_max[0] - inner_border_width, z),
            (x_min_max[1] + inner_border_width, y_min_max[1] + inner_border_width, z),
            (x_min_max[0] - inner_border_width, y_min_max[1] + inner_border_width, z)
        )

        on_screen = HexRenderEngine.is_on_screen(inner_border, prjMat, zoom)
        if on_screen:
            # Draw the border rectangle
            glColor3f(0, 0, 0) # black
            glBegin(GL_QUADS)
            glVertex3f(*inner_border[0])
            glVertex3f(*inner_border[1])
            glVertex3f(*inner_border[2])
            glVertex3f(*inner_border[3])
            glEnd()

        for row in range(rows):
            for column in range(columns):
                x_col = 3/2 * column + 3/2 * row
                y_row = math.sqrt(3)/2.0 * column - math.sqrt(3)/2.0 * row
                x_pos = x + x_col * square_size
                y_pos = y + y_row * square_size
                z_pos = z
                
                tile = StandardBoard.index_to_tile(row, column)
                piece = self.board.get_tile(tile)
                if piece is None:
                    continue

                tint = piece.tint

                quad = ((x_pos, y_pos, z_pos), (x_pos + square_size, y_pos, z_pos), (x_pos + square_size, y_pos + square_size, z_pos), (x_pos, y_pos + square_size, z_pos))
                center = ((quad[0][0] + quad[2][0])/2, (quad[0][1] + quad[2][1])/2)
                angles = [60*i*math.pi/180 for i in range(6)]
                hexagon = [(center[0] + square_size * math.cos(angle), center[1] + square_size * math.sin(angle), z_pos) for angle in angles]
                on_screen = HexRenderEngine.is_on_screen(hexagon, prjMat, zoom)
                if not on_screen:
                    continue

                if (row - column) % 3 == 0:
                    color = (0.9, 0.9, 0.9) # light gray
                elif (row - column) % 3 == 1:
                    color = (0.7, 0.7, 0.7) # dark gray
                else:
                    color = (0.8, 0.8, 0.8)
                
                color = (color[0]*tint[0], color[1]*tint[1], color[2]*tint[2])

                if (row, column) in tiles_highlight and (row, column) in tile_hover:
                    color = ((color[0] + hover_highlight_color[0])/2, (color[1] + hover_highlight_color[1])/2, (color[2] + hover_highlight_color[2])/2)
                elif (row, column) in tiles_highlight:
                    color = ((color[0] + highlight_color[0])/2, (color[1] + highlight_color[1])/2, (color[2] + highlight_color[2])/2)
                elif (row, column) in tile_selected:
                    color = ((color[0] + selected_color[0])/2, (color[1] + selected_color[1])/2, (color[2] + selected_color[2])/2)
                elif (row, column) in tile_hover:
                    color = ((color[0] + hover_color[0])/2, (color[1] + hover_color[1])/2, (color[2] + hover_color[2])/2)

                glBegin(GL_POLYGON)
                glColor3fv(color)
                glVertex3fv(hexagon[0])
                glVertex3fv(hexagon[1])
                glVertex3fv(hexagon[2])
                glVertex3fv(hexagon[3])
                glVertex3fv(hexagon[4])
                glVertex3fv(hexagon[5])
                glEnd()

                tile_name = StandardBoard.index_to_tile(row, column)

                quads[tile_name] = hexagon
        
        return quads

    def draw_pieces(self, imgs, zoom, pos):
        prjMat = (GLfloat * 16)()
        glGetFloatv(GL_PROJECTION_MATRIX, prjMat)
        rows = len(self.board.board)
        columns = len(self.board.board[0])
        x, y, z = pos

        square_size = 1 / 10 * 3/4
        for row in range(rows):
            for column in range(columns):
                x_col = 2*math.sqrt(3)/3 * column + 2*math.sqrt(3)/3 * row
                y_row = 2/3.0 * column - 2/3.0 * row
                x_pos = x + x_col * square_size - 0.0094 # Don't ask where this number comes from. I have no idea
                y_pos = y + y_row * square_size
                z_pos = z - 0.01
                quad = ((x_pos, y_pos, z_pos), (x_pos + square_size, y_pos, z_pos), (x_pos + square_size, y_pos + square_size, z_pos), (x_pos, y_pos + square_size, z_pos))
                on_screen = HexRenderEngine.is_on_screen(quad, prjMat, zoom)
                if not on_screen:
                    continue
                
                piece_color = (1.0, 1.0, 1.0)
                secondary_piece_color = (1.0, 1.0, 1.0)
                trinary_piece_color = (1.0, 1.0, 1.0)
                quadinary_piece_color = (1.0, 1.0, 1.0)
                tile = StandardBoard.index_to_tile(row, column)
                piece = self.board.get_tile(tile)
                if piece is None:
                    continue
                elif piece.piece == None:
                    continue
                else:
                    if piece.piece.team.name == 'black':
                        img = imgs['black'][piece.piece.name]
                        piece_data = np.asarray(img, dtype=np.uint8)
                    else:
                        img = imgs['white'][piece.piece.name]
                        piece_data = np.asarray(img, dtype=np.uint8)
                    if piece.piece.team.name in ['white', 'black']:
                        piece_color = (1.0, 1.0, 1.0)
                    else:
                        piece_color = piece.piece.team.color

                    if piece.piece.secondary_team.name == 'black':
                        if piece.piece.team.name == 'black':
                            secondary_piece_color = (1.0, 1.0, 1.0)
                        else:
                            secondary_piece_color = (0.0, 0.0, 0.0)
                    elif piece.piece.secondary_team.name == 'white':
                        secondary_piece_color = (1.0, 1.0, 1.0)
                    else:
                        secondary_piece_color = piece.piece.secondary_team.color

                    if piece.piece.trinary_team.name == 'black':
                        if piece.piece.team.name == 'black':
                            trinary_piece_color = (1.0, 1.0, 1.0)
                        else:
                            trinary_piece_color = (0.0, 0.0, 0.0)
                    elif piece.piece.trinary_team.name == 'white':
                        trinary_piece_color = (1.0, 1.0, 1.0)
                    else:
                        trinary_piece_color = piece.piece.trinary_team.color

                    if piece.piece.quadinary_team.name == 'black':
                        if piece.piece.team.name == 'black':
                            quadinary_piece_color = (1.0, 1.0, 1.0)
                        else:
                            quadinary_piece_color = (0.0, 0.0, 0.0)
                    elif piece.piece.secondary_team.name == 'white':
                        quadinary_piece_color = (1.0, 1.0, 1.0)
                    else:
                        quadinary_piece_color = piece.piece.quadinary_team.color

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
                glVertex3fv(quad[0])
                glColor3fv(trinary_piece_color)
                glTexCoord2f(1.0, 0.0)
                glVertex3fv(quad[1])
                glColor3fv(secondary_piece_color)
                glTexCoord2f(1.0, 1.0)
                glVertex3fv(quad[2])
                glColor3fv(quadinary_piece_color)
                glTexCoord2f(0.0, 1.0)
                glVertex3fv(quad[3])
                glEnd()
                glDisable(GL_TEXTURE_2D)

    def initialize(self, screen_size, ai_teams=None, ai_turn_delay=15):
        rows = len(self.board.board)
        columns = len(self.board.board[0])
        square_size = 1 / 10 / math.sqrt(3)
        x_min_max = [None, None]
        y_min_max = [None, None]
        for row in range(rows):
            for column in range(columns):
                x_col = 3/2 * column + 3/2 * row
                y_row = math.sqrt(3)/2.0 * column - math.sqrt(3)/2.0 * row
                x_pos = x_col * square_size
                y_pos = y_row * square_size
                z_pos = 0

                tile = StandardBoard.index_to_tile(row, column)
                piece = self.board.get_tile(tile)
                if piece is None:
                    continue

                quad = ((x_pos, y_pos, z_pos), (x_pos + square_size, y_pos, z_pos), (x_pos + square_size, y_pos + square_size, z_pos), (x_pos, y_pos + square_size, z_pos))
                center = ((quad[0][0] + quad[2][0])/2, (quad[0][1] + quad[2][1])/2)
                angles = [60*i*math.pi/180 for i in range(6)]
                hexagon = [(center[0] + square_size * math.cos(angle), center[1] + square_size * math.sin(angle), z_pos) for angle in angles]

                for vertex in hexagon:
                    if x_min_max[0] == None or x_min_max[0] > vertex[0]:
                        x_min_max[0] = vertex[0]
                    if x_min_max[1] == None or x_min_max[1] < vertex[0]:
                        x_min_max[1] = vertex[0]
                    if y_min_max[0] == None or y_min_max[0] > vertex[1]:
                        y_min_max[0] = vertex[1]
                    if y_min_max[1] == None or y_min_max[1] < vertex[1]:
                        y_min_max[1] = vertex[1]

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

        if ai_teams == None:
            self.ai_teams = dict()
        else:
            self.ai_teams = ai_teams

        self.ai_turn_delay = ai_turn_delay

        pygame.init()
        self.display = screen_size
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)
        self.screen_ratio = self.display[0]/self.display[1]
        self.zoom = 1.0

        rows = len(self.board.board) / 20
        columns = len(self.board.board[0]) / 20

        gluOrtho2D(-self.zoom, self.zoom, -self.zoom/self.screen_ratio, self.zoom/self.screen_ratio)
        glRotatef(180, 1, 0, 0)
        self.camera_pos = [-(x_min_max[0] + x_min_max[1])/2, -(y_min_max[0] + y_min_max[1])/2, 0.5]
        self.main_loop()

    def main_loop(self):

        hover_tile = ''
        selected_tile = ''
        frame = 0
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
                            self.board = self.rule_engine.play_move(self.board, selected_tile, hover_tile, self.illegal_moves, False)
                            selected_tile = ''
                    elif event.button == 3:
                        selected_tile = ''
                    if event.button == 4 and self.zoom > 0.2:
                        self.zoom -= self.zoom/2
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

            if selected_tile != '':
                highlight_tiles = self.rule_engine.get_legal_moves(selected_tile, self.board)
            elif hover_tile != '':
                highlight_tiles = self.rule_engine.get_legal_moves(hover_tile, self.board)
            else: 
                highlight_tiles = []

            glClearColor(0.7, 0.8, 0.9, 1.0) # light blue-gray
            quads = self.draw_board(self.zoom, highlight_tiles, selected_tile, hover_tile, *self.camera_pos)
            self.draw_pieces(self.imgs, self.zoom, self.camera_pos)
            pygame.display.flip()

            if (not self.rule_engine.all_legal_moves(self.board.current_team, self.board) and len(self.rule_engine.teams) > 2) or \
            self.board.current_team not in [self.board.get_tile(tile).piece.team.name for tile in self.board.royal_tiles if self.board.get_tile(tile).piece != None]:
                current_team = self.board.current_team
                next_index = self.rule_engine.turn_order.index(self.board.current_team) + 1
                if next_index in range(len(self.rule_engine.turn_order)):
                    self.board.current_team = self.rule_engine.turn_order[next_index]
                else:
                    self.board.current_team = self.rule_engine.turn_order[0]
                try:
                    self.rule_engine.turn_order.remove(current_team)
                except:
                    pass

            if self.board.current_team in self.ai_teams and frame % self.ai_turn_delay == 0 and len(self.rule_engine.turn_order) > 1:
                self.board = self.rule_engine.ai_play(self.board, False, self.ai_teams[self.board.current_team])

            prjMat = (GLfloat * 16)()
            glGetFloatv(GL_PROJECTION_MATRIX, prjMat)
            
            mouse = pygame.mouse.get_pos()

            for tile, quad in quads.items():
                if HexRenderEngine.TestRec(prjMat, mouse, self.display, self.zoom, quad):
                    hover_tile = tile
                    break
                else:
                    hover_tile = ''

            pygame.time.wait(10)
            frame += 1