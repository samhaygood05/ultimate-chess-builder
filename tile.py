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
from team import Team

class Tile:
    def __init__(self, piece=None, team=None, is_royal=None, has_moved=False):
        if piece == None:
            self.piece = 'empty'
        else:
            self.piece = piece
        self.has_moved = has_moved
        if team == None:
            self.team = Team.EMPTY
        else:
            self.team = team
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
    
    def get_file_name(self):
        if self.team == Team.WHITE:
            file = f"images/white/{self.piece}.png"
        elif self.team == Team.BLACK:
            file = f"images/black/{self.piece}.png"
        return file

    def __str__(self) -> str:
        return f"{self.team} {self.piece}"

    def __repr__(self) -> str:
        return f"{self.team} {self.piece}"