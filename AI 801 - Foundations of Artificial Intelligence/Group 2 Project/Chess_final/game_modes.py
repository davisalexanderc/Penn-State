import chess
from board import ChessBoard
from chess_gui import ChessGUI
from AI_Player import get_ai_engine
from logger import log_game_results

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
        self.gui = ChessGUI(self.board.board)
        self.white_player = None
        self.black_player = None

    def move_ai(self, ai_name):
        """
        Moves the AI player using the Stockfish engine. Eventrually, this will be replaced with the AI model.

        Parameters:
        None

        Returns:
        None

        """
        ai_engine = get_ai_engine(ai_name, self.board.board)
        move = ai_engine.select_move()
        if move is not None:
            self.board.board.push(move)
            print(f'AI move: {move}')

    def get_ai_depth(self, ai_engine):
        """
        Gets the depth of the AI engine.

        Parameters:
        - ai_engine (str): The AI engine name.

        Returns:
        - depth (int): The depth of the AI engine.
        
        """

        return ai_engine.depth

    def play_game(self, white_player, black_player):
        """
        Plays a game of chess based on the selected game mode.

        Parameters:
        - white_player (str): The white player type ('human' or 'ai').
        - black_player (str): The black player type ('human' or 'ai').

        Returns:
        None
        
        """

        self.white_player = white_player
        self.black_player = black_player
        board = self.board.board
        num_moves = 0

        print(f'white: {white_player}')
        print(f'black: {black_player}')

        while not board.is_game_over(): # Main game loop
            if board.turn == chess.WHITE:
                if self.white_player == 'human':
                    while not self.gui.move_human():
                        pass
                else:
                    self.move_ai(self.white_player)
            else:
                if self.black_player == 'human':
                    while not self.gui.move_human():
                        pass
                else:
                    self.move_ai(self.black_player)

            self.gui.update_display()
            num_moves += 1

        white_player_score, black_player_score, message = self.board.get_game_results()
        print(message)
        print(white_player_score, black_player_score)
        self.gui.status_message = message
        self.gui.update_display()

        # Determine the winning player
        if white_player_score == 1:
            winning_player = 'white'
        elif black_player_score == 1:
            winning_player = 'black'
        else:
            winning_player = 'draw'

        # Log the game results
        log_game_results('game_results.csv', 
            self.white_player, 
            self.black_player, 
            white_depth = self.get_ai_depth(get_ai_engine(self.white_player, board)) if self.white_player != 'human' else None, 
            black_depth = self.get_ai_depth(get_ai_engine(self.black_player, board)) if self.black_player != 'human' else None, 
            num_moves = num_moves, 
            winning_player = winning_player
        )

        self.restart_game()

    def restart_game(self):
        """
        Restarts the game.

        Parameters:
        None

        Returns:
        None
        
        """

        self.board.reset_board()
        self.gui.board = self.board.board
        self.gui.status_message = ""
        self.gui.selected_piece = None
        self.gui.selected_pos = None
        self.gui.possible_moves = []
        self.play_game(self.white_player, self.black_player)
        
