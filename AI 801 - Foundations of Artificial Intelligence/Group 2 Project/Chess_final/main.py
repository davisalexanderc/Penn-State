from game_modes import GameModes
from chess_gui import game_start_menu

def main():
    """
    The main function that runs the game.

    Parameters:
    None

    Returns:
    None

    """
    limit_time = 1
    (white_player, white_depth, black_player, black_depth) = game_start_menu() # Displays a player select menue and gets user input    
    GameModes().play_game(white_player, white_depth, black_player, black_depth, limit_time)

if __name__ == "__main__":
    main()