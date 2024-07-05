import chess
import random
import datetime
from minimax import Minimax

class BaseAI:
    """
    The base class for an AI player.
    
    """

    def __init__(self, board):
        self.board = board # chess.Board()
        self.name = None

    def select_move(self):
        """
        Selects a move for the AI player.
        
        Parameters:
        None
        
        Returns:
        move (str): The move selected by the AI player.
        
        """
        raise NotImplementedError("The select_move method must be implemented by the subclass.")
    
    def get_name(self):
        """
        Returns the name of the AI player.
        
        Parameters:
        None
        
        Returns:
        name (str): The name of the AI player.
        
        """
        return self.name
    
class RandomAI(BaseAI):
    """
    A class for an AI player that selects a random move.
    
    """
    
    def __init__(self, board):
        super().__init__(board)
        self.name = "Random AI"
        
    def select_move(self):
        """
        Selects a random move for the AI player.
        
        Parameters:
        None
        
        Returns:
        move (str): The move selected by the AI player.
        
        """
        legal_moves = list(self.board.legal_moves)
        if legal_moves:
            return random.choice(legal_moves)
        return None
    
class MinimaxAI(BaseAI):
    """
    A class for an AI player that selects a move using the minimax algorithm.
    
    """
    
    def __init__(self, board, depth = 7): # default depth was 3
        super().__init__(board)
        self.name = "Minimax AI"
        self.depth = depth
    
    def select_move(self):
        """
        Selects a move for the AI player using the minimax algorithm.
        
        Parameters:
        None
        
        Returns:
        move (str): The move selected by the AI player.
        
        """
        return Minimax.minimaxRoot(self.board, self.depth, True, datetime.datetime.now(), 3)
    
class StockfishAI(BaseAI):
    """
    A class for an AI player that selects a move using the Stockfish engine.
    
    """
    
    def __init__(self, board):
        super().__init__(board)
        self.name = "Stockfish AI"
        
    def select_move(self):
        """
        Selects a move for the AI player using the Stockfish engine.
        
        Parameters:
        None
        
        Returns:
        move (str): The move selected by the AI player.
        
        """
        raise NotImplementedError("The select_move method must be implemented by the subclass.")
    
class AlphaZeroAI(BaseAI):
    """
    A class for an AI player that selects a move using the AlphaZero model.
    
    """
    
    def __init__(self, board):
        super().__init__(board)
        self.name = "AlphaZero AI"
        
    def select_move(self):
        """
        Selects a move for the AI player using the AlphaZero model.
        
        Parameters:
        None
        
        Returns:
        move (str): The move selected by the AI player.
        
        """
        raise NotImplementedError("The select_move method must be implemented by the subclass.")
    
def get_ai_engine(name, board):
    """
    Returns an AI engine based on the name provided.
    
    Parameters:
    name (str): The name of the AI engine.
    board (chess.Board): The chess board.
    
    Returns:
    ai_engine (BaseAI): An instance of the AI engine.
    
    """
    if name == "Random AI":
        return RandomAI(board)
    elif name == "Minimax AI":
        return MinimaxAI(board)
    else:
        raise ValueError("Invalid AI engine name.")