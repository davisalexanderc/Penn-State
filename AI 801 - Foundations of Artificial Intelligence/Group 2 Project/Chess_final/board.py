import pygame
import chess
import chess.engine

class Board:
    def __init__(self):
        """
        Initializes the chess board and the Stockfish engine.        
        """
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")

def draw_board(self, screen, status):
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

        # Draw HUD
        font = pygame.font.Font(None, 74)
        # Draw Score
        score_text = font.render("Score: 0", True, BLACK)

        # Draw the player turn
        self.draw_player_turn(screen, status)