import datetime
import chess
from numpy import inf, flip

class Minimax:
    @staticmethod
    def reverseArray(array): 
        return flip(array)

    pawnEvalWhite = [
        [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [ 1.0,  1.0,  2.0,  3.0,  6.0,  2.0,  1.0,  1.0],
        [ 0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [ 0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [ 0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [ 0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5],
        [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ]

    pawnEvalBlack = reverseArray.__func__(pawnEvalWhite)

    knightEval = [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
        [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
        [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
        [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
        [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
        [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
    ]

    bishopEvalWhite = [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
        [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
        [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
        [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
        [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
    ]

    bishopEvalBlack = reverseArray.__func__(bishopEvalWhite)

    rookEvalWhite = [
        [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
    ]

    rookEvalBlack = reverseArray.__func__(rookEvalWhite)

    queenEval = [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
    ]

    kingEvalWhite = [
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
        [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]
    ]

    kingEvalBlack = reverseArray.__func__(kingEvalWhite)

    @staticmethod
    def minimaxRoot(board: chess.Board, depth, maximizingPlayer, time_before: datetime.datetime, limit_time):
        possibleMoves = board.legal_moves
        bestMove = float("-inf")
        bestMoveFound = None

        for possible_move in possibleMoves:
            time_after = datetime.datetime.now()
            move = chess.Move.from_uci(str(possible_move))
            board.push(move)
            value = Minimax.minimax(board, depth - 1, float("-inf"), float("inf"), not maximizingPlayer, time_before, limit_time, 'black')
            board.pop()
            if value >= bestMove:
                bestMove = value
                bestMoveFound = move
                print("Best move for now: ", str(bestMoveFound))
                answerTime = time_after - time_before
                if answerTime.seconds >= limit_time:
                    return bestMoveFound

        return bestMoveFound

    @staticmethod
    def minimax(board: chess.Board, depth, alpha, beta, maximizingPlayer, time_before: datetime.datetime, limit_time, turn):
        time_after = datetime.datetime.now()
        answerTime = time_after - time_before
        if depth == 0 or answerTime.seconds >= limit_time:
            node_evaluation = 0
            node_evaluation += Minimax.check_status(board, node_evaluation, turn)
            node_evaluation += Minimax.evaluationBoard(board)
            node_evaluation += Minimax.checkmate_status(board, turn)
            node_evaluation += Minimax.good_square_moves(board, turn)
            return -node_evaluation

        possibleMoves = board.legal_moves

        if maximizingPlayer:
            bestMove = float("-inf")
            for possibleMove in possibleMoves:
                time_after = datetime.datetime.now()
                move = chess.Move.from_uci(str(possibleMove))
                board.push(move)
                value = Minimax.minimax(board, depth - 1, alpha, beta, False, time_before, limit_time, 'black')
                bestMove = max(bestMove, value)
                board.pop()
                alpha = max(alpha, value)
                if beta <= alpha:
                    return bestMove

                answerTime = time_after - time_before
                if answerTime.seconds >= limit_time:
                    return bestMove

            return bestMove

        else:
            bestMove = float("inf")
            for possibleMove in possibleMoves:
                time_after = datetime.datetime.now()
                move = chess.Move.from_uci(str(possibleMove))
                board.push(move)
                value = Minimax.minimax(board, depth - 1, alpha, beta, True, time_before, limit_time, 'white')
                board.pop()
                bestMove = min(bestMove, value)
                if beta <= alpha:
                    return bestMove

                answerTime = time_after - time_before
                if answerTime.seconds >= limit_time:
                    return bestMove

            return bestMove

    @staticmethod
    def evaluationBoard(board):
        totalEvaluation = 0
        for i in range(8):
            for j in range(8):
                s = i * 8 + j
                totalEvaluation += Minimax.getPieceValue(str(board.piece_at(s)), i, j)
        return totalEvaluation

    @staticmethod
    def getPieceValue(piece, x, y):
        if piece is None or piece == 'None':
            return 0

        absoluteValue = 0

        if piece == 'P':
            absoluteValue = 10 + Minimax.pawnEvalWhite[x][y]
        elif piece == 'p':
            absoluteValue = 10 + Minimax.pawnEvalBlack[x][y] * -1
        elif piece == 'n':
            absoluteValue = 30 + Minimax.knightEval[x][y] * -1
        elif piece == 'N':
            absoluteValue = 30 + Minimax.knightEval[x][y]
        elif piece == 'b':
            absoluteValue = 30 + Minimax.bishopEvalBlack[x][y] * -1
        elif piece == 'B':
            absoluteValue = 30 + Minimax.bishopEvalWhite[x][y]
        elif piece == 'r':
            absoluteValue = 50 + Minimax.rookEvalBlack[x][y] * -1
        elif piece == 'R':
            absoluteValue = 50 + Minimax.rookEvalWhite[x][y]
        elif piece == 'q':
            absoluteValue = 90 + Minimax.queenEval[x][y] * -1
        elif piece == 'Q':
            absoluteValue = 90 + Minimax.queenEval[x][y]
        elif piece == 'k':
            absoluteValue = 9000 + Minimax.kingEvalBlack[x][y] * -1
        elif piece == 'K':
            absoluteValue = 9000 + Minimax.kingEvalWhite[x][y]
        else:
            print(f'Unknown piece: {piece} at position [{x}], [{y}]')

        return absoluteValue

    @staticmethod
    def checkmate_status(board: chess.Board, turn):
        node_evaluation = 0
        is_checkmate = board.is_checkmate()

        if turn == "white":
            if is_checkmate:
                node_evaluation += float("inf")
        else:
            if is_checkmate:
                node_evaluation += float("-inf")

        return node_evaluation

    @staticmethod
    def check_status(board: chess.Board, node_evaluation, turn):
        black_evaluation = 0
        is_check = board.is_check()

        if turn == "white":
            if is_check:
                black_evaluation += 10
        else:
            if is_check:
                black_evaluation -= 10

        return black_evaluation

    @staticmethod
    def good_square_moves(board: chess.Board, turn):
        node_evaluation = 0
        square_values = {
            "e4": 1, "e5": 1, "d4": 1, "d5": 1, "c6": 0.5, "d6": 0.5, "e6": 0.5, "f6": 0.5,
            "c3": 0.5, "d3": 0.5, "e3": 0.5, "f3": 0.5, "c4": 0.5, "c5": 0.5, "f4": 0.5, "f5": 0.5
        }

        possible_moves = board.legal_moves
        for possible_move in possible_moves:
            move = str(possible_move)
            if turn == "white" and move[2:4] in square_values:
                node_evaluation += square_values[move[2:4]]
            elif turn == "black" and move[2:4] in square_values:
                node_evaluation -= square_values[move[2:4]]

        return node_evaluation

    @staticmethod
    def main(move, next_player, board: chess.Board, limit_time=3):
        if next_player == 'white':
            is_game_over = board.is_game_over()
            if is_game_over:
                print('Game over')
                return 'Game over', board
            else:
                move = chess.Move.from_uci(str(move))
                board.push(move)
                print(board)
                print('----------------')
                print('Person move: ', str(move))
                return board
        elif next_player == 'black':
            if board is None or board == 'Game over':
                return 'Game over', board
            else:
                print('----------------')
                print("Minimax Turn:")
                print('\n-----------------\nMinimax is Calculating...\n-----------------')
                time_before = datetime.datetime.now()
                move = Minimax.minimaxRoot(board, 3, True, time_before, limit_time)

                if move is None:
                    return 'Game over', board

                time_after = datetime.datetime.now()
                answerTime = time_after - time_before
                print(f'Minimax time: {answerTime.seconds} seconds')
                move = chess.Move.from_uci(str(move))
                board.push(move)
                print(board)
                return move, board

