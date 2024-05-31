import pygame
from game import Game

def main():
    """
    Initializes the Pygame environment, sets up the game screen, and runs the main game loop.

    This function:
    - Initializes all Pygame modules.
    - Creates a game window with the specified dimensions.
    - Sets the window title to "Chess".
    - Creates a Clock object to manage the frame rate.
    - Initializes the Game class.
    - Enters the main game loop to handle events, update the game state, and refresh the display.
    - Exits the loop and uninitializes Pygame when the game is closed.
    """
    pygame.init()
    screen = pygame.display.set_mode((850, 1000)) # The tiles will be 100x100 pixels and there will be a 800x150 
                                                  # pixel space for the game info at the bottom with a 25 pixel border
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()

    game = Game(screen)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Checks for quit event
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Checks for left mouse button click event
                pos = pygame.mouse.get_pos() # Gets the mouse position
                row, col = (pos[1] - 25) // 100, (pos[0] - 25) // 100  # Converts pixel position to board position and accounts for the 25 pixel border
                game.handle_click((row, col))
                print("Mouse clicked at:", row, col)  ############### Error checking

        game.update()
        pygame.display.flip()
        clock.tick(30)

    # Close the game
    pygame.quit()

if __name__ == "__main__":
    main()