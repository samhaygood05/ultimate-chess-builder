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
import math
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
import pickle

class GraphRenderEngine(AbstractRenderEngine):
    def __init__(self, board: GraphBoard = None, rule_engine: GraphRuleEngine = None, illegal_moves=False):
        if board == None:
            self.board = gp.standard_board()
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

    def get_board_color(self, current_team):
        if current_team == None:
            return 0.0, 0.0, 0.0
        elif current_team == 'white':
            return 0.8, 0.8, 0.8
        elif current_team == 'black':
            return 0.3, 0.3, 0.3
        else:
            team_color_hsv = colorsys.rgb_to_hsv(*self.rule_engine.teams[current_team].color)
            return colorsys.hsv_to_rgb(team_color_hsv[0], 0.5 * team_color_hsv[1], 0.7 if team_color_hsv[2] == 1.0 else team_color_hsv[2])

    def draw_boarder(self, zoom, x=0, y=0, z=0):
        mvMat = glGetDoublev(GL_MODELVIEW_MATRIX)
        prjMat = glGetDoublev(GL_PROJECTION_MATRIX)

        if self.rule_engine.turn_order:
            current_team = self.rule_engine.turn_order[self.board.current_team_index]
        else:
            current_team = None
        board_color = self.get_board_color(current_team)

        square_size = 1 / 10
        border_widths = [1.05, 1.04, 1.01]  # Outer, Team, and Inner border widths

        hull, hull_center = self.hull

        def scale_hull(hull, center, scale):
            return [(x + ((vx - center[0]) * scale + center[0]) * square_size, y + ((vy - center[1]) * scale + center[1]) * square_size, z+vz)
                    for vx, vy, vz in hull]

        def draw_border(border, color):
            on_screen = GraphRenderEngine.is_on_screen(border, mvMat, prjMat, zoom)
            if on_screen:
                glColor3f(*color)
                glBegin(GL_POLYGON)
                for vertex in border:
                    glVertex3f(*vertex)
                glEnd()

        colors = [(0, 0, 0), board_color, (0, 0, 0)]
        for width, color in zip(border_widths, colors):
            border = scale_hull(hull, hull_center, width)
            draw_border(border, color)

    def draw_board(self, imgs, zoom, highlight_tiles=None, selected_tile='', hover_tile='', x=0, y=0, z=0):
        
        mvMat = glGetDoublev(GL_MODELVIEW_MATRIX)
        prjMat = glGetDoublev(GL_PROJECTION_MATRIX)

        if not highlight_tiles:
            highlight_tiles = []

        colors = {
            'highlight': (1.0, 1.0, 0.0),
            'selected': (1.0, 0.0, 0.0),
            'hover': (0.0, 1.0, 1.0),
            'hover_highlight': (0.0, 1.0, 0.0),
        }

        square_size = 1 / 10
        polygons = dict()

        for position, node in self.board.nodes.items():
            polygon, texture_quad = ([(vertex[0] * square_size + x, vertex[1] * square_size + y, vertex[2] * square_size + z) for vertex in node_attr] for node_attr in (node.render_polygon, node.texture_quad))

            if not GraphRenderEngine.is_on_screen(polygon, mvMat, prjMat, zoom):
                continue

            polygons[position] = polygon
            tile = node.tile

            if tile is None:
                continue

            color = tile.tint

            for key, c in colors.items():
                if position in (highlight_tiles if key == 'highlight' else [selected_tile] if key == 'selected' else [hover_tile]):
                    color = ((color[0] + c[0]) / 2, (color[1] + c[1]) / 2, (color[2] + c[2]) / 2)
                    break

            glBegin(GL_POLYGON)
            glColor3fv(color)
            for vertex in polygon:
                glVertex3fv(vertex)
            glEnd()

            if tile.texture is not None:
                texture_id = imgs[tile.texture]
                glColor3fv((1.0, 1.0, 1.0))
                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
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

    def draw_pieces(self, imgs, zoom, pos=(0.0, 0.0, 0.0), angle=0):
        mvMat = glGetDoublev(GL_MODELVIEW_MATRIX)
        prjMat = glGetDoublev(GL_PROJECTION_MATRIX)
        x, y, z = pos

        angle = math.radians(-angle)
        cos = math.cos(angle)
        sin = math.sin(angle)

        def polygon_centroid(vertices):
            area = 0
            x_sum = 0
            y_sum = 0
            z_min = min(vertex[2] for vertex in vertices)
            for i in range(len(vertices)):
                j = (i + 1) % len(vertices)
                cross_product = vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
                area += cross_product
                x_sum += (vertices[i][0] + vertices[j][0]) * cross_product
                y_sum += (vertices[i][1] + vertices[j][1]) * cross_product

            area *= 0.5
            x_centroid = x_sum / (6 * area)
            y_centroid = y_sum / (6 * area)

            return (x_centroid, y_centroid, z_min)

        square_size = 1 / 10
        for position, node in self.board.nodes.items():


            texture_quad = [(vertex[0] * square_size + x, vertex[1] * square_size + y, vertex[2] * square_size + z) for vertex in node.texture_quad]
            center = polygon_centroid(texture_quad)
            centered_quad = [[vertex[i] - center[i] for i in range(3)] for vertex in texture_quad]
            rotated_quad = [[vertex[0]*cos - vertex[1]*sin, vertex[0]*sin + vertex[1]*cos, vertex[2]] for vertex in centered_quad]
            texture_quad = [[vertex[i] + center[i] for i in range(3)] for vertex in rotated_quad]

            if not GraphRenderEngine.is_on_screen(texture_quad, mvMat, prjMat, zoom):
                continue

            piece = node.tile.piece
            if piece and piece.name not in [None, 'empty']:
                file_name = 'black' if piece.team == 'black' else 'white'
                texture_id = imgs[file_name][piece.name]
                piece_colors = (1.0, 1.0, 1.0) if piece.team in ('white', 'black') else self.rule_engine.teams[piece.team].color
                piece_colors = [self.rule_engine.teams[piece.team].color]

                for team_attr in ('trinary_team', 'secondary_team', 'quadinary_team'):
                    team = getattr(piece, team_attr)
                    color = self.rule_engine.teams[team].color
                    piece_colors.append(color)

                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
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

    def save(self, name, file_path = 'saves'):
        path = f"saved/{file_path}/{name}.ucbgame"
        try:
            with open(path, 'xb') as f:
                pickle.dump(self, f)
        except:
            with open(path, 'wb') as f:
                pickle.dump(self, f)
        print(f'{name} Game Saved')

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
        
        self.camera_pos = [-self.hull[1][0] / 10, -self.hull[1][1] / 10, 0.5]

        gluOrtho2D(-self.zoom, self.zoom, -self.zoom/self.screen_ratio, self.zoom/self.screen_ratio)
        glRotatef(180, 1, 0, 0)
        glRotatef(self.angle, 0, 0, 1)
        
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
                        elif self.rule_engine.turn_order:
                            self.board.current_team_index %= len(self.rule_engine.turn_order)
                            self.board = self.rule_engine.play_move(self.board, selected_tile, hover_tile, self.illegal_moves, False)
                            saved = False
                            selected_tile = ''
                        else:
                            selected_tile = ''
                    elif event.button == 3:
                        selected_tile = ''
                    elif event.button == 4 and self.zoom > 0.2:
                        self.zoom -= self.zoom/2
                    elif event.button == 5:
                        self.zoom += self.zoom

            keys = pygame.key.get_pressed()
            angle_rad = math.radians(self.angle)
            cos = math.cos(angle_rad)
            sin = math.sin(angle_rad)
            rcamera = [self.camera_pos[0]*cos - self.camera_pos[1]*sin, self.camera_pos[0]*sin + self.camera_pos[1]*cos, self.camera_pos[2]]
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                rcamera[1] += 0.3 * self.zoom / 5
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and not (keys[pygame.K_LCTRL] or keys[pygame.K_LMETA]):
                rcamera[1] -= 0.3 * self.zoom / 5
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                rcamera[0] += 0.3 * self.zoom / 5
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                rcamera[0] -= 0.3 * self.zoom / 5
            if keys[pygame.K_x] and self.zoom > 0.2:
                self.zoom -= self.zoom / 20
            if keys[pygame.K_z]:
                self.zoom += self.zoom / 20
            if keys[pygame.K_q]:
                self.angle += 1
            if keys[pygame.K_e]:
                self.angle -= 1
            if keys[pygame.K_r]:
                self.angle = 0
            if keys[pygame.K_s] and (keys[pygame.K_LCTRL] or keys[pygame.K_LMETA]) and not saved:
                now = datetime.now()
                default_save_name = now.strftime("%Y-%m-%d_%H-%M-%S")
                save_file_name = GraphRenderEngine.get_save_file_name(default_save_name)
                if save_file_name:
                    self.save(save_file_name, 'saves')
                    saved = True
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                return self.rule_engine.turn_order[0], turn

            self.camera_pos = [rcamera[0]*cos + rcamera[1]*sin, -rcamera[0]*sin + rcamera[1]*cos, rcamera[2]]

            if selected_tile != '':
                highlight_tiles = [move[0] for move in self.rule_engine.get_legal_moves(selected_tile, self.board)]
            elif hover_tile != '':
                highlight_tiles = [move[0] for move in self.rule_engine.get_legal_moves(hover_tile, self.board)]
            else: 
                highlight_tiles = []

            if len(self.rule_engine.turn_order) > 1:
                glClearColor(0.7, 0.8, 0.9, 1.0) # light blue-gray
            elif len(self.rule_engine.turn_order) == 1:
                team_color = self.rule_engine.teams[self.rule_engine.turn_order[0]].color
                tchsv = colorsys.rgb_to_hsv(*team_color)
                team_color = colorsys.hsv_to_rgb(tchsv[0], tchsv[1]*0.25, 1 - (1 - tchsv[2])*0.5)
                glClearColor(*team_color, 1.0)
            else:
                color = colorsys.rgb_to_hsv(0.7, 0.8, 0.9)
                color = colorsys.hsv_to_rgb(color[0], 0.0, color[2])
                glClearColor(*color, 1.0)
            self.draw_boarder(self.zoom, *self.camera_pos)
            quads = self.draw_board(self.tile_textures, self.zoom, highlight_tiles, selected_tile, hover_tile, *self.camera_pos)
            self.draw_pieces(self.piece_textures, self.zoom, self.camera_pos, self.angle)
            pygame.display.flip()

            if self.rule_engine.turn_order:
                current_team = self.rule_engine.turn_order[self.board.current_team_index]
            else:
                current_team = None

            if self.rule_engine.turn_order:
                lose_condition = self.rule_engine.lose[current_team]
                royal_tiles_count = len(self.board.royal_tiles[current_team])

                if lose_condition == 'eliminate_royals' and not royal_tiles_count:
                    msg = f"all of {current_team}'s royal pieces were eliminated"
                elif lose_condition == 'eliminate_any_royal' and royal_tiles_count < self.team_royal_numbers[current_team]:
                    msg = f"one of {current_team}'s royal pieces was eliminated"
                elif not self.board.get_team_pieces(current_team):
                    msg = f"all of {current_team}'s pieces were eliminated"
                else:
                    msg = None

                if msg != None:
                    self.rule_engine.turn_order.remove(current_team)
                    print(msg)
                    if self.rule_engine.turn_order:
                        self.board.current_team_index %= len(self.rule_engine.turn_order)

            if current_team in self.ai_teams and frame % self.ai_turn_delay == 0 and len(self.rule_engine.turn_order) > 1:
                if self.board.current_team_index == len(self.rule_engine.turn_order) - 1:
                    turn += 1
                self.board = self.rule_engine.ai_play(self.board, self.ai_teams[current_team], False)
                saved = False

            mvMat = glGetDoublev(GL_MODELVIEW_MATRIX)
            prjMat = glGetDoublev(GL_PROJECTION_MATRIX)
            
            mouse = pygame.mouse.get_pos()

            if quads:
                for tile, quad in quads.items():
                    try:
                        if self.board.get_node_tile(tile).not_selectable:
                            continue
                    except:
                        pass
                    if GraphRenderEngine.TestRec(mvMat, prjMat, mouse, self.display, self.zoom, quad):
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
