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
import pygame as pg
from OpenGL.GL import *
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

        # Initialize Pygame
        pg.init()

        # Define OpenGL version
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(screen_size, pg.OPENGL|pg.DOUBLEBUF)

        self.clock = pg.time.Clock()

        glClearColor(1.0, 1.0, 1.0, 1.0)

        self.main_loop()
    
    def draw_board(self, screen, font, color1, color2, text_color, tile_size):
        pass

    def highlight_tiles(self, tiles, screen, highlight_color=(255, 255, 0, 128), tile_size=90):
        pass

    def draw_pieces(self, screen, tile_size=90):
        pass
    
    def main_loop(self) -> None:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running == False

            glClear(GL_COLOR_BUFFER_BIT)

            pg.display.flip()

            #timing
            self.clock.tick(60)
        self.quit()


    def __str__(self) -> str:
        return f"Board: {self.board}\nRules: {self.rule_engine}"
