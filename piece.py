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

class Piece:
    def __init__(self, name, team, facing, is_royal=None, has_moved=False, secondary_team=None, trinary_team=None, quadinary_team=None):
        self.name = name
        self.team = team
        self.facing = facing

        self.has_moved = has_moved

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
            self.is_royal = (self.name == 'king')
        else:
            self.is_royal = is_royal

        

    def moved(self):
        self.has_moved = True
        return self

    def promote(self, promotion):
        self.name = promotion
        return self
    
    def get_allies_intersection(self, teams):
        team = teams[self.team]
        secondary_team = teams[self.secondary_team]
        trinary_team = teams[self.trinary_team]
        quadinary_team = teams[self.quadinary_team]
        return list(set(team.allies) & set(secondary_team.allies) & set(trinary_team.allies) & set(quadinary_team.allies))

    def get_allies_union(self, teams):
        team = teams[self.team]
        secondary_team = teams[self.secondary_team]
        trinary_team = teams[self.trinary_team]
        quadinary_team = teams[self.quadinary_team]
        return list(set(team.allies) | set(secondary_team.allies) | set(trinary_team.allies) | set(quadinary_team.allies))

    def is_allies(self, allies, inclusive):
        if inclusive:
            return list(set(self.get_team_names()) & set(allies))
        else:
            return not list(set(self.get_team_names()) ^ set(allies))

    def get_team_names(self):
        return list(set([self.team, self.secondary_team, self.trinary_team, self.quadinary_team]))
    
    def __str__(self) -> str:
        return f'{self.team} {self.name} -> {self.facing}'
