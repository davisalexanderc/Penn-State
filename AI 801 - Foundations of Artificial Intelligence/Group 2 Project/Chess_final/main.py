# main.py
# Description: This file contains the main function that runs the game.
#

import constants
from game_modes import GameModes
from menus import game_start_menu

def main():
    """
    The main function that runs the game.

    """
    limit_time = constants.TIME_LIMIT
    (white_player, white_depth, black_player, black_depth) = game_start_menu() # Displays a player select menue and gets user input    
    GameModes().play_game(white_player, white_depth, black_player, black_depth, limit_time, auto_run=False)

if __name__ == "__main__":
    main()