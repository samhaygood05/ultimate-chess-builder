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

class TimeTeam(AbstractTeam):
    def __init__(self, name, direction, time_direction, allies=None, color=(1.0, 1.0, 1.0), is_ai=False):
        self.name = name
        self.direction = direction
        self.perpendicular = (direction[1], -direction[0])
        self.time_direction = time_direction
        self.allies = ['empty', name]
        if allies != None:
            self.allies.extend(allies)
        self.color = color
        self.is_ai = is_ai

class TimeTeamPresets:
    WHITE = TimeTeam('white', (1, 0), 1)
    BLACK = TimeTeam('black', (-1, 0), -1, color=(0.0, 0.0, 0.0))