'''
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from abc import ABC, abstractmethod

class AbstractBoard(ABC):

    @staticmethod
    def tile_to_index(tile):
        column = tile[0]
        row = int(tile[1:])-1
        column_index = ord(column.lower()) - 97
        return row, column_index

    @staticmethod
    def index_to_tile(row, column):
        return chr(column + 97) + str(row+1)
    
    @abstractmethod
    def get_tile(self, tile):
        pass

    @abstractmethod
    def copy(self):
        pass