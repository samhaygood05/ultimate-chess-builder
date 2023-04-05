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

from graph_board import GraphBoard, GraphPresets as gp
from rule_engines import GraphRuleEngine
from render_engines import AbstractRenderEngine
import pygame
from PIL import Image
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import colorsys
import copy
import math

class SquareGraphRenderEngine(AbstractRenderEngine):
    def __init__(self, board: GraphBoard = None, rule_engine: GraphRuleEngine = None, illegal_moves=False):
        if board == None:
            self.board = gp.create_standard_board()
        else:
            self.board = board
        if rule_engine == None:
            self.rule_engine = GraphRuleEngine()
        else:
            self.rule_engine = rule_engine

        self.illegal_moves = illegal_moves

        self.imgs = dict()
    
    def copy(self):
        copy_engine = SquareGraphRenderEngine(board=self.board.copy(), rule_engine=self.rule_engine.copy(), illegal_moves=self.illegal_moves)
        return copy_engine

    def draw_board(self, imgs, zoom, highlight_tiles=None, selected_tile='', hover_tile='', x=0, y=0, z=0):
        prjMat = (GLfloat * 16)()
        glGetFloatv(GL_PROJECTION_MATRIX, prjMat)

        current_team = self.rule_engine.turn_order[self.board.current_team_index]

        if highlight_tiles == None:
            highlight_tiles = []

        if current_team == 'white':
            board_color = (0.8, 0.8, 0.8)
        elif current_team == 'black':
            board_color = (0.3, 0.3, 0.3)
        else:
            board_color = colorsys.hsv_to_rgb(colorsys.rgb_to_hsv(*self.rule_engine.teams[current_team].color)[0], 0.5, 0.7)

        highlight_color=(1.0, 1.0, 0.0)
        selected_color=(1.0, 0.0, 0.0)
        hover_color=(0.0, 1.0, 1.0)
        hover_highlight_color=(0.0, 1.0, 0.0)
        if selected_tile != '':
            tile_selected = [selected_tile]
        else:
            tile_selected = []
        if hover_tile != '':
            tile_hover = [hover_tile]
        else:
            tile_hover = []

        square_size = 1 / 10
        outer_border_width = 0.3 * square_size # set the width of the border
        inner_border_width = 0.05 * square_size # set the width of the border
        board_width = [col * square_size for col in self.column_minmax]
        board_width = [board_width[0], board_width[1] + square_size]
        board_height = [row * square_size for row in self.row_minmax]
        board_height = [board_height[0], board_height[1] + square_size]
        quads = dict()

        outer_border = (
            (x + board_width[0] - outer_border_width - inner_border_width, y + board_height[0] - outer_border_width - inner_border_width, z),
            (x + board_width[1] + outer_border_width + inner_border_width, y + board_height[0] - outer_border_width - inner_border_width, z),
            (x + board_width[1] + outer_border_width + inner_border_width, y + board_height[1] + outer_border_width + inner_border_width, z),
            (x + board_width[0] - outer_border_width - inner_border_width, y + board_height[1] + outer_border_width + inner_border_width, z)
        )

        on_screen = SquareGraphRenderEngine.is_on_screen(outer_border, prjMat, zoom)
        if on_screen:
            # Draw the border rectangle
            glColor3f(0, 0, 0) # black
            glBegin(GL_QUADS)
            glVertex3f(*outer_border[0])
            glVertex3f(*outer_border[1])
            glVertex3f(*outer_border[2])
            glVertex3f(*outer_border[3])
            glEnd()

        team_border = (
            (x + board_width[0] - outer_border_width, y + board_height[0] - outer_border_width, z),
            (x + board_width[1] + outer_border_width, y + board_height[0] - outer_border_width, z),
            (x + board_width[1] + outer_border_width, y + board_height[1] + outer_border_width, z),
            (x + board_width[0] - outer_border_width, y + board_height[1] + outer_border_width, z)
        )

        on_screen = SquareGraphRenderEngine.is_on_screen(team_border, prjMat, zoom)
        if on_screen:
            # Draw the border rectangle
            glColor3f(*board_color) # black
            glBegin(GL_QUADS)
            glVertex3f(*team_border[0])
            glVertex3f(*team_border[1])
            glVertex3f(*team_border[2])
            glVertex3f(*team_border[3])
            glEnd()

        inner_border = (
            (x + board_width[0] - inner_border_width, y + board_height[0] - inner_border_width, z),
            (x + board_width[1] + inner_border_width, y + board_height[0] - inner_border_width, z),
            (x + board_width[1] + inner_border_width, y + board_height[1] + inner_border_width, z),
            (x + board_width[0] - inner_border_width, y + board_height[1] + inner_border_width, z)
        )

        on_screen = SquareGraphRenderEngine.is_on_screen(inner_border, prjMat, zoom)
        if on_screen:
            # Draw the border rectangle
            glColor3f(0, 0, 0) # black
            glBegin(GL_QUADS)
            glVertex3f(*inner_border[0])
            glVertex3f(*inner_border[1])
            glVertex3f(*inner_border[2])
            glVertex3f(*inner_border[3])
            glEnd()

        # Draw the checkerboard
        for position, node in self.board.nodes.items():
            if node.render_position == None:
                row, col = position
            else:
                row, col = node.render_position
            if node.render_rotation == None:
                rotation = 0
            else:
                rotation = node.render_rotation

            code_position = position

            x_pos = x + (col + 1/2) * square_size
            y_pos = y + (self.rows - row + 1/2) * square_size
            z_pos = z
            quad_centered = ((-square_size / 2, -square_size / 2, 0), (square_size / 2, -square_size / 2, 0), (square_size / 2, square_size / 2, 0), (-square_size / 2, square_size / 2, 0))
            rotated_quad = SquareGraphRenderEngine.rotate_quad(quad_centered, rotation)
            quad = tuple((x_pos + point[0], y_pos + point[1], z_pos + point[2]) for point in rotated_quad)
            on_screen = SquareGraphRenderEngine.is_on_screen(quad, prjMat, zoom)
            if not on_screen:
                continue

            tile = node.tile
            if tile == None:
                continue

            color = tile.tint

            if code_position in highlight_tiles and (row, col) in tile_hover:
                color = ((color[0] + hover_highlight_color[0])/2, (color[1] + hover_highlight_color[1])/2, (color[2] + hover_highlight_color[2])/2)
            elif code_position in highlight_tiles:
                color = ((color[0] + highlight_color[0])/2, (color[1] + highlight_color[1])/2, (color[2] + highlight_color[2])/2)
            elif code_position in tile_selected:
                color = ((color[0] + selected_color[0])/2, (color[1] + selected_color[1])/2, (color[2] + selected_color[2])/2)
            elif code_position in tile_hover:
                color = ((color[0] + hover_color[0])/2, (color[1] + hover_color[1])/2, (color[2] + hover_color[2])/2)

            glBegin(GL_QUADS)
            glColor3fv(color)
            glVertex3fv(quad[0])
            glVertex3fv(quad[1])
            glVertex3fv(quad[2])
            glVertex3fv(quad[3])
            glEnd()

            if tile.texture != None: 
                texture_id = imgs[tile.texture]
                glColor3fv((1.0, 1.0, 1.0))
                glEnable(GL_BLEND);
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
                glBindTexture(GL_TEXTURE_2D, texture_id)

                glEnable(GL_TEXTURE_2D)
                glBegin(GL_QUADS)
                glTexCoord2f(0.0, 0.0)
                glVertex3fv(quad[0])
                glTexCoord2f(1.0, 0.0)
                glVertex3fv(quad[1])
                glTexCoord2f(1.0, 1.0)
                glVertex3fv(quad[2])
                glTexCoord2f(0.0, 1.0)
                glVertex3fv(quad[3])
                glEnd()
                glDisable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, 0)

            quads[code_position] = quad
        
        return quads

    def draw_pieces(self, imgs, zoom, pos):
        prjMat = (GLfloat * 16)()
        glGetFloatv(GL_PROJECTION_MATRIX, prjMat)
        x, y, z = pos

        square_size = 1 / 10
        for position, node in self.board.nodes.items():
            if node.render_position == None:
                row, col = position
            else:
                row, col = node.render_position
            if node.render_rotation == None:
                rotation = 0
            else:
                rotation = node.render_rotation

            x_pos = x + (col) * square_size
            y_pos = y + (self.rows - row) * square_size
            z_pos = z - 0.01
            quad = ((x_pos, y_pos, z_pos), (x_pos + square_size, y_pos, z_pos), (x_pos + square_size, y_pos + square_size, z_pos), (x_pos, y_pos + square_size, z_pos))
            on_screen = SquareGraphRenderEngine.is_on_screen(quad, prjMat, zoom)
            if not on_screen:
                continue
            
            piece_color = (1.0, 1.0, 1.0)
            secondary_piece_color = (1.0, 1.0, 1.0)
            trinary_piece_color = (1.0, 1.0, 1.0)
            quadinary_piece_color = (1.0, 1.0, 1.0)
            piece = node.tile.piece
            if piece == None:
                continue
            elif piece.name == 'empty' or piece.name == None:
                continue
            else:
                if piece.team == 'black':
                    texture_id = imgs['black'][piece.name]
                else:
                    texture_id = imgs['white'][piece.name]
                if piece.team in ['white', 'black']:
                    piece_color = (1.0, 1.0, 1.0)
                else:
                    piece_color = self.rule_engine.teams[piece.team].color

                if piece.secondary_team == 'black':
                    if piece.team == 'black':
                        secondary_piece_color = (1.0, 1.0, 1.0)
                    else:
                        secondary_piece_color = (0.0, 0.0, 0.0)
                elif piece.secondary_team == 'white':
                    secondary_piece_color = (1.0, 1.0, 1.0)
                else:
                    secondary_piece_color = self.rule_engine.teams[piece.secondary_team].color

                if piece.trinary_team == 'black':
                    if piece.team == 'black':
                        trinary_piece_color = (1.0, 1.0, 1.0)
                    else:
                        trinary_piece_color = (0.0, 0.0, 0.0)
                elif piece.trinary_team == 'white':
                    trinary_piece_color = (1.0, 1.0, 1.0)
                else:
                    trinary_piece_color = self.rule_engine.teams[piece.trinary_team].color

                if piece.quadinary_team == 'black':
                    if piece.team == 'black':
                        quadinary_piece_color = (1.0, 1.0, 1.0)
                    else:
                        quadinary_piece_color = (0.0, 0.0, 0.0)
                elif piece.secondary_team == 'white':
                    quadinary_piece_color = (1.0, 1.0, 1.0)
                else:
                    quadinary_piece_color = self.rule_engine.teams[piece.quadinary_team].color

            glColor3fv(piece_color)
            glEnable(GL_BLEND);
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glBindTexture(GL_TEXTURE_2D, texture_id)

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

            glBindTexture(GL_TEXTURE_2D, 0)

    def store_imgs(self):
        piece_textures = dict()
        black_imgs = dict()
        white_imgs = dict()
        for piece in self.rule_engine.rulesets.keys():
            black_files = f"images/black/{piece}.png"
            white_files = f"images/white/{piece}.png"
            with open(white_files, "rb") as file:
                img = Image.open(file).convert('RGBA')
                texture_id = self.generate_texture(img)
                white_imgs[piece] = texture_id
            with open(black_files, "rb") as file:
                img = Image.open(file).convert('RGBA')
                texture_id = self.generate_texture(img)
                black_imgs[piece] = texture_id
        
        piece_textures['white'] = white_imgs
        piece_textures['black'] = black_imgs

        self.piece_textures = piece_textures

        self.tile_textures = dict()
        
        for texture in self.board.tile_textures:
            if texture == None:
                continue
            texture_file = f'images/tiles/{texture}.png'
            with open(texture_file, "rb") as file:
                img = Image.open(file).convert('RGBA')
                texture_id = self.generate_texture(img)
                self.tile_textures[texture] = texture_id
        print('pieces:', self.piece_textures)
        print('tiles:', self.tile_textures)

    def generate_texture(self, img):
        texture_data = np.asarray(img, dtype=np.uint8)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

        return texture_id

    def initialize(self, screen_size, ai_teams=None, ai_turn_delay=15):

        if ai_teams == None:
            self.ai_teams = dict()
        else:
            self.ai_teams = ai_teams

        self.ai_turn_delay = ai_turn_delay

        self.display = screen_size
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)
        self.screen_ratio = self.display[0]/self.display[1]
        self.zoom = 1.0

        row_min = None
        row_max = None
        column_min = None
        column_max = None
        for node_position, node in self.board.nodes.items():
            if node.render_position == None:
                node_row, node_col = node_position
            else:
                node_row, node_col = node.render_position

            if row_min == None:
                row_min = node_row
            else:
                row_min = min(row_min, node_row)
            if row_max == None:
                row_max = node_row
            else:
                row_max = max(row_max, node_row)
            if column_min == None:
                column_min = node_col
            else:
                column_min = min(column_min, node_col)
            if column_max == None:
                column_max = node_col
            else:
                column_max = max(column_max, node_col)

        self.row_minmax = (row_min, row_max)
        self.column_minmax = (column_min, column_max)

        self.center = ((row_max + row_min) / 2, (column_max + column_min) / 2)


        self.rows = row_max - row_min
        self.columns = column_max - column_min

        gluOrtho2D(-self.zoom, self.zoom, -self.zoom/self.screen_ratio, self.zoom/self.screen_ratio)
        glRotatef(180, 1, 0, 0)
        self.camera_pos = [-(self.center[1]) / 10, -(self.center[0]) / 10, 0.5]
        
        self.store_imgs()

        return self.main_loop()

    def main_loop(self):

        hover_tile = ''
        selected_tile = ''
        frame = 0
        turn = 1
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
                            if self.board.current_team_index == len(self.rule_engine.turn_order) - 1:
                                turn += 1
                            self.board = self.rule_engine.play_move(self.board, selected_tile, hover_tile, self.illegal_moves, False)
                            selected_tile = ''
                    elif event.button == 3:
                        selected_tile = ''
                    elif event.button == 4 and self.zoom > 0.2:
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
                highlight_tiles = [move[0] for move in self.rule_engine.get_legal_moves(selected_tile, self.board)]
            elif hover_tile != '':
                highlight_tiles = [move[0] for move in self.rule_engine.get_legal_moves(hover_tile, self.board)]
            else: 
                highlight_tiles = []

            glClearColor(0.7, 0.8, 0.9, 1.0) # light blue-gray
            quads = self.draw_board(self.tile_textures, self.zoom, highlight_tiles, selected_tile, hover_tile, *self.camera_pos)
            self.draw_pieces(self.piece_textures, self.zoom, self.camera_pos)
            pygame.display.flip()

            current_team = self.rule_engine.turn_order[self.board.current_team_index]

            # if (not self.rule_engine.get_all_legal_moves(current_team, self.board) and len(self.rule_engine.teams) > 2) or \
            # current_team not in self.board.royal_tiles:
            #     self.board.current_team_index = (self.board.current_team_index + 1) % len(self.rule_engine.turn_order)
            #     try:
            #         self.rule_engine.turn_order.remove(current_team)
            #         if len(self.rule_engine.turn_order) == 1:
            #             break
            #     except:
            #         pass

            # if self.board.current_team in self.ai_teams and frame % self.ai_turn_delay == 0 and len(self.rule_engine.turn_order) > 1:
            #     if self.board.current_team == self.rule_engine.turn_order[-1]:
            #         turn += 1
            #     self.board = self.rule_engine.ai_play(self.board, False, self.ai_teams[self.board.current_team])

            prjMat = (GLfloat * 16)()
            glGetFloatv(GL_PROJECTION_MATRIX, prjMat)
            
            mouse = pygame.mouse.get_pos()

            for tile, quad in quads.items():
                if SquareGraphRenderEngine.TestRec(prjMat, mouse, self.display, self.zoom, quad):
                    hover_tile = tile
                    break
                else:
                    hover_tile = ''

            pygame.time.wait(10)
            frame += 1

        pygame.quit()
        return self.rule_engine.turn_order[0], turn

    def __str__(self) -> str:
        return f"Board: {self.board}\nRules: {self.rule_engine}"
