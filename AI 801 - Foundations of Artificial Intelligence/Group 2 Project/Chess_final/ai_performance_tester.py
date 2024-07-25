from game_modes import run_ai_vs_ai_tests

# Define AI types and depths for testing
white_ai_types = ['Random AI']  # Add other AI types as needed
black_ai_types = ['Minimax AI', 'Stockfish AI']  # Add other AI types as needed
white_depths = [3]
black_depths = [3, 4, 5]
num_games = 3  # Change to 100 for full testing
time_limit = 30

if __name__ == "__main__":
    run_ai_vs_ai_tests(white_ai_types, black_ai_types, white_depths, black_depths, num_games, time_limit)
