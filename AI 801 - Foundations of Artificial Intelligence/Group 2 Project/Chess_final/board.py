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
        tuple: A tuple containing the scores for white and black players (0 for loss, 0.5 for draw, 1 for win)
        
        """
        if self.board.is_checkmate(): # Check for checkmate
            if self.board.turn == chess.WHITE:
                print("Checkmate! Black wins!")
                return (0,1)
            else:
                print("Checkmate! White wins!")
                return (1,0)
        elif self.board.is_stalemate(): # Check for stalemate (draw) which is when the player whose turn it is has no legal moves and their king is not in check
            print("Stalemate!")
            return (0.5,0.5)
        elif self.board.is_insufficient_material(): # Check for insufficient material (draw) which is when neither player has enough material to checkmate the other
            print("Draw due to insufficient material!")
            return (0.5,0.5)
        elif self.board.is_seventyfive_moves(): # Check for the seventy-five-move rule (draw) which is when no pawn has been moved and no piece has been captured in the last 75 moves
            print("Draw due to the seventy-five-move rule!")
            return (0.5,0.5)
        elif self.board.is_fivefold_repetition(): # Check for fivefold repetition (draw) which is when the same position has occurred five times with the same player to move
            print("Draw due to fivefold repetition!")
            return (0.5,0.5)
        else: # If none of the above conditions are met
            print("Game over!")
            return (0,0)
        
    def close_engine(self):
        self.engine.quit()