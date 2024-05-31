import pygame
import numpy
import chess
from piece import Piece

class Board:
    def __init__(self):
        """
        Initializes the Board class.

        This method:
        - Creates a new chess board.
        - Initializes the board state as a 2D (8x8) numpy array.
        """

        self.chess_board = chess.Board() # Creates a new chess board using the python-chess library
        self.board = numpy.zeros((8, 8), dtype=object) # Initializes the board state as a 2D numpy array
        self.initialize_board() # Initializes the board with the starting position of the pieces

    def initialize_board(self):
        """
        Initializes the chess board with the starting position of the pieces.

        This method:
        - Initializes the chess board with the starting position of the pieces.
        """
        
        for row in range(8):
            for col in range(8):
                chess_piece = self.chess_board.piece_at(chess.square(col, 7-row))
                if chess_piece:
                    color = 'w' if chess_piece.color == chess.WHITE else 'b'
                    piece_type = chess_piece.symbol().upper() if color == 'w' else chess_piece.symbol().lower() # Converts the piece symbol to 
                                                                                            #uppercase for white pieces and lowercase for black pieces
                    self.board[row,col] = Piece(color, piece_type, (row, col))

    def draw(self, screen):
        """
        Draws the chess board and pieces on the screen.

        Parameters:
        - screen (pygame.Surface): The surface to draw the board on.

        This method:
        - Draws the chess board with a 25 pixel border and dark gray and white tiles that are 100 x 100 pixels.
        - Draws the pieces on the board.
        """

        # Define colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        TAN = (210, 180, 140) # For the board color
        DARKGRAY = (100, 100, 100)

        # Draw the board
        pygame.draw.rect(screen, TAN, (0, 0, 850, 1000), 25)
        pygame.draw.rect(screen, TAN, (0, 825, 850, 825), 25)       
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, WHITE, (25 + col * 100, 25 + row * 100, 100, 100))
                else:
                    pygame.draw.rect(screen, DARKGRAY, (25 + col * 100, 25 + row * 100, 100, 100))
                
                # Draw the pieces
                ###piece = self.chess_board.piece_at(chess.square(col, 7-row))
                piece = self.board[row, col]
                if piece:
                    ###self.draw_piece(screen, piece.symbol(), row, col)
                    piece.draw(screen)

    def draw_piece(self, screen, symbol, row, col):  ### This method is not used in the current implementation
        """
        Draws a chess piece on the screen.

        Parameters:
        - screen (pygame.Surface): The surface to draw the piece on.
        - symbol (str): The symbol of the piece to draw.
        - row (int): The row index of the piece.
        - col (int): The column index of the piece.

        This method:
        - Draws the chess piece on the screen at the specified position.
        """

        font = pygame.font.Font(None, 74)
        piece_text = font.render(symbol, True, (0, 0, 0))
        screen.blit(piece_text, (col * 100 + 50, row * 100 + 50))

    def move_piece(self, start_pos, end_pos):
        """
        Moves a chess piece from the start position to the end position of a players move.
        
        Parameters:
        - start_pos (tuple): The starting position of the piece to move.
        - end_pos (tuple): The ending position of the piece to move.

        This method:
        - Converts the start and end positions to UCI chess notation.
        - Checks if the move is legal.
        - Moves the piece on the chess board.
        """
        print(f' start {start_pos}, end {end_pos} ')
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.board[start_pos] 
        self.board[end_row, end_col] = piece
        self.board[start_row, start_col] = None
        if piece:
            piece.position = end_pos

        move = chess.Move.from_uci(f"{self.to_chess_pos(start_pos)}{self.to_chess_pos(end_pos)}")
        if move in self.chess_board.legal_moves:
            self.chess_board.push(move)
            print(f"Moved piece from {start_pos} to {end_pos}")
        else:
            print(f"Invalid move: {self.to_chess_pos(start_pos)} to {self.to_chess_pos(end_pos)}")

    
    def get_possible_moves(self, piece):
        """
        Gets the possible moves for a piece at the specified position.

        Parameters:
        - pos (tuple): The position of the piece on the board (row, col).

        Returns:
        - list: A list of possible moves for the piece at the specified position.
        """
        possible_moves = []
        for move in self.chess_board.legal_moves:
            if move.from_square == chess.square(piece.position[1], 7 - piece.position[0]):
                to_row = 7 - chess.square_rank(move.to_square)
                to_col = chess.square_file(move.to_square)
                possible_moves.append((to_row, to_col))
        return possible_moves
    
    def to_chess_pos(self, pos):
        """
        Converts a board position to chess notation.

        Parameters:
        - pos (tuple): The position to convert (row, col).

        Returns:
        - str: The chess notation of the position (e.g., "a1", "e5").
        
        """
        row, col = pos
        return f"{chr(col + 97)}{8-row}" # Converts the row and column indices to chess notation
