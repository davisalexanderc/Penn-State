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

        # Highlight possible moves
        for move in self.possible_moves:
            row, col = move
            pygame.draw.rect(self.screen, (0, 255, 0), (25 + col * 100, 25 + row * 100, 100, 100), 5)

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
                self.selected_piece = None # Deselect the piece
                self.selected_pos = None # Deselect the position
                self.possible_moves = [] # Clear the possible moves
            else: # If the clicked position is not a possible move, deselect the piece
                self.selected_piece = None
                self.selected_pos = None
                self.possible_moves = []

        else: # If no piece is selected
            chess_piece = self.board.board[row, col] # Get the piece at the clicked position
            if chess_piece:
                self.selected_piece = chess_piece # Select the piece
                self.selected_pos = pos # Select the position
                self.possible_moves = self.board.get_possible_moves(chess_piece) # Get the possible moves for the selected piece
                print(f"Selected piece at: {self.selected_pos}, possible moves: {self.possible_moves}") ############### Error checking