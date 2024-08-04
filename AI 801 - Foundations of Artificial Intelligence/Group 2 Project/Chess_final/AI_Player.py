# AI_player.py
# Description: This file contains the AI_Player class which is used to create AI players for the game.
#

import chess
import chess.engine
import random
import datetime
import time
from minimax import Minimax
from mcts_ai import MCTS
from chess_env import ChessEnv

class AI_Player:
    """
    The base class for an AI player.
    
    """

    def __init__(self, board, depth=None, color=None):
        self.board = board # chess.Board()
        self.depth = depth
        self.color = color
        self.name = None

    def select_move(self):
        """
        Selects a move for the AI player.
        
        Returns:
        move (str): The move selected by the AI player.
        
        """
        raise NotImplementedError("The select_move method must be implemented by the subclass.")
    
    def get_name(self):
        """
        Returns the name of the AI player.
        
        Returns:
        name (str): The name of the AI player.
        
        """
        return self.name
    
class RandomAI(AI_Player):
    """
    A class for an AI player that selects a random move.
    
    """
    
    def __init__(self, board):
        super().__init__(board)
        self.name = "Random AI"
        self.depth = None
        
    def select_move(self):
        """
        Selects a random move for the AI player.
        
        Returns:
        move (str): The move selected by the AI player.
        
        """
        legal_moves = list(self.board.legal_moves)
        if legal_moves:
            return random.choice(legal_moves)
        return None
    
class MinimaxAI(AI_Player):
    """
    A class for an AI player that selects a move using the minimax algorithm.
    
    """
    
    def __init__(self, board, depth = 3, color=None, limit_time=30): # default depth was 3 and limit_time was 3
        super().__init__(board, depth, color)
        self.name = "Minimax AI"
        self.limit_time = limit_time
        self.depth = depth
    
    def select_move(self):
        """
        Selects a move for the AI player using the minimax algorithm.
        
        Returns:
        move (str): The move selected by the AI player.
        
        """
        return Minimax.minimaxRoot(self.board, self.depth, True, datetime.datetime.now(), 
                                   limit_time=self.limit_time, color=self.color)

class MCTSAI(AI_Player):
    """
    A class for an AI player that selects a move using the Monte Carlo Tree Search model.
    
    """
    
    def __init__(self, board, depth=1000, color=None, limit_time=60, C=1.4): # depth is the number of searches
        super().__init__(board, depth, color)
        self.name = "MCTS AI"
        self.depth = depth
        self.limit_time = limit_time
        self.C = C

        
    def select_move(self):
        """
        Selects a move for the AI player using the MCTS model.

        Returns:
        move (str): The move selected by the AI player.
        
        """
        mcts = MCTS(self.board, num_searches=self.depth, C=self.C)
        return mcts.search()

class StockfishAI(AI_Player):
    """
    A class for an AI player that selects a move using the Stockfish engine.
    The version of Stockfish used is Stockfish 24.0
    
    """
    
    def __init__(self, board, stockfish_path, depth = 10, color=None):
        super().__init__(board, depth)
        self.name = "Stockfish AI"
        self.depth = depth
        retries = 5  # Number of retries
        while retries > 0:
            try:
                self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
                break
            except Exception as e:
                print(f"Failed to initialize Stockfish engine: {e}. Retrying...")
                retries -= 1
                time.sleep(1)  # Wait for 1 second before retrying
        if retries == 0:
            raise RuntimeError("Failed to initialize Stockfish engine after multiple attempts.")

    def select_move(self):
        """
        Selects a move for the AI player using the Stockfish engine.
        
        Returns:
        move (str): The move selected by the AI player.
        
        """
        result = self.engine.play(self.board, chess.engine.Limit(depth=self.depth))
#        result = self.engine.play(self.board, chess.engine.Limit(time=0.5, depth=self.depth)) # default time 500 miliseconds
        return result.move
    
    def close(self):
        """
        Closes the Stockfish engine.
        
        """
        self.engine.quit()
    
def get_ai_engine(name, board, depth=None, color=None, limit_time=60, C=1.4):
    """
    Returns an AI engine based on the name provided.
    
    Parameters:
    name (str): The name of the AI engine.
    board (chess.Board): The chess board.
    depth (int): The depth of the AI engine, or the number of searches for the MCTS AI engine.
    color (chess.Color): The color of the AI engine.
    limit_time (int): The time limit for the AI engine.
    C (float): The exploration parameter for the MCTS AI engine
    
    Returns:
    ai_engine (BaseAI): An instance of the AI engine.
    
    """
    if name == "Random AI":
        return RandomAI(board)
    elif name == "Minimax AI":
        return MinimaxAI(board, depth, color, limit_time)
    elif name == "MCTS AI":
        return MCTSAI(board, depth, color, limit_time)
    elif name == "Stockfish AI":
        stockfish_path = "stockfish/stockfish-windows-x86-64-avx2.exe"
        return StockfishAI(board, stockfish_path, depth, color)
    else:
        raise ValueError("Invalid AI engine name.")