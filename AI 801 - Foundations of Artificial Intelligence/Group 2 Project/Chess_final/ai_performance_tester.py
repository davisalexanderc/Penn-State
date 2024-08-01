from game_modes import run_ai_vs_ai_tests

# Define AI types and depths for testing
white_ai_types = ['Minimax AI']  # Add other AI types as needed
black_ai_types = ['Stockfish AI']  # Add other AI types as needed
white_depths = [4]
black_depths = [1]
num_games = 10  # Change to 100 for full testing
time_limit = 120

if __name__ == "__main__":
    run_ai_vs_ai_tests(white_ai_types, black_ai_types, white_depths, black_depths, num_games, time_limit)
    exit()
