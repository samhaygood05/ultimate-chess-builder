'''
Copyright 2024 Sam A. Haygood

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

import json

class TeamType:
    def __init__(self, name, properties={}, instance_properties={}):
        self.name = name
        self.properties = properties
        self.instance_properties = instance_properties

    @staticmethod
    def build(file_path) -> 'TeamType':
        try:
            with open(file_path, 'r') as file:
                # make sure the file path has the right structure: ../{namespace}/data/teams/{name}.json
                split_path = file_path.split('/')
                if split_path[-2] != 'teams' or split_path[-3] != 'data' or split_path[-1].split('.')[-1] != 'json':
                    raise ValueError('Invalid file path for team type')

                data = json.load(file)
                # use file_path to get the name of the tile type
                namespace = split_path[-4]
                name = split_path[-1].split('.')[0]
                properties = {}
                instance_properties = {}
                if 'properties' in data:
                    properties = data['properties']
                if 'instance_properties' in data:
                    instance_properties = data['instance_properties']
                return TeamType(f'{namespace}:{name}', properties, instance_properties)
        except Exception as e:
            print(f"Error building team type: {e}")
            return None

class Team:
    def __init__(self, name: str, type: str, allies=None, color=0xFFFFFF, board_color=0xFFFFFF, team_types={}, **properties):
        self.name = name
        self.type = type
        self.allies = [name]
        if allies != None:
            self.allies.extend(allies)
        self.color = color
        self.board_color = board_color
        self.is_ai = False

        self.properties = {}
        if len(team_types) == 0:
            self.properties = properties
        else:
            team_properties = team_types[type].instance_properties
            for key in properties:
                if key in team_properties:
                    self.properties[key] = properties[key]
                else:
                    raise ValueError(f"Invalid property: {key}")
                
            for key in team_properties:
                if key not in self.properties:
                    self.properties[key] = team_properties[key]
        
    def __copy__(self):
        return Team(self.name, self.type, None if self.allies == None else self.allies[1:], self.color, self.board_color, {}, **self.properties)


    def add_ally(self, ally):
        self.allies.append(ally)

    def remove_ally(self, ally):
        try:
            self.allies.remove(ally)
        except:
            pass

    def make_ai(self):
        self.is_ai = True
        return self