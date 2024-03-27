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


class Move:
    def __init__(self, sequence, end_direction: str = 'forward', min_distance: int = 1, max_distance: int = -1):
        self.sequence = sequence
        self.end_direction = end_direction
        if min_distance < 1:
            raise ValueError('min_distance must be greater than 0')
        self.min_distance = min_distance
        if max_distance != -1 and max_distance < min_distance:
            raise ValueError('max_distance must be greater than or equal to min_distance')
        self.max_distance = max_distance

    @staticmethod
    def build(dictionary: dict) -> 'Move':
        sequence = dictionary['sequence']
        end_direction = "forward"
        if 'end' in dictionary:
            end_direction = dictionary['end']
        return Move(sequence, end_direction=end_direction)
    
    def __str__(self) -> str:
        string = "move\n ├ sequence:\n"
        for step, i in zip(self.sequence, range(len(self.sequence))):
            if i == len(self.sequence) - 1:
                string += f" │ └ {step}\n"
            else:
                string += f" │ ├ {step}\n"
        string += f" ├ end: {self.end_direction}"
        if self.max_distance != -1:
            string += f"\n └ range: [{self.min_distance}, {self.max_distance}]"
        else:
            string += f"\n └ range: [{self.min_distance}, ∞)"
        return string

        