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

class Move:
    def __init__(self, *sequence, end_direction: str = 'f') -> None:
        self.sequence = sequence
        self.end_direction = end_direction

    def get_end_position(self, board, start_position, start_direction):
        end_direction = self.end_direction
        current_position = start_position
        current_direction = start_direction
        for relative_direction, type in self.sequence:
            if type in board.directions.included_adjacency_types:
                new_direction = board.get_direction_from_relative(current_direction, relative_direction)
            else:
                new_direction = relative_direction
            adjacencies = board.get_node_adjacencies(current_position, type)
            try:
                new_position = adjacencies[new_direction][1]
                change_direction = adjacencies[new_direction][2]
                if change_direction != None and change_direction != 'f':
                    new_direction = board.get_direction_from_relative(new_direction, change_direction)
                    end_direction = change_direction
            except KeyError:
                return None, None, None
            current_position = new_position
            current_direction = new_direction
        
        return current_position, board.get_direction_from_relative(start_direction, end_direction), new_direction

    def __str__(self) -> str:
        return " -> ".join([f"{direction} ({type})" for direction, type in self.sequence])
    
    def __repr__(self) -> str:
        return f'Move({self.sequence})'
    
