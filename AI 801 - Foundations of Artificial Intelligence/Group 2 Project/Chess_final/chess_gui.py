from typing import Any
import pygame
import chess
import game_modes
from board import ChessBoard

pygame.init()

# Constants
START_SCREEN_WIDTH, START_SCREEN_HEIGHT = 500, 500
BOARD_WIDTH, BOARD_HEIGHT = 850, 1000
SQUARE_SIZE = 100
BOARDER = 25
PIECE_SIZE = 100

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TAN = (210, 180, 140) # For the board color
DARKGRAY = (100, 100, 100)
RED = (255, 0, 0)

# Define fonts
start_font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)
player_turn_font = pygame.font.Font(None, 36)

# Define General GUI Functions

def draw_text(text: str, font: Any, color: Any, screen: Any, x: int, y: int):
    """
    Draws text to the screen.

    Parameters:
    - text (str): The text to display.
    - font (Any): The font to use.
    - color (Any): The color of the text.
    - screen (Any): The screen to draw the text on.
    - x (int): The x-coordinate of the text.
    - y (int): The y-coordinate of the text.

    Returns:
    None
    
    """

    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_obj, text_rect)

def draw_button(screen, text, location, font = start_font, button_color = DARKGRAY, text_color = BLACK):
    """
    Draws a button to the screen.

    Parameters:
    - screen (Any): The screen to draw the button on.
    - text (str): The text to display on the button.
    - location (tuple): The location of the button (x1, y1, x2, y2).
    - font (Any): The font to use for the text.
    - button_color (Any): The color of the button.
    - text_color (Any): The color of the text.

    Returns:
    None
        
    """

    button = pygame.Rect(location)
    pygame.draw.rect(screen, button_color, button)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center = button.center)
    screen.blit(text_surface, text_rect)

# Define Game Start Menu Function

def game_start_menu():
    """
    The main function that runs the game.

    Parameters:
    None

    Returns:
    tuple: (white_player, black_player)
    
    """

    running = True
    clock = pygame.time.Clock()

    while running:
        start_screen = pygame.display.set_mode((START_SCREEN_WIDTH, START_SCREEN_HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption('Chess Game Mode Selection')
        start_screen.fill(WHITE)

        # Define button locations
        button_width, button_height = 300, 50
        button1_location = pygame.Rect(100, 100, button_width, button_height)
        button2_location = pygame.Rect(100, 200, button_width, button_height)
        button3_location = pygame.Rect(100, 300, button_width, button_height)
        button4_location = pygame.Rect(100, 400, button_width, button_height)

        # Draw buttons
        draw_text("Welcome to Chess!", start_font, BLACK, start_screen, START_SCREEN_WIDTH // 2, 50)
        draw_button(start_screen, "W: Player vs. B: Player", button1_location)
        draw_button(start_screen, "W: Player vs. B: AI", button2_location)
        draw_button(start_screen, "W: AI vs. B: Player", button3_location)
        draw_button(start_screen, "W: AI vs. B: AI", button4_location)

        # Check for button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return ("None", "None")
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button1_location.collidepoint(mouse_pos):
                    return ("human", "human")
                elif button2_location.collidepoint(mouse_pos):
                    return ("human", "ai")
                elif button3_location.collidepoint(mouse_pos):
                    return ("ai", "human")
                elif button4_location.collidepoint(mouse_pos):
                    return ("ai", "ai")
        
        pygame.display.flip()  # Update the display
        clock.tick(15) # set frame rate to 30 fps
    pygame.quit()

# Define Functions for Loading and Drawing Piece Images

def load_piece_images():
    pieces = {}
    black_pieces = ['r', 'n', 'b', 'q', 'k', 'p']
    white_pieces = ['R', 'N', 'B', 'Q', 'K', 'P']
    for piece in black_pieces:
        pieces[piece] = pygame.transform.scale(pygame.image.load(f'assets/Images/black_pieces/{piece}.png'), (PIECE_SIZE, PIECE_SIZE))

    for piece in white_pieces:
        pieces[piece] = pygame.transform.scale(pygame.image.load(f'assets/Images/white_pieces/{piece}.png'), (PIECE_SIZE, PIECE_SIZE))    
    
    return pieces

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
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.boarder = BOARDER
        self.screen = pygame.display.set_mode((self.width, self.height),  pygame.DOUBLEBUF)
        pygame.display.set_caption('Chess')
        self.piece_images = load_piece_images()
        self.clock = pygame.time.Clock()
        self.selected_piece = None
        self.selected_pos = None
        self.possible_moves = []
        self.status_message = ""

    def draw_board(self):
        """
        Draws the chess board.

        Parameters:
        None

        Returns:
        None
        
        """
        # Draw Screen Background
        pygame.draw.rect(self.screen, TAN, (0, 0, self.width, self.height), self.boarder)
        pygame.draw.rect(self.screen, TAN, (0, self.width - self.boarder, self.width, self.width - self.boarder), self.boarder) 

        for row in range(8):
            for col in range(8):
                color = DARKGRAY if (row + col) % 2 == 0 else WHITE
                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE + self.boarder, row * SQUARE_SIZE + self.boarder, 
                                                 SQUARE_SIZE, SQUARE_SIZE))
                piece = self.board.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_image = self.piece_images[piece.symbol()] 
                    self.screen.blit(piece_image, (col * SQUARE_SIZE + self.boarder, row * SQUARE_SIZE + self.boarder))
        
        if self.status_message:
            draw_text(self.status_message, start_font, RED, self.screen, self.width // 2, self.height - 50)

    def update_display(self):
        """
        Updates the display.

        Parameters:
        None

        Returns:
        None
        
        """

        self.draw_board()
        pygame.display.flip()
        self.clock.tick(30)

    #def handel_human_move(self):

    def handel_click(self, pos):
        """
        Handles the click event on the chess board.

        Parameters:
        - pos (tuple): The position of the click.

        Returns:
        None
        
        """

        col = (pos[0] - self.boarder) // SQUARE_SIZE
        row = 7 - (pos[1] - self.boarder) // SQUARE_SIZE
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

        Parameters:
        None

        Returns:
        bool: True if the move is made, False otherwise
        
        """

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.handel_click(pos):
                        return True
                    
            self.update_display()
        return False

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

        Parameters:
        None

        Returns:
        str: The piece to promote the pawn to.
        
        """

        print("promotion detected")
        running = True
        while running:
            draw_text("Select a piece to promote the pawn to:", start_font, RED, self.screen, self.width // 2, 875)

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