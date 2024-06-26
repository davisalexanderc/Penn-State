import chess
import math

MAX, MIN = math.inf, -math.inf

def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizingPlayer:
        maxEval = MIN
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = MAX
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def evaluate_board(board):
    evaluation = 0
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    for piece_type in piece_values:
        evaluation += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        evaluation -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    return evaluation

def get_best_move(board, depth):
    best_move = None
    maxEval = MIN
    for move in board.legal_moves:
        board.push(move)
        moveEval = minimax(board, depth - 1, MIN, MAX, False)
        board.pop()
        if moveEval > maxEval:
            maxEval = moveEval
            best_move = move
    return best_move