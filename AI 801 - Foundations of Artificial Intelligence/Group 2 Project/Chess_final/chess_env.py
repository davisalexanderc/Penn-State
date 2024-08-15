# File: ChessEnv
# Description: A class for an that helps set the initial parameters for MCST AI player.

import chess
import numpy as np

class ChessEnv:
    def __init__(self):
        self.board = chess.Board()
        self.action_size = len(list(self.board.legal_moves))

    def get_initial_state(self):
        return self.board.copy()

    def get_next_state(self, board, move, player):
        board.push(move)
        return board

    def get_valid_moves(self, board):
        valid_moves = np.zeros(self.action_size, dtype=np.uint8)
        for move in board.legal_moves:
            valid_moves[move] = 1
        return valid_moves

    def check_win(self, board):
        return board.is_checkmate()

    def get_value_and_terminated(self, board, move):
        if self.check_win(board):
            return 1, True
        if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
            return 0, True
        return 0, False

    def get_opponent(self, player):
        return chess.BLACK if player == chess.WHITE else chess.WHITE

    def change_perspective(self, board, player):
        if player == chess.BLACK:
            board = board.mirror()
        return board
