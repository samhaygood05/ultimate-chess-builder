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

from datetime import datetime
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

from variants import Variants

class GraphRenderEngine(AbstractRenderEngine):
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
        copy_engine = GraphRenderEngine(board=self.board.copy(), rule_engine=self.rule_engine.copy(), illegal_moves=self.illegal_moves)
        return copy_engine

    def draw_boarder(self, zoom, x=0, y=0, z=0):
        prjMat = (GLfloat * 16)()
        glGetFloatv(GL_PROJECTION_MATRIX, prjMat)

        current_team = self.rule_engine.turn_order[self.board.current_team_index]
        if current_team == 'white':
            board_color = (0.8, 0.8, 0.8)
        elif current_team == 'black':
            board_color = (0.3, 0.3, 0.3)
        else:
            team_color_hsv = colorsys.rgb_to_hsv(*self.rule_engine.teams[current_team].color)
            board_color = colorsys.hsv_to_rgb(team_color_hsv[0], 0.5*team_color_hsv[1], 0.7 if team_color_hsv[2] == 1.0 else team_color_hsv[2])

        square_size = 1 / 10
        outer_border_width = 1.05 # set the width of the border
        team_border_width = 1.04
        inner_border_width = 1.01 # set the width of the border

        hull, hull_center = self.hull
        def scale_hull(hull, center, scale):
            centered_hull = [(vertex[0]-center[0], vertex[1]-center[1]) for vertex in hull]
            hull_scale = [(vertex[0]*scale, vertex[1]*scale) for vertex in centered_hull]
            hull_shift = [(vertex[0]+center[0], vertex[1]+center[1]) for vertex in hull_scale]
            hull_proper_scaled = [(x + vertex[0]*square_size, y+ vertex[1]*square_size, z) for vertex in hull_shift]
            return hull_proper_scaled

        outer_border = scale_hull(hull, hull_center, outer_border_width)

        on_screen = GraphRenderEngine.is_on_screen(outer_border, prjMat, zoom)
        if on_screen:
            # Draw the border hull
            glColor3f(0, 0, 0)
            glBegin(GL_POLYGON)
            for vertex in outer_border:
                glVertex3f(*vertex)
            glEnd()

        team_border = scale_hull(hull, hull_center, team_border_width)

        on_screen = GraphRenderEngine.is_on_screen(team_border, prjMat, zoom)
        if on_screen:
            # Draw the border hull
            glColor3f(*board_color)
            glBegin(GL_POLYGON)
            for vertex in team_border:
                glVertex3f(*vertex)
            glEnd()

        inner_border = scale_hull(hull, hull_center, inner_border_width)

        on_screen = GraphRenderEngine.is_on_screen(inner_border, prjMat, zoom)
        if on_screen:
            # Draw the border hull
            glColor3f(0, 0, 0)
            glBegin(GL_POLYGON)
            for vertex in inner_border:
                glVertex3f(*vertex)
            glEnd()

    def draw_board(self, imgs, zoom, highlight_tiles=None, selected_tile='', hover_tile='', x=0, y=0, z=0):
        prjMat = (GLfloat * 16)()
        glGetFloatv(GL_PROJECTION_MATRIX, prjMat)

        if highlight_tiles == None:
            highlight_tiles = []

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
        polygons = dict()

        # Draw the checkerboard
        for position, node in self.board.nodes.items():

            code_position = position
            polygon = node.render_polygon
            texture_quad = node.texture_quad

            polygon = tuple((vertex[0] * square_size + x, vertex[1] * square_size + y, vertex[2] * square_size + z) for vertex in polygon)
            texture_quad = tuple((vertex[0] * square_size + x, vertex[1] * square_size + y, vertex[2] * square_size + z) for vertex in texture_quad)

            on_screen = GraphRenderEngine.is_on_screen(polygon, prjMat, zoom)
            if not on_screen:
                continue
            polygons[code_position] = polygon

            tile = node.tile
            if tile == None:
                continue

            color = tile.tint

            if code_position in highlight_tiles and code_position in tile_hover:
                color = ((color[0] + hover_highlight_color[0])/2, (color[1] + hover_highlight_color[1])/2, (color[2] + hover_highlight_color[2])/2)
            elif code_position in highlight_tiles:
                color = ((color[0] + highlight_color[0])/2, (color[1] + highlight_color[1])/2, (color[2] + highlight_color[2])/2)
            elif code_position in tile_selected:
                color = ((color[0] + selected_color[0])/2, (color[1] + selected_color[1])/2, (color[2] + selected_color[2])/2)
            elif code_position in tile_hover:
                color = ((color[0] + hover_color[0])/2, (color[1] + hover_color[1])/2, (color[2] + hover_color[2])/2)

            glBegin(GL_POLYGON)
            glColor3fv(color)
            for vertex in polygon:
                glVertex3fv(vertex)
            glEnd()

            if tile.texture != None: 
                texture_id = imgs[tile.texture]
                glColor3fv((1.0, 1.0, 1.0))
                glEnable(GL_BLEND);
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
                glBindTexture(GL_TEXTURE_2D, texture_id)

                glEnable(GL_TEXTURE_2D)
                glBegin(GL_QUADS)
                for vertex, uv_vertex in zip(texture_quad, self.uv_quad):
                    glTexCoord2f(*uv_vertex)
                    glVertex3fv(vertex)
                glEnd()
                glDisable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, 0)
        
        return polygons

    def draw_pieces(self, imgs, zoom, pos):
        prjMat = (GLfloat * 16)()
        glGetFloatv(GL_PROJECTION_MATRIX, prjMat)
        x, y, z = pos

        square_size = 1 / 10
        for position, node in self.board.nodes.items():
            
            texture_quad = node.texture_quad
            texture_quad = tuple((vertex[0] * square_size + x, vertex[1] * square_size + y, vertex[2] * square_size + z) for vertex in texture_quad)

            on_screen = GraphRenderEngine.is_on_screen(texture_quad, prjMat, zoom)
            if not on_screen:
                continue
            
            piece_colors = [
                (1.0, 1.0, 1.0),
                (1.0, 1.0, 1.0),
                (1.0, 1.0, 1.0),
                (1.0, 1.0, 1.0)
            ]
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
                    piece_colors[0] = (1.0, 1.0, 1.0)
                else:
                    piece_colors[0] = self.rule_engine.teams[piece.team].color

                if piece.secondary_team == 'black':
                    if piece.team == 'black':
                        piece_colors[1] = (1.0, 1.0, 1.0)
                    else:
                        piece_colors[1] = (0.0, 0.0, 0.0)
                elif piece.secondary_team == 'white':
                    piece_colors[1] = (1.0, 1.0, 1.0)
                else:
                    piece_colors[1] = self.rule_engine.teams[piece.secondary_team].color

                if piece.trinary_team == 'black':
                    if piece.team == 'black':
                        piece_colors[2] = (1.0, 1.0, 1.0)
                    else:
                        piece_colors[2] = (0.0, 0.0, 0.0)
                elif piece.trinary_team == 'white':
                    piece_colors[2] = (1.0, 1.0, 1.0)
                else:
                    piece_colors[2] = self.rule_engine.teams[piece.trinary_team].color

                if piece.quadinary_team == 'black':
                    if piece.team == 'black':
                        piece_colors[3] = (1.0, 1.0, 1.0)
                    else:
                        piece_colors[3] = (0.0, 0.0, 0.0)
                elif piece.secondary_team == 'white':
                    piece_colors[3] = (1.0, 1.0, 1.0)
                else:
                    piece_colors[3] = self.rule_engine.teams[piece.quadinary_team].color

            piece_colors = [piece_colors[0], piece_colors[2], piece_colors[1], piece_colors[3]]

            glEnable(GL_BLEND);
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glBindTexture(GL_TEXTURE_2D, texture_id)

            glEnable(GL_TEXTURE_2D)
            glBegin(GL_QUADS)
            for vertex, uv_vertex, color in zip(texture_quad, self.uv_quad, piece_colors):
                glColor3fv(color)
                glTexCoord2f(*uv_vertex)
                glVertex3fv(vertex)
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

    def initialize(self, screen_size, zoom=1.0, ai_teams=None, ai_turn_delay=15):

        if ai_teams == None:
            self.ai_teams = dict()
        else:
            self.ai_teams = ai_teams

        self.ai_turn_delay = ai_turn_delay

        for team in self.rule_engine.turn_order:
            if team not in self.board.royal_tiles:
                self.board.royal_tiles[team] = []

        self.hull = self.board.init_hull()
        self.team_royal_numbers = {team: len(royals) for team, royals in self.board.royal_tiles.items()}

        self.display = screen_size
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)
        self.screen_ratio = self.display[0]/self.display[1]
        self.zoom = zoom
        self.angle = 0

        self.uv_quad = (
            (0.0, 0.0),
            (1.0, 0.0),
            (1.0, 1.0),
            (0.0, 1.0)
        )

        row_min = None
        row_max = None
        column_min = None
        column_max = None
        for node_position, node in self.board.nodes.items():
            for node_col, node_row, _ in node.render_polygon:
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
        glRotatef(self.angle, 0, 0, 1)
        self.camera_pos = [-(self.center[1]) / 10, -(self.center[0]) / 10, 0.5]
        
        self.store_imgs()

        return self.main_loop()

    def main_loop(self):

        hover_tile = ''
        selected_tile = ''
        frame = 0
        turn = 1
        saved = False

        while True:

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            gluOrtho2D(-self.zoom, self.zoom, -self.zoom/self.screen_ratio, self.zoom/self.screen_ratio)
            glRotatef(180, 1, 0, 0)
            glRotatef(self.angle, 0, 0, 1)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print('selected', hover_tile)
                        if selected_tile == '':
                            selected_tile = hover_tile
                        else:
                            if self.board.current_team_index == len(self.rule_engine.turn_order) - 1:
                                turn += 1
                            self.board = self.rule_engine.play_move(self.board, selected_tile, hover_tile, self.illegal_moves, False)
                            saved = False
                            selected_tile = ''
                    elif event.button == 3:
                        selected_tile = ''
                    elif event.button == 4 and self.zoom > 0.2:
                        self.zoom -= self.zoom/2
                    elif event.button == 5:
                        self.zoom += self.zoom

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.camera_pos[1] += 0.3 * self.zoom / 5
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and not (keys[pygame.K_LCTRL] or keys[pygame.K_LMETA]):
                self.camera_pos[1] -= 0.3 * self.zoom / 5
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.camera_pos[0] += 0.3 * self.zoom / 5
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.camera_pos[0] -= 0.3 * self.zoom / 5
            if keys[pygame.K_x] and self.zoom > 0.2:
                self.zoom -= self.zoom / 20
            if keys[pygame.K_z]:
                self.zoom += self.zoom / 20
            if keys[pygame.K_q]:
                self.angle -= 1
            if keys[pygame.K_e]:
                self.angle += 1
            if keys[pygame.K_s] and (keys[pygame.K_LCTRL] or keys[pygame.K_LMETA]) and not saved:
                now = datetime.now()
                default_save_name = now.strftime("%Y-%m-%d_%H-%M-%S")
                save_file_name = GraphRenderEngine.get_save_file_name(default_save_name)
                if save_file_name:
                    Variants.save(save_file_name, self, 'saves')
                    saved = True
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return self.rule_engine.turn_order[0], turn

            if selected_tile != '':
                highlight_tiles = [move[0] for move in self.rule_engine.get_legal_moves(selected_tile, self.board)]
            elif hover_tile != '':
                highlight_tiles = [move[0] for move in self.rule_engine.get_legal_moves(hover_tile, self.board)]
            else: 
                highlight_tiles = []

            glClearColor(0.7, 0.8, 0.9, 1.0) # light blue-gray
            self.draw_boarder(self.zoom, *self.camera_pos)
            quads = self.draw_board(self.tile_textures, self.zoom, highlight_tiles, selected_tile, hover_tile, *self.camera_pos)
            self.draw_pieces(self.piece_textures, self.zoom, self.camera_pos)
            pygame.display.flip()

            current_team = self.rule_engine.turn_order[self.board.current_team_index]

            if self.rule_engine.lose[current_team] == 'eliminate_royals' and not self.board.royal_tiles[current_team]:
                self.rule_engine.turn_order.remove(current_team)
                print(f"all of {current_team}'s royal pieces were eliminated")
                self.board.current_team_index = self.board.current_team_index % len(self.rule_engine.turn_order)

            elif self.rule_engine.lose[current_team] == 'eliminate_any_royal' and len(self.board.royal_tiles[current_team]) < self.team_royal_numbers[current_team]:
                self.rule_engine.turn_order.remove(current_team)
                print(f"one of {current_team}'s royal pieces was eliminated")
                self.board.current_team_index = self.board.current_team_index % len(self.rule_engine.turn_order)

            if not self.board.get_team_pieces(current_team):
                self.rule_engine.turn_order.remove(current_team)
                print(f"all of {current_team}'s pieces were eliminated")
                self.board.current_team_index = self.board.current_team_index % len(self.rule_engine.turn_order)

            # if self.board.current_team in self.ai_teams and frame % self.ai_turn_delay == 0 and len(self.rule_engine.turn_order) > 1:
            #     if self.board.current_team == self.rule_engine.turn_order[-1]:
            #         turn += 1
            #     self.board = self.rule_engine.ai_play(self.board, False, self.ai_teams[self.board.current_team])
            #     saved = False

            prjMat = (GLfloat * 16)()
            glGetFloatv(GL_PROJECTION_MATRIX, prjMat)
            
            mouse = pygame.mouse.get_pos()

            if quads:
                for tile, quad in quads.items():
                    try:
                        if self.board.get_node_tile(tile).not_selectable:
                            continue
                    except:
                        pass
                    if GraphRenderEngine.TestRec(prjMat, mouse, self.display, self.zoom, quad):
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
