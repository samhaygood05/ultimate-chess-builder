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

from teams import AbstractTeam

class Team(AbstractTeam):
    def __init__(self, name, allies=None, color=(1.0, 1.0, 1.0)):
        self.name = name
        self.allies = ['empty', name]
        if allies != None:
            self.allies.extend(allies)
        self.color = color

class TeamPresets:
    WHITE = Team('white')
    BLACK = Team('black', color=(0.0, 0.0, 0.0))
    RED = Team('red', color=(1.0, 0.0, 0.0))
    GREEN = Team('green', color=(0.0, 1.0, 0.0))
    EMPTY = Team('empty')