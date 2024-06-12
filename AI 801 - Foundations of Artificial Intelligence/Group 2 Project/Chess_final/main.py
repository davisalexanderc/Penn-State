import chess
import chess.engine

def print_board(board):
    """
    Prints the current state of the chess board.

    Parameters:
    board (list): A 2-dimensional list representing the chess board.

    Returns:
    None

    """

    print(board)

def main():
    """
    This function represents the main game loop for playing chess.
    It prompts the user for moves in UCI format, validates the moves,
    updates the chess board, and checks for game over conditions.

    Parameters:
    None

    Returns:
    None

    """

    board = chess.Board() # Initialize the chess board
    while not board.is_game_over(): # Main game loop
        print_board(board)   ####### Add call to board drawing program/function here ##########
        if board.turn == chess.WHITE:
            print("White's turn")
        else:
            print("Black's turn")

        move = input("Enter your move in UCI format (e.g., e2e4): ") ####### Add call to movement function here
        try: # Validate the move
            move = chess.Move.from_uci(move) # Convert the move to UCI format (e.g., e2e4)
            if move.promotion is None and board.piece_at(move.from_square).piece_type == chess.PAWN: # Check for pawn promotion
                if chess.square_rank(move.to_square) in (0, 7): # Check if the pawn has reached the end of the board
                    promotion_piece = get_pawn_promotion()  # Get the piece to promote to
                    move = chess.Move(move.from_square, move.to_square, promotion = promotion_piece) # Update the move with the promotion piece
            if move in board.legal_moves: # Check if the move is legal
                board.push(move) # Update the board with the move
            else: # If the move is illegal
                print("Illegal move, please try again.")
        except ValueError: # If the move is not in UCI format
            print("Invalid move format, please try again.")

    # Game over conditions
    print_board(board)
    if board.is_checkmate(): # Check for checkmate
        if board.turn == chess.WHITE:
            print("Checkmate! Black wins!")
        else:
            print("Checkmate! White wins!")
    elif board.is_stalemate(): # Check for stalemate (draw) which is when the player whose turn it is has no legal moves and their king is not in check
        print("Stalemate!")
    elif board.is_insufficient_material(): # Check for insufficient material (draw) which is when neither player has enough material to checkmate the other
        print("Draw due to insufficient material!")
    elif board.is_seventyfive_moves(): # Check for the seventy-five-move rule (draw) which is when no pawn has been moved and no piece has been captured in the last 75 moves
        print("Draw due to the seventy-five-move rule!")
    elif board.is_fivefold_repetition(): # Check for fivefold repetition (draw) which is when the same position has occurred five times with the same player to move
        print("Draw due to fivefold repetition!")
    else: # If none of the above conditions are met
        print("Game over!")

def get_pawn_promotion():
    """
    Prompts the user for the piece to promote the pawn to.

    Parameters:
    None

    Returns:
    int: The piece to promote the pawn to (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT)
    
    """
    while True:
        piece = input("Enter the piece to promote to (Q, R, B, N): ").lower()
        if piece == 'q':
            return chess.QUEEN
        elif piece == 'r':
            return chess.ROOK
        elif piece == 'b':
            return chess.BISHOP
        elif piece == 'n':
            return chess.KNIGHT
        else:
            print("Invalid promotion piece, please try again.")

if __name__ == "__main__":
    main()