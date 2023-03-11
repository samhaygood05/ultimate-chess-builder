from rule_engine import RuleEngine
from board import Board
from team import TeamPresets as tp
import pygame

class RenderEngine:
    def __init__(self, board: Board = None, rule_engine: RuleEngine = None):
        if board == None:
            self.board = Board()
        else:
            self.board = board
        if rule_engine == None:
            self.rule_engine = RuleEngine()
        else:
            self.rule_engine = rule_engine
    
    def draw_board(self, screen, font, color1, color2, text_color, tile_size):
        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[row])):
                # Calculate the position of the tile
                x = (col + 1) * tile_size
                y = row * tile_size

                # Draw the tile
                color = color1 if (row + col) % 2 == 0 else color2
                pygame.draw.rect(screen, color, [x, y, tile_size, tile_size])

        for row in range(len(self.board.board)):
            y = row * tile_size

            # Draw the tile coordinates
            text = font.render(f"{len(self.board.board)-row}", True, text_color)
            screen.blit(text, (tile_size*0.5, y+tile_size*0.4))

        for col in range(len(self.board.board[0])):
            x = (col + 1) * tile_size

            # Draw the tile coordinates
            text = font.render(f"{chr(97+col)}", True, text_color)
            screen.blit(text, (x+tile_size*0.4, len(self.board.board)*tile_size+tile_size*0.4))

    def highlight_tiles(self, tiles, screen, highlight_color=(255, 255, 0, 128), tile_size=90):
        for tile in tiles:
            row, col = Board.tile_to_index(tile)
            x = (col + 1) * tile_size
            y = (len(self.board.board) - 1 - row) * tile_size

            s = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            s.fill(highlight_color) 
            screen.blit(s, (x,y))


    def draw_pieces(self, screen, tile_size=90):

        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[row])):
                # Calculate the position of the tile
                x = (col + 1) * tile_size
                y = row * tile_size

                # Draw the piece
                piece = self.board.board[len(self.board.board) - 1 - row][col]
                if piece != None:
                    if piece.piece != 'empty':
                            filename = piece.get_file_name()
                            try:
                                image = pygame.transform.scale(pygame.image.load(filename), (tile_size, tile_size))
                            except:
                                image = pygame.Surface((tile_size*0.75, tile_size*0.75))
                                if piece.team == tp.BLACK:
                                    image.fill((0, 0, 0))
                                else:
                                    image.fill((255, 255, 200))
                            screen.blit(image, (x, y))
                else:
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill((0, 0, 0))
                    screen.blit(image, (x, y))

    def render_static(self, legal_moves, selected_tile, tile_size=90, color1=(255, 255, 255), color2=(128, 128, 128), text_color=(0, 0, 0), highlight_color=(255, 255, 0, 128)):
        # Set the size of the window and the size of each tile
        WINDOW_SIZE = ((len(self.board.board[0])+1)*tile_size, (len(self.board.board)+1)*tile_size)

        # Create the window
        screen = pygame.display.set_mode(WINDOW_SIZE)

        # Create a font for drawing text
        font = pygame.font.Font(None, 24)
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

        return screen
    
    def render_board(self, tile_size=90, color1=(255, 255, 255), color2=(128, 128, 128), text_color=(0, 0, 0), highlight_color=(255, 255, 0, 128), illegal_moves=False):

        # Initialize Pygame
        pygame.init()

        # Set the size of the window and the size of each tile
        WINDOW_SIZE = ((len(self.board.board[0])+1)*tile_size, (len(self.board.board)+1)*tile_size)

        # Create the window
        screen = pygame.display.set_mode(WINDOW_SIZE)

        # Create a font for drawing text
        font = pygame.font.Font(None, 24)

        turn = f"{self.board.current_team}'s turn"
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
                        tile_y = len(self.board.board) - 1 - (mouse_y // tile_size)

                        if tile_x in range(len(self.board.board)) and tile_y in range(len(self.board.board[0])):
                            hovered_tile = Board.index_to_tile(tile_y, tile_x)
                            legal_moves = self.rule_engine.get_legal_moves(hovered_tile, self.board)
                    else:
                        legal_moves = self.rule_engine.get_legal_moves(selected_tile[0], self.board)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # get the mouse position
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        tile_x = (mouse_x // tile_size) - 1
                        tile_y = len(self.board.board) - 1 - (mouse_y // tile_size)
                        
                        if tile_x in range(len(self.board.board)) and tile_y in range(len(self.board.board[0])):
                            clicked_tile = Board.index_to_tile(tile_y, tile_x)

                            if not selected_tile:
                                if self.board.get_tile(clicked_tile).piece != 'empty':
                                    selected_tile = [clicked_tile]
                                    legal_moves = self.rule_engine.get_legal_moves(clicked_tile, self.board)
                            else:
                                self.board = self.rule_engine.play_move(self.board, selected_tile[0], clicked_tile, illegal_moves)
                                turn = f"{self.board.current_team}'s turn"
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

    def __str__(self) -> str:
        return f"Board: {self.board}\nRules: {self.rule_engine}"
