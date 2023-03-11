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
from team import Team
from tile import Tile
from rule_set import RuleSet
import pygame
import copy

class Board:
    def __init__(self, white_first=True, board_state=None, rulesets=None):
        if board_state == None:
            self.board = [[Tile('rook', Team.WHITE), Tile('knight', Team.WHITE), Tile('bishop', Team.WHITE), Tile('queen', Team.WHITE), Tile('king', Team.WHITE), Tile('bishop', Team.WHITE), Tile('knight', Team.WHITE), Tile('rook', Team.WHITE)],
                            [Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE), Tile('pawn', Team.WHITE)],
                            [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                            [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                            [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                            [Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()],
                            [Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK), Tile('pawn', Team.BLACK)],
                            [Tile('rook', Team.BLACK), Tile('knight', Team.BLACK), Tile('bishop', Team.BLACK), Tile('queen', Team.BLACK), Tile('king', Team.BLACK), Tile('bishop', Team.BLACK), Tile('knight', Team.BLACK), Tile('rook', Team.BLACK)]]
        else:
            self.board = board_state

        self.white_first = white_first
        self.rulesets = RuleSet.rule_dict(
            RuleSet('pawn', [(1, 0)], [(1, -1), (1, 1)], True, False, True, 'queen'),
            RuleSet('rook', [(0, 1), (0, -1), (1, 0), (-1, 0)], None, False, True, False),
            RuleSet('bishop', [(-1, -1), (-1, 1), (1, -1), (1, 1)], None, False, True, False),
            RuleSet('knight', [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)], None, False, False, False),
            RuleSet('queen', [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], None, False, True, False),
            RuleSet('king', [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], None, False, False, False)
        )
        if rulesets != None:
            self.rulesets.update(rulesets)

    def copy(self):
        copy_board = Board(copy.deepcopy(self.board), self.white_first, self.rulesets)
        return copy_board

    def tile_to_index(tile):
        column = tile[0]
        row = int(tile[1:])-1
        column_index = ord(column.lower()) - 97
        return row, column_index

    def index_to_tile(row, column):
        return chr(column + 97) + str(row+1)

    def get_tile(self, tile):
        row, column = Board.tile_to_index(tile)
        try:
            return self.board[row][column]
        except:
            print('Not a valid tile')
            return Tile()

    def add_ruleset(self, tile, ruleset: RuleSet):
        piece = self.get_tile(tile)
        team = piece.team
        piece_name = ruleset.name
        moveset = ruleset.moveset
        captureset = ruleset.captureset
        first_move = ruleset.first_move
        multimove = ruleset.multimove
        directional = ruleset.directional

        if captureset == None:
            captureset = moveset
        enemy = Team.EMPTY
        if team == Team.WHITE:
            enemy = Team.BLACK
        elif team == Team.BLACK:
            enemy = Team.WHITE
        row, col = Board.tile_to_index(tile)
        legal_moves = []
        direction = 1
        if directional and team == Team.BLACK:
            direction = -1

        if piece.piece == piece_name:
            # Logic for Moveset
            for delta_row, delta_col in moveset:
                new_row = row + delta_row*direction
                new_col = col + delta_col
                if multimove:
                    while (new_row in range(len(self.board))) and (new_col in range(len(self.board[new_row]))):
                        target = self.board[new_row][new_col]
                        if target == None:
                            break
                        if target.piece == 'empty':
                            legal_moves.append(Board.index_to_tile(new_row, new_col))
                        else:
                            break
                        new_row += delta_row*direction
                        new_col += delta_col
                else:
                    if (new_row in range(len(self.board))) and (new_col in range(len(self.board[new_row]))):
                        target = self.board[new_row][new_col]
                        if target != None:
                            if target.piece == 'empty':
                                legal_moves.append(Board.index_to_tile(new_row, new_col))
                                if first_move and not piece.has_moved:
                                    while new_row < len(self.board) / 2 - 1 or new_row > len(self.board) / 2:
                                        new_row += delta_row*direction
                                        new_col += delta_col
                                        try:
                                            target = self.board[new_row][new_col]
                                            if target.piece == 'empty':
                                                legal_moves.append(Board.index_to_tile(new_row, new_col ))
                                        except:
                                            break
            # Logic for Capture Set
            for delta_row, delta_col in captureset:
                new_row = row + delta_row*direction
                new_col = col + delta_col
                if multimove:
                    while (new_row in range(len(self.board))) and (new_col in range(len(self.board[new_row]))):
                        target = self.board[new_row][new_col]
                        if target == None:
                            break
                        if target.piece == 'empty':
                            pass
                        elif target.team == enemy:
                            legal_moves.append(Board.index_to_tile(new_row, new_col))
                            break
                        else:
                            break
                        new_row += delta_row*direction
                        new_col += delta_col
                else:
                    if (new_row in range(len(self.board))) and (new_col in range(len(self.board[new_row]))):
                        target = self.board[new_row][new_col]
                        if target != None:
                            if target.team == enemy:
                                legal_moves.append(Board.index_to_tile(new_row, new_col))
        return legal_moves


    def get_legal_moves(self, tile):
        piece = self.get_tile(tile)
        legal_moves = []

        # None Tiles
        if piece == None:
            return legal_moves

        # Empy Tile
        if piece.piece == 'empty':
            return legal_moves

        # All Other Pieces
        for name, rules in self.rulesets.items():
            legal_moves.extend(self.add_ruleset(tile, rules))

        return legal_moves

    def get_legal_moves_no_check(self, tile):
        legal_moves = self.get_legal_moves(tile)
        if not legal_moves:
            return []
        i = 0
        while i < len(legal_moves):
            copy_board = self.copy()
            copy_board.play_move(tile, legal_moves[i])
            if copy_board.is_in_check(self.get_tile(tile).team):
                legal_moves.remove(i)
            else:
                i += 1
        return legal_moves

    def is_in_check(self, team):
        royal_pieces = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                tile = self.board[row][col]
                if team == tile.team and tile.is_royal:
                    royal_pieces.extend(self.index_to_tile(row, col))
        if team == Team.WHITE:
            enemy = Team.BLACK
        elif team == Team.BLACK:
            ememy = Team.WHITE
        return not set(royal_pieces).isdisjoint(self.all_legal_moves(enemy))
    
    def all_legal_moves(self, team):
        legal_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                tile = self.board[row][col]
                if team == tile.team:
                    legal_moves.extend(self.get_legal_moves(tile))
        return legal_moves


    def play_move(self, start_tile, end_tile, illegal_moves=False):
        if self.white_first:
            current_team = Team.WHITE
        else:
            current_team = Team.BLACK
        if not illegal_moves:
            legal_moves = self.get_legal_moves(start_tile)
            if end_tile not in legal_moves:
                print("Illegal Move")
                return self
        
        if self.get_tile(start_tile).team != current_team:
            print("You Can't Play Your Opponent's Pieces")
            return self
            
        start = Board.tile_to_index(start_tile)
        end = Board.tile_to_index(end_tile)

        piece = self.get_tile(start_tile).piece

        new_board = self.board
        new_board[end[0]][end[1]] = self.get_tile(start_tile).moved()
        new_board[start[0]][start[1]] = Tile()

        ruleset = self.rulesets[piece]
        promotion, promotion_row = ruleset.promotion, ruleset.promotion_row
        if promotion != None:
            if (end[0] == len(self.board) - 1 - promotion_row and current_team == Team.WHITE) or (end[0] == promotion_row and current_team == Team.BLACK):
                new_board[end[0]][end[1]] = new_board[end[0]][end[1]].promote(promotion)

        self.board = new_board
        self.white_first = not self.white_first
        return self

    def draw_board(self, screen, font, color1, color2, text_color, tile_size):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                # Calculate the position of the tile
                x = (col + 1) * tile_size
                y = row * tile_size

                # Draw the tile
                color = color1 if (row + col) % 2 == 0 else color2
                pygame.draw.rect(screen, color, [x, y, tile_size, tile_size])

        for row in range(len(self.board)):
            y = row * tile_size

            # Draw the tile coordinates
            text = font.render(f"{len(self.board)-row}", True, text_color)
            screen.blit(text, (tile_size*0.5, y+tile_size*0.4))

        for col in range(len(self.board[0])):
            x = (col + 1) * tile_size

            # Draw the tile coordinates
            text = font.render(f"{chr(97+col)}", True, text_color)
            screen.blit(text, (x+tile_size*0.4, len(self.board)*tile_size+tile_size*0.4))

    def highlight_tiles(self, tiles, screen, highlight_color=(255, 255, 0, 128), tile_size=90):
        for tile in tiles:
            row, col = Board.tile_to_index(tile)
            x = (col + 1) * tile_size
            y = (len(self.board) - 1 - row) * tile_size

            s = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            s.fill(highlight_color) 
            screen.blit(s, (x,y))


    def draw_pieces(self, screen, tile_size=90):

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                # Calculate the position of the tile
                x = (col + 1) * tile_size
                y = row * tile_size

                # Draw the piece
                piece = self.board[len(self.board) - 1 - row][col]
                if piece != None:
                    if piece.piece != 'empty':
                            filename = piece.get_file_name()
                            try:
                                image = pygame.transform.scale(pygame.image.load(filename), (tile_size, tile_size))
                            except:
                                image = pygame.Surface((tile_size*0.75, tile_size*0.75))
                                if piece.team == Team.BLACK:
                                    image.fill((0, 0, 0))
                                else:
                                    image.fill((255, 255, 200))
                            screen.blit(image, (x, y))
                else:
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill((0, 0, 0))
                    screen.blit(image, (x, y))

    def render_board(self, tile_size=90, color1=(255, 255, 255), color2=(128, 128, 128), text_color=(0, 0, 0), highlight_color=(255, 255, 0, 128), illegal_moves=False):

        # Initialize Pygame
        pygame.init()

        # Set the size of the window and the size of each tile
        WINDOW_SIZE = ((len(self.board[0])+1)*tile_size, (len(self.board)+1)*tile_size)

        # Create the window
        screen = pygame.display.set_mode(WINDOW_SIZE)

        # Create a font for drawing text
        font = pygame.font.Font(None, 24)

        if self.white_first:
            turn = "White's Turn"
        else:
            turn = "Black's Turn"
        pygame.display.set_caption(turn)

        icon = pygame.image.load('images/white/pawn.png')
        pygame.display.set_icon(icon)

        screen.fill(color1)

        running = True

        legal_moves = []
        selected_tile = []
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEMOTION:
                    if not selected_tile:
                        # get the mouse position
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        tile_x = (mouse_x // tile_size) - 1
                        tile_y = len(self.board) - 1 - (mouse_y // tile_size)

                        if tile_x in range(len(self.board)) and tile_y in range(len(self.board[0])):
                            hovered_tile = Board.index_to_tile(tile_y, tile_x)
                            legal_moves = self.get_legal_moves(hovered_tile)
                    else:
                        legal_moves = self.get_legal_moves(selected_tile[0])

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # get the mouse position
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        tile_x = (mouse_x // tile_size) - 1
                        tile_y = len(self.board) - 1 - (mouse_y // tile_size)
                        
                        if tile_x in range(len(self.board)) and tile_y in range(len(self.board[0])):
                            clicked_tile = Board.index_to_tile(tile_y, tile_x)

                            if not selected_tile:
                                if self.get_tile(clicked_tile).piece != 'empty':
                                    selected_tile = [clicked_tile]
                                    legal_moves = self.get_legal_moves(clicked_tile)
                            else:
                                self.play_move(selected_tile[0], clicked_tile, illegal_moves)
                                if self.white_first:
                                    turn = "White's Turn"
                                else:
                                    turn = "Black's Turn"
                                pygame.display.set_caption(turn)
                                selected_tile = []

                    elif event.button == 3:
                        selected_tile = []

            # Draw the chessboard
            self.draw_board(screen, font, color1, color2, text_color, tile_size)

            # Highlight Valid Moves
            self.highlight_tiles(legal_moves, screen, highlight_color, tile_size)

            # Highlight Selected Tile
            self.highlight_tiles(selected_tile, screen, (0, 255, 255, 128), tile_size)

            # Draw Pieces
            self.draw_pieces(screen, tile_size)

            # Update the screen
            pygame.display.update()

        # Quit Pygame
        pygame.quit()
