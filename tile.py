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
from teams.team import TeamPresets as tp
from PIL import Image
import os

class Tile:
    def __init__(self, piece=None, team=None, secondary_team=None, trinary_team=None, quadinary_team=None, is_royal=None, has_moved=False):
        if piece == None:
            self.piece = 'empty'
        else:
            self.piece = piece
        self.has_moved = has_moved

        if team == None:
            self.team = tp.EMPTY
        else:
            self.team = team
        if secondary_team == None:
            self.secondary_team = self.team
        else:
            self.secondary_team = secondary_team
        if trinary_team == None:
            self.trinary_team = self.team
        else:
            self.trinary_team = trinary_team
        if quadinary_team == None:
            self.quadinary_team = self.secondary_team
        else:
            self.quadinary_team = quadinary_team
        
        if is_royal == None:
            self.is_royal = (self.piece == 'king')
        else:
            self.is_royal = is_royal
    
    def moved(self):
        self.has_moved = True
        return self

    def promote(self, promotion):
        self.piece = promotion
        return self
    
    def get_allies_intersection(self):
        return list(set(self.team.allies) & set(self.secondary_team.allies) & set(self.trinary_team.allies) & set(self.quadinary_team.allies))

    def get_allies_union(self):
        return list(set(self.team.allies).union(set(self.secondary_team.allies)).union(set(self.trinary_team.allies)).union(set(self.quadinary_team.allies)))

    def is_allies(self, allies):
        return list(set(self.get_team_names()) & set(allies))

    def get_team_names(self):
        return [self.team.name, self.secondary_team.name, self.trinary_team.name, self.quadinary_team.name]

    def __str__(self) -> str:
        return f"{self.team.name} {self.piece}"

    def __repr__(self) -> str:
        return f"{self.team.name} {self.piece}"