'''
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from board import Board
from tile import Tile

class PolyBoard:
    def __init__(self, boards: dict = None, active_boards: list=None):
        if boards == None:
            self.boards = {(0,0): Board()}
        else:
            self.boards = boards
        if active_boards == None:
            self.active_boards = [(0,0)]
        else:
            self.active_boards = active_boards

    def get_tile(self, tile_loc):
        board, tile = tile_loc
        try:
            return self.boards[board].get_tile(tile)
        except:
            print('Not a valid board')
            return Tile()
        
    def add_board(self, board_loc: tuple, board: Board):
        self.boards[board_loc] = board