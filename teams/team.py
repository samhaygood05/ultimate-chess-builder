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

import os
from PIL import Image
from teams.abstract_team import AbstractTeam

class Team(AbstractTeam):
    def __init__(self, name, direction, allies=None, hue=0):
        self.name = name
        self.direction = direction
        self.perpendicular = (direction[1], -direction[0])
        self.allies = ['empty', name]
        if allies != None:
            self.allies.extend(allies)
        self.hue = hue

        img_folder = f'{os.getcwd()}/images'.replace('\\', '/')
        teams = os.listdir(img_folder)
        if self != None:
            if self.name not in teams and self.name != 'empty':
                pieces = os.listdir(f'{img_folder}/red')
                os.mkdir(f'{img_folder}/{self.name}')
                for piece_name in pieces:
                    image = Image.open(f'{img_folder}/red/{piece_name}')
                    image = image.convert('RGBA')

                    hsv_image = image.convert('HSV')

                    hue_shift = self.hue / 360.0
                    h, s, v = hsv_image.split()
                    r, g, b, a = image.split()
                    h = h.point(lambda i: (i + hue_shift) % 1.0 * 255)

                    rgb_image = Image.merge('HSV', (h, s, v)).convert('RGB')

                    r, g, b = rgb_image.split()
                    edited_img = Image.merge('RGBA', (r, g, b, a))

                    edited_img.save(f'{img_folder}/{self.name}/{piece_name}')

class TeamPresets:
    WHITE = Team('white', (1, 0))
    BLACK = Team('black', (-1, 0))
    RED = Team('red', (0, 1))
    GREEN = Team('green', (0, -1), hue=120)
    EMPTY = Team('empty', (0,0))