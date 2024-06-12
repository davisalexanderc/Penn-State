import pygame
from board import Board

class Game:
    def __init__(self, screen):
        """
        Initializes the Game class.

        Parameters:
        - screen (pygame.Surface): The surface the game is drawn on.
        """

        self.screen = screen
        self.board = Board() # Creates and initializes the Board class
        self.selected_piece = None # Stores the position of the selected piece, no piece is selected initially
        self.selected_pos = None # Stores the position of the selected piece, no piece is selected initially
        self.possible_moves = [] # Stores the possible moves for the selected piece
        self.status = "" # Stores the status of the game (e.g., "Check" or "Checkmate")
        self.promotion_pending = False # Stores whether a promotion is pending
        self.promotion_square = None # Stores the position of the promotion square
        self.promotion_color = None # Stores the color of the promotion piece

    def update(self):
        """
        Updates the game state and redraws the board.

        This method:
        - Fills the screen with white.
        - Draws the board and pieces.
        - Checks for mouse click events and handles them.
        """

        self.screen.fill((255,255,255)) # Fill the screen with white
        self.board.draw(self.screen) # Draw the board and pieces
        self.board.draw(self.screen, self.status) # Draw the board and pieces

        # Highlight possible moves
        for move in self.possible_moves:
            row, col = move
            pygame.draw.rect(self.screen, (0, 255, 0), (25 + col * 100, 25 + row * 100, 100, 100), 5)

        if self.promotion_pending:
            self.draw_promotion_choices()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                row, col = (pos[1] - 25) // 100, (pos[0] - 25) // 100
                if self.promotion_pending:
                    print("Promotion pending") ############### Error checking
                    self.handle_promotion_click(pos)
                else:
                    self.handle_click((row, col))
                print("Mouse clicked at:", row, col)
        return True

    def draw_promotion_choices(self,pos):
        """
        Draws the promotion choices on the screen.

        This method:
        - Draws the promotion choices (Queen, Rook, Bishop, Knight) on the screen.
        """

        x, y = pos
        choices = ['q', 'r', 'b', 'n']
        if 400 <= y <= 500:
            index = (x - 250) // 150
            if 0 <= index < len(choices):
                promotion_piece = choices[index]
                row, col = self.promotion_square
                piece = self.board.board[row, col]
                piece.piece_type = promotion_piece
                self.promotion_pending = False
                self.promotion_square = None
                self.promotion_color = None
                self.status = ""



#        # Handle mouse events
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT: # Check for quit event
#                return False
#            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Check for left mouse button click event
#                pos = pygame.mouse.get_pos() # Get the mouse position
#                row, col = (pos[1] - 25) // 100, (pos[0] - 25) // 100   # Convert pixel position to board position and accounts for the 25 pixel border
#               self.handle_click((row, col)) # Handle the mouse click
#               print("Mouse clicked at:", row, col)

    def handle_click(self, pos):
        """
        Handles mouse click events on the board.

        Parameters:
        - pos (tuple): The position of the mouse click on the board (row, col).

        This method:
        - Selects a piece if no piece is selected.
        - Moves the selected piece to the clicked position if a piece is already selected.
        """

        row, col = pos
        if self.selected_piece: # If a piece is already selected
            if pos in self.possible_moves: # If the clicked position is a possible move
                self.board.move_piece(self.selected_pos, pos) # Move the selected piece to the clicked position
                message = self.board.move_piece(self.selected_pos, pos) # Move the selected piece to the clicked position
                self.selected_piece = None # Deselect the piece
                self.selected_pos = None # Deselect the position
                self.possible_moves = [] # Clear the possible moves
                if message == "Checkmate" or message == "Check":
                    self.status = message # Set the status of the game
                elif isinstance(message, tuple) and message[0] == "Promotion":
                    self.promotion_pending = True
                    self.promotion_square = message[2]
                    self.promotion_color = message[1]
                    return
                else:
                    self.status = ""

            else: # If the clicked position is not a possible move, deselect the piece
                self.selected_piece = None
                self.selected_pos = None
                self.possible_moves = []
                self.status = ""
                #self.promotion_pending = False
                #self.promotion_square = None
                #self.promotion_color = None

        else: # If no piece is selected
            chess_piece = self.board.board[row, col] # Get the piece at the clicked position
            if chess_piece:
                self.selected_piece = chess_piece # Select the piece
                self.selected_pos = pos # Select the position
                self.possible_moves = self.board.get_possible_moves(chess_piece) # Get the possible moves for the selected piece
                print(f"Selected piece at: {self.selected_pos}, possible moves: {self.possible_moves}") ############### Error checking                print(f"Selected piece at: {self.selected_pos}, possible moves: {self.possible_moves}") ############### Error checking
                self.status = ""

    def display_message(self, message):
        """
        Displays a message on the screen.

        Parameters:
        - message (str): The message to display.

        This method:
        - Renders the message text.
        - Draws the message text on the screen.
        """

        font = pygame.font.Font(None, 74)
        text = font.render(message, True, (255, 0, 0))
        self.screen.blit(text, (25, 850)) # Draw the message text on the screen
        pygame.display.flip()