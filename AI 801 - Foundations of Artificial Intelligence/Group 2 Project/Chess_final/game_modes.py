# game_modes.py
# Description: This file contains the GameModes class which is used to manage the game modes and play a game of chess.
#

import chess
import time
import logging
from board import ChessBoard
#from chess_gui import ChessGUI, play_again_menu
from game_gui import ChessGUI
from menus import play_again_menu
from AI_Player import get_ai_engine, StockfishAI
from logger import log_game_results

class GameModes:
    """
    A class to represent the game modes. This class contains methods to play a game of chess based on the selected game mode.
    
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the GameModes object.
        
        """

        self.board = ChessBoard()
        self.gui = ChessGUI(self.board.board)
        self.white_player = None
        self.black_player = None
        self.white_depth = None
        self.black_depth = None
        self.auto_run = False
        self.reset_game_state

    def move_ai(self, ai_name, ai_depth, color, limit_time=3):
        """
        Moves the AI player using the Stockfish engine. Eventrually, this will be replaced with the AI model.

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

    def play_game(self, white_player, white_depth, black_player, black_depth, limit_time=3, auto_run=False):
        """
        Plays a game of chess based on the selected game mode.

        Parameters:
        - white_player (str): The white player type ('human' or 'ai').
        - black_player (str): The black player type ('human' or 'ai').
        
        """

        self.white_player = white_player
        self.black_player = black_player
        self.white_depth = white_depth
        self.black_depth = black_depth
        board = self.board.board
        self.auto_run = auto_run
        self.reset_game_state()

        white_ai_engine = get_ai_engine(white_player, board, white_depth, chess.WHITE, limit_time) if white_player != 'human' else None
        black_ai_engine = get_ai_engine(black_player, board, black_depth, chess.BLACK, limit_time) if black_player != 'human' else None


        print(f'white: {white_player}')
        print(f'black: {black_player}')

        while not board.is_game_over(): # Main game loop
            start_time = time.time() # Start the timer for the current turn

            if board.turn == chess.WHITE:
                if self.white_player == 'human':
                    while not self.gui.move_human():
                        pass
                else:
                    self.move_ai(self.white_player, white_depth, chess.WHITE, limit_time)
                self.white_turn_time += time.time() - start_time
            else:
                if self.black_player == 'human':
                    while not self.gui.move_human():
                        pass
                else:
                    self.move_ai(self.black_player, black_depth, chess.BLACK, limit_time)
                self.black_turn_time += time.time() - start_time

            if board.is_check() and not board.is_checkmate():
                self.gui.status_message = 'Check!'
            else:
                self.gui.clear_status_message()
                self.gui.status_message = ''

            self.gui.update_display()
            self.num_moves += 1

        # After the game ends
        white_player_score, black_player_score, message = self.board.get_game_results()
        print(message)
        print(white_player_score, black_player_score)
        self.gui.status_message = message
        self.gui.update_display()

        # Determine the winning player
        if white_player_score == 1:
            self.winning_player = 'white'
        elif black_player_score == 1:
            self.winning_player = 'black'
        else:
            self.winning_player = 'draw'

        # Log the game results
        log_game_results('game_results.csv', 
            self.white_player, 
            self.black_player, 
            white_depth=self.get_ai_depth(white_ai_engine),  # Code changed here
            black_depth=self.get_ai_depth(black_ai_engine),  # Code changed here
            num_moves = self.num_moves, 
            winning_player = self.winning_player,
            white_turn_time = self.white_turn_time,
            black_turn_time = self.black_turn_time
            )

        if not self.auto_run:
            self.gui.draw_end_game_buttons()
            if self.gui.play_again:
                self.restart_game()
            elif self.gui.quit_game:
                print('Thanks for playing!')
                exit()

    def restart_game(self):
        """
        Restarts the game.

        Parameters:
        None

        Returns:
        None
        
        """

        self.board.reset_board()
        self.gui.reset(self.board.board)
        if not self.auto_run:
            self.gui.clear_status_message()
            self.gui.update_display()
            self.play_game(self.white_player, self.white_depth, self.black_player, self.black_depth, auto_run=self.auto_run) 
        
    def reset_game_state(self):
        """
        Resets the game state attributes.
        """
        self.white_turn_time = 0
        self.black_turn_time = 0
        self.num_moves = 0
        self.winning_player = None

def run_ai_vs_ai_tests(white_ai_types, black_ai_types, white_depths, black_depths, num_games, time_limit=3):
    """
    Runs AI vs AI tests for all combinations of AI types and depths.

    Parameters:
    - ai_types (list): List of AI types.
    - depths (list): List of depths to test.
    - num_games (int): Number of games to run for each combination.
    """
    for white_ai in white_ai_types:
        for black_ai in black_ai_types:
            for white_depth in white_depths:
                for black_depth in black_depths:
                    for _ in range(num_games):
                        try:
                            game_modes = GameModes()
                            game_modes.play_game(white_ai, white_depth, black_ai, black_depth, time_limit, auto_run=True)
                        except RuntimeError as e:
                            logging.error(f"Game failed: {e}")