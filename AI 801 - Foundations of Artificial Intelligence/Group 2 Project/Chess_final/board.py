import chess
import chess.engine

class ChessBoard:
    def __init__(self):
        self.board = chess.Board()
        #self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")

    def reset_board(self):
        self.board.reset()

    def make_move(self, move):
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False
    
    def get_legal_moves(self):
        return list(self.board.legal_moves)
    
    def is_game_over(self):
        return self.board.is_game_over()
    
    def get_game_results(self):
        """
        Get the game results for the end of the game. Prints the result to the console, then 
        returns the scores for white and black players (0 for loss, 0.5 for draw, 1 for win).

        Parameters:
        None

        Returns:
        tuple: A tuple containing the scores for white and black players (0 for loss, 0.5 for draw, 1 for win) and a message string.
        
        """
        if self.board.is_checkmate(): # Check for checkmate
            if self.board.turn == chess.WHITE:
                message = "Checkmate! Black wins!"
                return (0,1, message)
            else:
                message = "Checkmate! White wins!"
                return (1,0, message)
        elif self.board.is_stalemate(): # Check for stalemate (draw) which is when the player whose turn it is has no legal moves and their king is not in check
            message = "Stalemate!"
            return (0.5,0.5, message)
        elif self.board.is_insufficient_material(): # Check for insufficient material (draw) which is when neither player has enough material to checkmate the other
            message = "Draw due to insufficient material!"
            return (0.5,0.5, message)
        elif self.board.is_seventyfive_moves(): # Check for the seventy-five-move rule (draw) which is when no pawn has been moved and no piece has been captured in the last 75 moves
            message = "Draw due to the seventy-five-move rule!"
            return (0.5,0.5, message)
        elif self.board.is_fivefold_repetition(): # Check for fivefold repetition (draw) which is when the same position has occurred five times with the same player to move
            message = "Draw due to fivefold repetition!"
            return (0.5,0.5, message)
        elif self.board.is_check(): # Check for fivefold repetition (draw) which is when the same position has occurred five times with the same player to move
            message = "Check"
            return (0.0,0.0, message)
        else: # Normal state where the game is still ongoing
            message = " "
            return (0.0,0.0, message)
        
    def close_engine(self):
        self.engine.quit()