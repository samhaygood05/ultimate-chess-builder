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

from hashlib import new


class Move:
    def __init__(self, *sequence, end_direction: str = 'f') -> None:
        self.sequence = sequence
        self.end_direction = end_direction

    def get_intermediate_position(self, board, start_positions, i):
        relative_direction, type = self.sequence[i]
        end_positions = []
        for start_position, start_direction, end_direction in start_positions:
            if type in board.directions.included_adjacency_types:
                new_direction = board.get_direction_from_relative(start_direction, relative_direction)
            else:
                new_direction = relative_direction
            adjacencies = board.get_node_adjacencies(start_position, type)
            try:
                new_positions = adjacencies[new_direction]
                for position in new_positions:
                    new_position = position[1]
                    change_direction = position[2]
                    if change_direction != None and change_direction != 'f':
                        new_direction = board.get_direction_from_relative(new_direction, change_direction)
                        end_direction = change_direction
                    end_positions.append((new_position, new_direction, end_direction))
            except KeyError:
                pass
        return end_positions


    def get_end_position(self, board, start_position, start_direction):
        end_direction = self.end_direction
        change_directions = []
        current_position = start_position
        current_direction = start_direction
        for relative_direction, type in self.sequence:
            if type in board.directions.included_adjacency_types:
                new_direction = board.get_direction_from_relative(current_direction, relative_direction)
            else:
                new_direction = relative_direction
            adjacencies = board.get_node_adjacencies(current_position, type)
            try:
                new_position = adjacencies[new_direction][0][1]
                change_direction = adjacencies[new_direction][0][2]
                if change_direction != None and change_direction != 'f':
                    new_direction = board.get_direction_from_relative(new_direction, change_direction)
                    change_directions.append(change_direction)
            except KeyError:
                return None, None, None
            current_position = new_position
            current_direction = new_direction
        
        end_direction_final = start_direction
        for direction in change_directions:
            end_direction_final = board.get_direction_from_relative(end_direction_final, direction)
        end_direction_final = board.get_direction_from_relative(end_direction_final, end_direction)
        
        
        return current_position, end_direction_final, new_direction

    def __str__(self) -> str:
        return " -> ".join([f"{direction} ({type})" for direction, type in self.sequence])
    
    def __repr__(self) -> str:
        return f'Move({self.sequence})'
    
