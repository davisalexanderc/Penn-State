Explanation

    main.py:
        Initializes the Pygame environment and game screen.
        Creates an instance of the Game class.
        Runs the main game loop, which handles events, updates the game state, and refreshes the display.

    game.py:
        Game class:
            Initializes with a reference to the screen.
            Creates an instance of the Board class.
            Stores the selected piece, its position, and possible moves.
            handle_click: Handles mouse click events on the board, selecting or moving pieces.
            update: Updates the game state, redraws the board, and highlights possible moves.

    board.py:
        Board class:
            Initializes the board as a 2D numpy array and sets up the initial positions of the pieces using the initialize_board method.
            draw: Draws the chess board and pieces on the screen.
            move_piece: Moves a piece from the start position to the end position if the move is legal.
            get_possible_moves: Gets the possible moves for a selected piece.
            to_chess_pos: Converts board positions to chess notation.
            draw_player_turn: Draws the current player's turn on the screen.

    piece.py:
        Piece class:
            Initializes with a color, type, and position.
            load_image: Loads the image for the piece based on its type and color.
            draw: Draws the piece on the screen at its specified position.

Summary

    main.py initializes the game and manages the main game loop.
    game.py manages the game state and interactions.
    board.py manages the board state and interactions with pieces.
    piece.py manages individual pieces, including loading their images and drawing them on the board.