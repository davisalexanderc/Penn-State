# game_gui.py
# This file contains the GUI for the chess game.
#

import os
import pygame
import chess
import game_modes
import constants
from board import ChessBoard
from typing import Any
from menus import draw_text, draw_button

pygame.init()

# Set the desired window position
x = 300  # X position of the window
y = 50  # Y position of the window
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{constants.WINDOW_X_POSITION},{constants.WINDOW_Y_POSITION}"

LIGHT=constants.WHITE
DARK=constants.DARKGRAY
BOARDER_COLOR=constants.TAN

start_font = pygame.font.Font(None, constants.START_FONT_SIZE)
game_over_font = pygame.font.Font(None, constants.GAME_OVER_FONT_SIZE)
player_turn_font = pygame.font.Font(None, constants.PLAYER_TURN_FONT_SIZE)



# Define Chess GUI Class and Methods for Drawing the Board

class ChessGUI:
    """
    The ChessGUI class for the chess game.

    Attributes:
    - board (chess.Board): The chess board object.
    - width (int): The width of the screen.
    - height (int): The height of the screen.
    - boarder (int): The width of the boarder.
    - screen (Any): The screen object.
    - piece_images (dict): A dictionary containing the piece images.
    - clock (Any): The clock object for controlling the frame rate.
    - selected_piece (chess.Piece): The selected piece.
    - selected_pos (tuple): The selected position.
    - possible_moves (list): A list of possible moves for the selected piece.

    """

    def __init__(self, board):
        self.board = board
        self.chessboard = ChessBoard()
        self.width = constants.BOARD_WIDTH
        self.height = constants.BOARD_HEIGHT
        self.boarder = constants.BOARDER
        self.screen = pygame.display.set_mode((self.width, self.height),  pygame.DOUBLEBUF)
        pygame.display.set_caption('Chess')
        self.piece_images = self.load_piece_images()
        self.clock = pygame.time.Clock()
        self.selected_piece = None
        self.selected_pos = None
        self.possible_moves = []
        self.status_message = ""
        self.play_again = False
        self.quit_game = False        
        print(f"Initialized ChessGUI with width: {self.width}, height: {self.height}")

    def reset(self, board):
        self.__init__(board)
        self.update_display()
        print(f"Reset ChessGUI with width: {self.width}, height: {self.height}")

    def load_piece_images(self):
        pieces = {}
        black_pieces = ['r', 'n', 'b', 'q', 'k', 'p']
        white_pieces = ['R', 'N', 'B', 'Q', 'K', 'P']
        for piece in black_pieces:
            pieces[piece] = pygame.transform.scale(pygame.image.load(f'assets/Images/black_pieces/{piece}.png'), 
                                                (constants.PIECE_SIZE, constants.PIECE_SIZE))
        for piece in white_pieces:
            pieces[piece] = pygame.transform.scale(pygame.image.load(f'assets/Images/white_pieces/{piece}.png'), 
                                                (constants.PIECE_SIZE, constants.PIECE_SIZE))    
        return pieces

    def draw_board(self):
        """
        Draws the chess board.
        
        """
        # Draw Screen Background
        pygame.draw.rect(self.screen, BOARDER_COLOR, (0, 0, self.width, self.height), self.boarder)
        pygame.draw.rect(self.screen, BOARDER_COLOR, (0, self.width - self.boarder, self.width, self.width - self.boarder), self.boarder) 

        for row in range(8):
            for col in range(8):
                color = DARK if (row + col) % 2 == 0 else LIGHT
                pygame.draw.rect(self.screen, color, (col * constants.SQUARE_SIZE + self.boarder, 
                                                      row * constants.SQUARE_SIZE + self.boarder, 
                                                      constants.SQUARE_SIZE, constants.SQUARE_SIZE))
                piece = self.board.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_image = self.piece_images[piece.symbol()] 
                    self.screen.blit(piece_image, (col * constants.SQUARE_SIZE + self.boarder, 
                                                   row * constants.SQUARE_SIZE + self.boarder))
        
        if self.status_message:
            draw_text(self.status_message, start_font, constants.RED, self.screen, self.width // 2, 875)

    def draw_end_game_buttons(self):
        """
        Draws the end game buttons.

        """

        # Define button locations
        button_width, button_height = 150, 50
        replay_button_location = pygame.Rect(200, 900, button_width, button_height)
        quit_button_location = pygame.Rect(500, 900, button_width, button_height)

        # Draw buttons
        draw_button(self.screen, "Play Again", replay_button_location)
        draw_button(self.screen, "Quit", quit_button_location)
        pygame.display.flip()

        quit_game = True
        while quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if replay_button_location.collidepoint(mouse_pos):
                        self.play_again = True
                        quit_game = False
                        self.clear_status_message()
                    elif quit_button_location.collidepoint(mouse_pos):
                        self.quit_game = True
                        pygame.quit()
                        exit()

    def clear_status_message(self):
        """
        Clears the status message.

        """

        self.status_message = ""
        pygame.draw.rect(self.screen, constants.BLACK, (25, 850, 975, 850))
        self.update_display()

    def update_display(self):
        """
        Updates the display.

        """

        self.draw_board()
        pygame.display.flip()
        self.clock.tick(30)

    def handel_click(self, pos):
        """
        Handles the click event on the chess board.

        Parameters:
        - pos (tuple): The position of the click.

        """

        col = (pos[0] - self.boarder) // constants.SQUARE_SIZE
        row = 7 - (pos[1] - self.boarder) // constants.SQUARE_SIZE
        square = chess.square(col, row)
        piece = self.board.piece_at(square)

        if self.selected_piece:
            if square in self.possible_moves:
                move = chess.Move(self.selected_pos, square)

                # Check for pawn promotion
                if (move.promotion is None and self.selected_piece.piece_type == chess.PAWN) and (
                    chess.square_rank(move.to_square) in (0, 7)):
                        promotion_piece = self.get_pawn_promotion()
                        move = chess.Move(move.from_square, move.to_square, promotion = promotion_piece)
                        self.clear_status_message()
                        
                self.board.push(move)
                (white_score, black_score, self.status_message) = self.chessboard.get_game_results()
                self.selected_piece = None
                self.selected_pos = None
                self.possible_moves = []
                self.update_display()
                if white_score + black_score == 1:
                    pygame.time.wait(3000)
                    game_modes.restart_game()
                    return False

                return True
            else:
                self.selected_piece = None
                self.selected_pos = None
                self.possible_moves = []
        else:
            if piece:
                if piece.color == self.board.turn:
                    self.selected_piece = piece
                    self.selected_pos = square
                    self.possible_moves = list(self.board.legal_moves)
                    self.possible_moves = [move.to_square for move in self.possible_moves if move.from_square == self.selected_pos]
                else:
                    self.selected_piece = None
                    self.selected_pos = None
                    self.possible_moves = []
        return False
    
    def move_human(self):
        """
        Moves the human player.

        Returns:
        bool: True if the move is made, False otherwise
        
        """

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()  # Ensure the entire program exits
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.handel_click(pos):
                        return True
            self.update_display()
        return False

    def get_clicked_square(self, pos):
        """
        Gets the clicked square.

        Parameters:
        - pos (tuple): The position of the click.

        Returns:
        int: The clicked square.
        
        """

        col = (pos[0] - self.boarder) // constants.SQUARE_SIZE
        row = 7 - (pos[1] - self.boarder) // constants.SQUARE_SIZE
        return chess.square(col, row)

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update_display()
        pygame.quit()

    def get_pawn_promotion(self):
        """
        Gets the pawn promotion piece from the user.

        Returns:
        str: The piece to promote the pawn to.
        
        """

        print("promotion detected")
        running = True
        while running:
            draw_text("Select a piece to promote the pawn to:", start_font, constants.RED, self.screen, self.width // 2, 875)

            # Define button locations
            button_width, button_height = 100, 50
            buttonQ_location = pygame.Rect(175, 900, button_width, button_height)
            buttonR_location = pygame.Rect(300, 900, button_width, button_height)
            buttonB_location = pygame.Rect(425, 900, button_width, button_height)
            buttonN_location = pygame.Rect(550, 900, button_width, button_height)

            # Draw buttons
            draw_button(self.screen, "Queen", buttonQ_location)
            draw_button(self.screen, "Rook", buttonR_location)
            draw_button(self.screen, "Bishop", buttonB_location)
            draw_button(self.screen, "Knight", buttonN_location)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if buttonQ_location.collidepoint(mouse_pos):
                        return chess.QUEEN
                    elif buttonR_location.collidepoint(mouse_pos):
                        return chess.ROOK
                    elif buttonB_location.collidepoint(mouse_pos):
                        return chess.BISHOP
                    elif buttonN_location.collidepoint(mouse_pos):
                        return chess.KNIGHT
                    
            pygame.display.flip()
            self.clock.tick(15)
        pygame.quit()

    def reset(self, board):
        """
        Resets the game.

        Parameters:
        - board (chess.Board): The chess board object.
        
        """

        self.board = board
        self.selected_piece = None
        self.selected_pos = None
        self.possible_moves = []
        self.status_message = ""
        self.update_display()