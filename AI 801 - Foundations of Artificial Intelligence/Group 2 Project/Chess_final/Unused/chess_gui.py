from typing import Any
import os
import pygame
import chess
import game_modes
from board import ChessBoard

# Set the desired window position
x = 300  # X position of the window
y = 50  # Y position of the window
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

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
    Generates the game start menu.

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
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button1_location.collidepoint(mouse_pos):
                    white_player = "human"
                    black_player = "human"
                    return (white_player, None, black_player, None)
                elif button2_location.collidepoint(mouse_pos):
                    white_player = "human"
                    _, black_player, black_depth = select_ai_menu("black")
                    return (white_player, None, black_player, black_depth)
                elif button3_location.collidepoint(mouse_pos):
                    _, white_player, white_depth = select_ai_menu("white")
                    black_player = "human"                    
                    return (white_player, white_depth, black_player, None)
                elif button4_location.collidepoint(mouse_pos):
                    _, white_player, white_depth = select_ai_menu("white")
                    _, black_player, black_depth = select_ai_menu("black")
                    return (white_player, white_depth, black_player, black_depth)
        
        pygame.display.flip()  # Update the display
        clock.tick(15) # set frame rate to 30 fps
    pygame.quit()

def select_ai_menu(player_color):
    """
    Generates the AI selection menu.

    Parameters:
    - player_color (str): The color of the player ('white' or 'black').

    Returns:
    str: The selected AI engine.
    
    """

    running = True
    clock = pygame.time.Clock()
    ai_screen = pygame.display.set_mode((START_SCREEN_WIDTH, START_SCREEN_HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption(f'Select AI Engine for {player_color} Player')

    while running:

        ai_screen.fill(WHITE)

        # Define button locations
        button_width, button_height = 300, 50
        button1_location = pygame.Rect(100, 100, button_width, button_height)
        button2_location = pygame.Rect(100, 200, button_width, button_height)
        button3_location = pygame.Rect(100, 300, button_width, button_height)
        button4_location = pygame.Rect(100, 400, button_width, button_height)

        # Draw buttons
        draw_text("Welcome to Chess!", start_font, BLACK, ai_screen, START_SCREEN_WIDTH // 2, 50)
        draw_button(ai_screen, "Random Engine", button1_location)
        draw_button(ai_screen, "Minimax Engine", button2_location)
        draw_button(ai_screen, "MCTS Engine", button3_location)
        draw_button(ai_screen, "Stockfish Engine", button4_location)

        # Check for button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button1_location.collidepoint(mouse_pos):
                    return f"{player_color}_ai", "Random AI", None
                elif button2_location.collidepoint(mouse_pos):
                    depth = select_depth_menu(player_color, "Minimax AI")
                    return f"{player_color}_ai", "Minimax AI", depth
                elif button3_location.collidepoint(mouse_pos):
                    depth = 500 # Set a high depth for MCTS
                    return f"{player_color}_ai", "MCTS AI", depth
                elif button4_location.collidepoint(mouse_pos):
                    depth = select_depth_menu(player_color, "Stockfish AI")
                    return f"{player_color}_ai", "Stockfish AI", depth
        
        pygame.display.flip()  # Update the display
        clock.tick(15) # set frame rate to 30 fps
    pygame.quit()

def select_depth_menu(player_color, ai_engine):
    """
    Generates the AI depth selection menu.

    Parameters:
    - player_color (str): The color of the player ('white' or 'black').
    - ai_engine (str): The AI engine name.

    Returns:
    int: The selected depth for the AI engine.
    
    """
    running = True
    clock = pygame.time.Clock()
    ai_depth_screen = pygame.display.set_mode((START_SCREEN_WIDTH, START_SCREEN_HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption(f"Select Depth for {player_color}'s {ai_engine} AI Engine")

    while running:

        ai_depth_screen.fill(WHITE)

        # Define button locations
        button_width, button_height = 50, 50
        button_gap = 10
        buttons = []

        for i in range(10):
            x = 100 + (i % 5) * (button_width + button_gap)
            y = 100 + (i // 5) * (button_height + button_gap)
            buttons.append(pygame.Rect(x, y, button_width, button_height))

        # Draw buttons
        draw_text("Welcome to Chess!", start_font, BLACK, ai_depth_screen, START_SCREEN_WIDTH // 2, 50)

        for i, button in enumerate(buttons):
            draw_button(ai_depth_screen, str(i + 1), button, start_font)

        # Check for button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        print(f"Depth selected: {i + 1}")
                        return i + 1
                    
        pygame.display.flip()  # Update the display
        clock.tick(15) # set frame rate to 15 fps
    pygame.quit()

def play_again_menu():
    """
    Generates the play again menu.

    Parameters:
    None

    Returns:
    bool: True if the user wants to play again, False otherwise
    
    """

    running = True
    clock = pygame.time.Clock()
    play_again_screen = pygame.display.set_mode((START_SCREEN_WIDTH, START_SCREEN_HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption('Game Over!')

    while running:

        play_again_screen.fill(WHITE)

        # Define button locations
        button_width, button_height = 300, 50
        button1_location = pygame.Rect(100, 150, button_width, button_height)
        button2_location = pygame.Rect(100, 300, button_width, button_height)

        # Draw buttons
        draw_text("Do you want to play again?", start_font, BLACK, play_again_screen, START_SCREEN_WIDTH // 2, 50)
        draw_button(play_again_screen, "Yes", button1_location)
        draw_button(play_again_screen, "No", button2_location)

        # Check for button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button1_location.collidepoint(mouse_pos):
                    return True
                elif button2_location.collidepoint(mouse_pos):
                    return False
        
        pygame.display.flip()  # Update the display
        clock.tick(15) # set frame rate to 30 fps
    #pygame.quit()


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
        self.play_again = False
        self.quit_game = False        
        print(f"Initialized ChessGUI with width: {self.width}, height: {self.height}")

    def reset(self, board):
        self.__init__(board)
        self.update_display()
        print(f"Reset ChessGUI with width: {self.width}, height: {self.height}")

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
            draw_text(self.status_message, start_font, RED, self.screen, self.width // 2, 875)

    def draw_end_game_buttons(self):
        """
        Draws the end game buttons.

        Parameters:
        None

        Returns:
        None
        
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

        Parameters:
        None

        Returns:
        None
        
        """

        self.status_message = ""
        pygame.draw.rect(self.screen, BLACK, (25, 850, 975, 850))
        self.update_display()

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

        Parameters:
        None

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

        col = (pos[0] - self.boarder) // SQUARE_SIZE
        row = 7 - (pos[1] - self.boarder) // SQUARE_SIZE
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

    def reset(self, board):
        """
        Resets the game.

        Parameters:
        - board (chess.Board): The chess board object.

        Returns:
        None
        
        """

        self.board = board
        self.selected_piece = None
        self.selected_pos = None
        self.possible_moves = []
        self.status_message = ""
        self.update_display()