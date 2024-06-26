# alphabeta_ai.py

class AlphaBetaAI:
    def __init__(self, depth=3):
        self.depth = depth

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return board.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.get_all_possible_moves('black'):
                board.make_move(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.undo_move(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.get_all_possible_moves('white'):
                board.make_move(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, board):
        best_move = None
        best_value = float('-inf')
        for move in board.get_all_possible_moves('black'):
            board.make_move(move)
            move_value = self.minimax(board, self.depth - 1, float('-inf'), float('inf'), False)
            board.undo_move(move)
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move