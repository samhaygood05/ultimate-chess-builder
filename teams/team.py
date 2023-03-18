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

from teams.abstract_team import AbstractTeam

class Team(AbstractTeam):
    def __init__(self, name, direction, allies=None, color=(1.0, 1.0, 1.0), is_ai=False):
        self.name = name
        self.direction = direction
        self.perpendicular = (direction[1], -direction[0])
        self.allies = ['empty', name]
        if allies != None:
            self.allies.extend(allies)
        self.color = color
        self.is_ai = is_ai

class TeamPresets:
    WHITE = Team('white', (1, 0))
    BLACK = Team('black', (-1, 0), (0.0, 0.0, 0.0))
    RED = Team('red', (0, 1), color=(1.0, 0.0, 0.0))
    GREEN = Team('green', (0, -1), color=(0.0, 1.0, 0.0))
    EMPTY = Team('empty', (0,0))