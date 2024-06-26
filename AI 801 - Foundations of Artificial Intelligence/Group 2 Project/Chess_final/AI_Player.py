import chess
import random

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
    
    def __init__(self, board, depth = 3):
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
        def minimax(board, depth, is_maximizing):
            if depth == 0 or board.is_game_over():
                return board_evaluation(board)
            if is_maximizing:
                max_eval = float("-inf")
                for move in board.legal_moves:
                    board.push(move)
                    eval = minimax(board, depth - 1, False)
                    board.pop()
                    max_eval = max(max_eval, eval)
                return max_eval
            else:
                min_eval = float("inf")
                for move in board.legal_moves:
                    board.push(move)
                    eval = minimax(board, depth - 1, True)
                    board.pop()
                    min_eval = min(min_eval, eval)
                return min_eval
        
        def board_evaluation(board):
            if board.is_checkmate():
                if board.turn == chess.WHITE:
                    return float("-inf")
                else:
                    return float("inf")
            return 0
        
        best_move = None
        best_eval = float("-inf")
        for move in self.board.legal_moves:
            self.board.push(move)
            eval = minimax(self.board, self.depth, False)
            self.board.pop()
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move
    
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