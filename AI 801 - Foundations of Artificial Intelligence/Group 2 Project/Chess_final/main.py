from game_modes import GameModes

def main():
    """
    The main function that runs the game.

    Parameters:
    None

    Returns:
    None
    
    """

    print("Welcome to Chess!")
    print("Please select a game mode:")
    print("1. Player vs. Player")
    print("2. Player vs. AI")
    print("3. AI vs. Player")
    print("4. AI vs. AI")
    choice = input("Enter your selection (1, 2, 3, or 4): ")
    print('Your choice:', choice)
    game_modes = GameModes()

    if choice == "1": # Player vs. Player
        white_player = "human"
        black_player = "human"
    elif choice == "2":
        white_player = "human"
        black_player = "ai"
    elif choice == "3":
        white_player = "ai"
        black_player = "human"
    elif choice == "4":
        white_player = "ai"
        black_player = "ai"
    else:
        print("Invalid selection. Please try again.")
        main()

    game_modes.play_game(white_player, black_player)

if __name__ == "__main__":
    main()