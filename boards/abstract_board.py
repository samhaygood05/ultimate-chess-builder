from abc import ABC, abstractmethod

class AbstractBoard(ABC):

    def tile_to_index(tile):
        column = tile[0]
        row = int(tile[1:])-1
        column_index = ord(column.lower()) - 97
        return row, column_index

    def index_to_tile(row, column):
        return chr(column + 97) + str(row+1)
    
    @abstractmethod
    def get_tile(self, tile):
        pass

    @abstractmethod
    def copy(self):
        pass