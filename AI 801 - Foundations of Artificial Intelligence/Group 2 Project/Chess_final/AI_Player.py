import chess
import chess.engine
import random
import datetime
from minimax import Minimax

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
        
        Parameters:
        None
        
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
    
    def __init__(self, board, depth = 3, color=None, limit_time=3): # default depth was 3 and limit_time was 3
        super().__init__(board, depth, color)
        self.name = "Minimax AI"
        self.limit_time = limit_time
        #self.depth = depth
    
    def select_move(self):
        """
        Selects a move for the AI player using the minimax algorithm.
        
        Parameters:
        None
        
        Returns:
        move (str): The move selected by the AI player.
        
        """
        return Minimax.minimaxRoot(self.board, self.depth, True, datetime.datetime.now(), 
                                   limit_time=self.limit_time, color=self.color)
    
class StockfishAI(AI_Player):
    """
    A class for an AI player that selects a move using the Stockfish engine.
    The version of Stockfish used is Stockfish 24.0
    
    """
    
    def __init__(self, board, stockfish_path, depth = 10, color=None):
        super().__init__(board, depth)
        self.name = "Stockfish AI"
        #self.depth = depth
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        
    def select_move(self):
        """
        Selects a move for the AI player using the Stockfish engine.
        
        Parameters:
        None
        
        Returns:
        move (str): The move selected by the AI player.
        
        """
        result = self.engine.play(self.board, chess.engine.Limit(depth=self.depth))
#        result = self.engine.play(self.board, chess.engine.Limit(time=0.5, depth=self.depth)) # default time 500 miliseconds
        return result.move
    
    def close(self):
        """
        Closes the Stockfish engine.
        
        Parameters:
        None
        
        Returns:
        None
        
        """
        self.engine.quit()
    
class AlphaZeroAI(AI_Player):
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
    
def get_ai_engine(name, board, depth=None, color=None, limit_time=3):
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
        return MinimaxAI(board, depth, color, limit_time)
    elif name == "Stockfish AI":
        stockfish_path = "stockfish/stockfish-windows-x86-64-avx2.exe"
        return StockfishAI(board, stockfish_path, depth, color)
    else:
        raise ValueError("Invalid AI engine name.")