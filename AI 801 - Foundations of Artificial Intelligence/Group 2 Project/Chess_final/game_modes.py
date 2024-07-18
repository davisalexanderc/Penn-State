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
        self.white_depth = None
        self.black_depth = None

    def move_ai(self, ai_name, ai_depth, color, limit_time=3):
        """
        Moves the AI player using the Stockfish engine. Eventrually, this will be replaced with the AI model.

        Parameters:
        None

        Returns:
        None

        """
        ai_engine = get_ai_engine(ai_name, self.board.board, ai_depth, color, limit_time)
        move = ai_engine.select_move()
        if move is not None:
            self.board.board.push(move)
            player_color = 'White' if self.board.board.turn == chess.WHITE else 'Black'
            print(f'{player_color} AI player move: {move}')

    def get_ai_depth(self, ai_engine):
        """
        Gets the depth of the AI engine.

        Parameters:
        - ai_engine (str): The AI engine name.

        Returns:
        - depth (int): The depth of the AI engine.
        
        """

        return ai_engine.depth if ai_engine is not None else None

    def play_game(self, white_player, white_depth, black_player, black_depth, limit_time=3):
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
        self.white_depth = white_depth
        self.black_depth = black_depth
        board = self.board.board
        num_moves = 0

        white_ai_engine = get_ai_engine(white_player, board, white_depth, chess.WHITE, limit_time) if white_player != 'human' else None
        black_ai_engine = get_ai_engine(black_player, board, black_depth, chess.BLACK, limit_time) if black_player != 'human' else None


        print(f'white: {white_player}')
        print(f'black: {black_player}')

        while not board.is_game_over(): # Main game loop
            if board.turn == chess.WHITE:
                if self.white_player == 'human':
                    while not self.gui.move_human():
                        pass
                else:
                    self.move_ai(self.white_player, white_depth, chess.WHITE, limit_time)
            else:
                if self.black_player == 'human':
                    while not self.gui.move_human():
                        pass
                else:
                    self.move_ai(self.black_player, black_depth, chess.BLACK, limit_time)

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
        #white_depth = self.get_ai_depth(get_ai_engine(self.white_player, board)) if self.white_player != 'human' else None
        #print(white_depth)
        #black_depth = self.get_ai_depth(get_ai_engine(self.black_player, board)) if self.black_player != 'human' else None
        #print(black_depth)

        log_game_results('game_results.csv', 
            self.white_player, 
            self.black_player, 
            white_depth=self.get_ai_depth(white_ai_engine),  # Code changed here
            black_depth=self.get_ai_depth(black_ai_engine),  # Code changed here
            #white_depth = self.get_ai_depth(get_ai_engine(self.white_player, board)) if self.white_player != 'human' else None, 
            #black_depth = self.get_ai_depth(get_ai_engine(self.black_player, board)) if self.black_player != 'human' else None, 
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
        self.play_game(self.white_player, self.white_depth, self.black_player, self.black_depth)
        
