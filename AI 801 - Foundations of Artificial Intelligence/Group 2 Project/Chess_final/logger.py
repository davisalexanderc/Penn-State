import pandas as pd
import os

def log_game_results(file_path, white_player, black_player, 
                     white_depth, black_depth, num_moves, winning_player):
    """
    Logs the results of a game to a csv file.

    Parameters:
    - file_path (str): The file path of the csv file.
    - white_player (str): The white player type ('human' or type of AI engine).
    - black_player (str): The black player type ('human' or type of AI engine).
    - white_depth (int): The depth of the algorithm for an ai white player.
    - black_depth (int): The depth of the algorithm for an ai black player.
    - num_moves (int): The number of moves in the game.
    - winning_player (str): The winning player ('white', 'black', or 'draw').

    Returns:
    None
    
    """

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create a new csv file with headers
        df = pd.DataFrame(columns=['White Player', 'Black Player', 'White Depth', 'Black Depth', 
                                   'Number of Moves', 'Winning Player'])
        df.to_csv(file_path, index=False)

    # Append the results to the csv file
    df = pd.read_csv(file_path)

    new_row = {'White Player': white_player, 'Black Player': black_player, 
               'White Depth': white_depth, 'Black Depth': black_depth, 
               'Number of Moves': num_moves, 'Winning Player': winning_player}
    
    new_record = pd.DataFrame([new_row])
    df = pd.concat([df, new_record], ignore_index=True)

    df.to_csv(file_path, index=False)