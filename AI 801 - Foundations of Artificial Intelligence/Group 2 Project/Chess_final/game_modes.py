import chess
import chess.engine
from board import ChessBoard
from chess_gui import ChessGUI

def get_pawn_promotion():
    """
    Prompts the user for the piece to promote the pawn to.

    Parameters:
    None

    Returns:
    int: The piece to promote the pawn to (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT)
    
    """
    
    while True:
        piece = input("Enter the piece to promote to (Q, R, B, N): ").lower()
        if piece == 'q':
            return chess.QUEEN
        elif piece == 'r':
            return chess.ROOK
        elif piece == 'b':
            return chess.BISHOP
        elif piece == 'n':
            return chess.KNIGHT
        else:
            print("Invalid promotion piece, please try again.")

class GameModes:
    """
    A class to represent the game modes. This class contains methods to play a game of chess based on the selected game mode.
    
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the GameModes object.

        Parameters:
        None

        Returns:
        None
        
        """
        self.board = ChessBoard()
        self.gui = None
        self.white_player = None
        self.black_player = None
        
    def initialize_gui(self):
        """
        Initializes the GUI.
        
        Parameters:
        None
        
        Returns:
        None
        
        """
        if not self.gui:
            self.gui = ChessGUI(self.board.board)

    def move_human(self):
        """
        Moves the human player. Prompts the user for a move and validates it.
        
        Parameters:
        None

        Returns:
        bool: True if the move is valid, False otherwise
        
        """

        board = self.board.board
        self.gui.update_display()

        if board.turn == chess.WHITE:
            print("White's turn")
        else:
            print("Black's turn")

        #print(board.fen()) # Print the board state in Forsyth-Edwards Notation (FEN)
        move = input("Enter your move in UCI format (e.g., e2e4): ") ####### Add call to movement function here
        try: # Validate the move
            move = chess.Move.from_uci(move) # Convert the move to UCI format (e.g., e2e4)
            if move.promotion is None and board.piece_at(move.from_square).piece_type == chess.PAWN: # Check for pawn promotion
                if chess.square_rank(move.to_square) in (0, 7): # Check if the pawn has reached the end of the board
                    promotion_piece = get_pawn_promotion()  # Get the piece to promote to
                    move = chess.Move(move.from_square, move.to_square, promotion = promotion_piece) # Update the move with the promotion piece
            if move in board.legal_moves: # Check if the move is legal
                board.push(move) # Update the board with the move
                return True
            else: # If the move is illegal
                print("Illegal move, please try again.")
                return True
        
        except ValueError: # If the move is not in UCI format
            print("Invalid move format, please try again.")
            return False

    def move_ai(self):
        """
        Moves the AI player using the Stockfish engine. Eventrually, this will be replaced with the AI model.

        Parameters:
        None

        Returns:
        None

        """

        board = self.board.board
        print("AI's turn")
        result = self.board.engine.play(board, chess.engine.Limit(time=0.5))
        board.push(result.move)

    def play_game(self, white_player, black_player):
        """
        Plays a game of chess based on the selected game mode.

        Parameters:
        - white_player (str): The white player type ('human' or 'ai').
        - black_player (str): The black player type ('human' or 'ai').

        Returns:
        None
        
        """

        self.initialize_gui()
        self.white_player = white_player
        self.black_player = black_player
        board = self.board.board

        while not board.is_game_over(): # Main game loop
            if board.turn == chess.WHITE:
                if self.white_player == 'human':
                    while not self.move_human():
                        pass
                else:
                    self.move_ai()
            else:
                if self.black_player == 'human':
                    while not self.move_human():
                        pass
                else:
                    self.move_ai()

        score = self.board.get_game_results()
        print(score)

    def human_vs_human(self):  ##### No longer needed
        self.initialize_gui()
        board = self.board.board  #chess.Board() # Initialize the chess board

        while not board.is_game_over(): # Main game loop
            #print(board)   ####### Add call to board drawing program/function here ##########
            self.move_human
            #self.gui.update_display()  
        score = self.board.get_game_results()
        print(score)   

    def human_vs_ai(self): ##### No longer needed
        print("Human vs. AI mode is not yet implemented.")
        pass
    
    def ai_vs_ai(self): ##### No longer needed
        print("AI vs. AI mode is not yet implemented.")
        pass