'''
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from boards.abstract_board import AbstractBoard
from boards.square_board import SquareBoard
from tile import Tile
from variants import Variants
from teams.time_team import TimeTeamPresets as tp
import copy

class PolyBoard(AbstractBoard):
    def __init__(self, boards: dict = None, active_boards: list=None):
        if boards == None:
            self.boards = {(0,0): SquareBoard(board_state=Variants.create_standard_board(tp.WHITE, tp.BLACK, 4))}
        else:
            self.boards = boards
        if active_boards == None:
            self.active_boards = [(0,0)]
        else:
            self.active_boards = active_boards

    def get_tile(self, board, tile):
        try:
            return self.boards[board].get_tile(tile)
        except:
            print('Not a valid board')
            return Tile()
        
    def add_board(self, board_loc: tuple, board: AbstractBoard):
        self.boards[board_loc] = board
        return self

    def copy(self):

        copy_boards = dict()
        for loc, board in self.boards.items():
            copy_boards[loc] = board

        copy_board = PolyBoard(copy_boards, copy.deepcopy(self.active_boards))