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
from team import TeamPresets as tp
from PIL import Image
import colorsys
import os

class Tile:
    def __init__(self, piece=None, team=None, is_royal=None, has_moved=False):
        if piece == None:
            self.piece = 'empty'
        else:
            self.piece = piece
        self.has_moved = has_moved
        if team == None:
            self.team = tp.EMPTY
        else:
            self.team = team
        if is_royal == None:
            self.is_royal = (self.piece == 'king')
        else:
            self.is_royal = is_royal
        
        img_folder = f'{os.getcwd()}\\images'
        teams = os.listdir(img_folder)
        if team != None:
            if team.name not in teams:
                print(f'Creating {team.name} files')

                pieces = os.listdir(f'{img_folder}\\red')
                os.mkdir(f'{img_folder}\\{team.name}')
                for piece_name in pieces:
                    print(f'Creating {team.name}/{piece_name}')
                    image = Image.open(f'{img_folder}\\red\\{piece_name}')
                    image = image.convert('RGBA')

                    hsv_image = image.convert('HSV')

                    hue_shift = team.hue / 360.0
                    h, s, v = hsv_image.split()
                    r, g, b, a = image.split()
                    h = h.point(lambda i: (i + hue_shift) % 1.0 * 255)

                    rgb_image = Image.merge('HSV', (h, s, v)).convert('RGB')

                    r, g, b = rgb_image.split()
                    edited_img = Image.merge('RGBA', (r, g, b, a))

                    edited_img.save(f'{img_folder}\\{team.name}\\{piece_name}')
                    print(f'{team.name}/{piece_name} created successfully')
                
                print(f'{team.name} files created successfully')
    
    def moved(self):
        self.has_moved = True
        return self

    def promote(self, promotion):
        self.piece = promotion
        return self
    
    def get_file_name(self):
        return f"images/{self.team.name}/{self.piece}.png"

    def __str__(self) -> str:
        return f"{self.team.name} {self.piece}"

    def __repr__(self) -> str:
        return f"{self.team.name} {self.piece}"