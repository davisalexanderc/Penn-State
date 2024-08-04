# menus.py
# Description: This file contains the GUI for the menu screen.
#

import pygame
import constants
from typing import Any

pygame.init()

# Define fonts
start_font = pygame.font.Font(None, constants.START_FONT_SIZE)
game_over_font = pygame.font.Font(None, constants.GAME_OVER_FONT_SIZE)
player_turn_font = pygame.font.Font(None, constants.PLAYER_TURN_FONT_SIZE)

def draw_text(text: str, font: Any, color: Any, screen: Any, x: int, y: int):
    """
    Draws text to the screen.

    Parameters:
    - text (str): The text to display.
    - font (Any): The font to use.
    - color (Any): The color of the text.
    - screen (Any): The screen to draw the text on.
    - x (int): The x-coordinate of the text.
    - y (int): The y-coordinate of the text.

    """

    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_obj, text_rect)

def draw_button(screen, text, location, font = start_font, button_color = constants.DARKGRAY, text_color = constants.BLACK):
    """
    Draws a button to the screen.

    Parameters:
    - screen (Any): The screen to draw the button on.
    - text (str): The text to display on the button.
    - location (tuple): The location of the button (x1, y1, x2, y2).
    - font (Any): The font to use for the text.
    - button_color (Any): The color of the button.
    - text_color (Any): The color of the text.

    """

    button = pygame.Rect(location)
    pygame.draw.rect(screen, button_color, button)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center = button.center)
    screen.blit(text_surface, text_rect)

def game_start_menu():
    """
    Generates the game start menu in which the user selects the types of players (human or AI) that
    will be playing. To select the AI engine, the user will be prompted to select the depth of the AI.

    Returns:
    tuple: (white_player, white_depth, black_player, black_depth)
    
    """

    running = True
    clock = pygame.time.Clock()

    while running:
        start_screen = pygame.display.set_mode((constants.START_SCREEN_WIDTH, constants.START_SCREEN_HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption('Chess Game Mode Selection')
        start_screen.fill(constants.WHITE)

        # Define button locations
        button_width, button_height = 300, 50
        button1_location = pygame.Rect(100, 100, button_width, button_height)
        button2_location = pygame.Rect(100, 200, button_width, button_height)
        button3_location = pygame.Rect(100, 300, button_width, button_height)
        button4_location = pygame.Rect(100, 400, button_width, button_height)

        # Draw buttons
        draw_text("Welcome to Chess!", start_font, constants.BLACK, start_screen, constants.START_SCREEN_WIDTH // 2, 50)
        draw_button(start_screen, "W: Player vs. B: Player", button1_location)
        draw_button(start_screen, "W: Player vs. B: AI", button2_location)
        draw_button(start_screen, "W: AI vs. B: Player", button3_location)
        draw_button(start_screen, "W: AI vs. B: AI", button4_location)

        # Check for button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button1_location.collidepoint(mouse_pos):
                    white_player = "human"
                    black_player = "human"
                    return (white_player, None, black_player, None)
                elif button2_location.collidepoint(mouse_pos):
                    white_player = "human"
                    _, black_player, black_depth = select_ai_menu("black")
                    return (white_player, None, black_player, black_depth)
                elif button3_location.collidepoint(mouse_pos):
                    _, white_player, white_depth = select_ai_menu("white")
                    black_player = "human"                    
                    return (white_player, white_depth, black_player, None)
                elif button4_location.collidepoint(mouse_pos):
                    _, white_player, white_depth = select_ai_menu("white")
                    _, black_player, black_depth = select_ai_menu("black")
                    return (white_player, white_depth, black_player, black_depth)
        
        pygame.display.flip()  # Update the display
        clock.tick(constants.FRAME_RATE)
    pygame.quit()

def select_ai_menu(player_color):
    """
    Generates the AI selection menu.

    Parameters:
    - player_color (str): The color of the player ('white' or 'black').

    Returns:
    str: The selected AI engine.
    
    """

    running = True
    clock = pygame.time.Clock()
    ai_screen = pygame.display.set_mode((constants.START_SCREEN_WIDTH, constants.START_SCREEN_HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption(f'Select AI Engine for {player_color} Player')

    while running:

        ai_screen.fill(constants.WHITE)

        # Define button locations
        button_width, button_height = 300, 50
        button1_location = pygame.Rect(100, 100, button_width, button_height)
        button2_location = pygame.Rect(100, 200, button_width, button_height)
        button3_location = pygame.Rect(100, 300, button_width, button_height)
        button4_location = pygame.Rect(100, 400, button_width, button_height)

        # Draw buttons
        draw_text("Welcome to Chess!", start_font, constants.BLACK, ai_screen, constants.START_SCREEN_WIDTH // 2, 50)
        draw_button(ai_screen, "Random Engine", button1_location)
        draw_button(ai_screen, "Minimax Engine", button2_location)
        draw_button(ai_screen, "MCTS Engine", button3_location)
        draw_button(ai_screen, "Stockfish Engine", button4_location)

        # Check for button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button1_location.collidepoint(mouse_pos):
                    return f"{player_color}_ai", "Random AI", None
                elif button2_location.collidepoint(mouse_pos):
                    depth = select_depth_menu(player_color, "Minimax AI")
                    return f"{player_color}_ai", "Minimax AI", depth
                elif button3_location.collidepoint(mouse_pos):
                    depth = select_MCTS_search_menu(player_color, "MCTS AI")
                    return f"{player_color}_ai", "MCTS AI", depth
                elif button4_location.collidepoint(mouse_pos):
                    depth = select_depth_menu(player_color, "Stockfish AI")
                    return f"{player_color}_ai", "Stockfish AI", depth
        
        pygame.display.flip()  # Update the display
        clock.tick(constants.FRAME_RATE)
    pygame.quit()

def select_depth_menu(player_color, ai_engine):
    """
    Generates the AI depth selection menu.

    Parameters:
    - player_color (str): The color of the player ('white' or 'black').
    - ai_engine (str): The AI engine name.

    Returns:
    int: The selected depth for the AI engine.
    
    """
    running = True
    clock = pygame.time.Clock()
    ai_depth_screen = pygame.display.set_mode((constants.START_SCREEN_WIDTH, constants.START_SCREEN_HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption(f"Select Depth for {player_color}'s {ai_engine} AI Engine")

    while running:

        ai_depth_screen.fill(constants.WHITE)

        # Define button locations
        button_width, button_height = 50, 50
        button_gap = 10
        buttons = []

        for i in range(10):
            x = 100 + (i % 5) * (button_width + button_gap)
            y = 100 + (i // 5) * (button_height + button_gap)
            buttons.append(pygame.Rect(x, y, button_width, button_height))

        # Draw buttons
        draw_text("Welcome to Chess!", start_font, constants.BLACK, ai_depth_screen, constants.START_SCREEN_WIDTH // 2, 50)

        for i, button in enumerate(buttons):
            draw_button(ai_depth_screen, str(i + 1), button, start_font)

        # Check for button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        print(f"Depth selected: {i + 1}")
                        return i + 1
                    
        pygame.display.flip()  # Update the display
        clock.tick(constants.FRAME_RATE)
    pygame.quit()

def select_MCTS_search_menu(player_color, ai_engine):
    """
    Generates the AI depth selection menu.

    Parameters:
    - player_color (str): The color of the player ('white' or 'black').
    - ai_engine (str): The AI engine name.

    Returns:
    int: The selected depth for the AI engine.
    
    """
    running = True
    clock = pygame.time.Clock()
    ai_depth_screen = pygame.display.set_mode((constants.START_SCREEN_WIDTH, constants.START_SCREEN_HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption(f"Select Depth for {player_color}'s {ai_engine} AI Engine")

    while running:

        ai_depth_screen.fill(constants.WHITE)

        # Define button locations
        button_width, button_height = 75, 50
        button_gap = 10
        buttons = []

        for i in range(20):
            x = 50 + (i % 5) * (button_width + button_gap)
            y = 100 + (i // 5) * (button_height + button_gap)
            buttons.append(pygame.Rect(x, y, button_width, button_height))

        # Draw buttons
        draw_text("Welcome to Chess!", start_font, constants.BLACK, ai_depth_screen, constants.START_SCREEN_WIDTH // 2, 50)

        for i, button in enumerate(buttons):
            draw_button(ai_depth_screen, str((i + 1) * 100), button, start_font)

        # Check for button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        print(f"Depth selected: {(i + 1)*100}")
                        return (i + 1)*100
                    
        pygame.display.flip()  # Update the display
        clock.tick(constants.FRAME_RATE)
    pygame.quit()

def play_again_menu():
    """
    Generates the play again menu.

    Returns:
    bool: True if the user wants to play again, False otherwise
    
    """

    running = True
    clock = pygame.time.Clock()
    play_again_screen = pygame.display.set_mode((constants.START_SCREEN_WIDTH, constants.START_SCREEN_HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption('Game Over!')

    while running:

        play_again_screen.fill(constants.WHITE)

        # Define button locations
        button_width, button_height = 300, 50
        button1_location = pygame.Rect(100, 150, button_width, button_height)
        button2_location = pygame.Rect(100, 300, button_width, button_height)

        # Draw buttons
        draw_text("Do you want to play again?", start_font, constants.BLACK, play_again_screen, constants.START_SCREEN_WIDTH // 2, 50)
        draw_button(play_again_screen, "Yes", button1_location)
        draw_button(play_again_screen, "No", button2_location)

        # Check for button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button1_location.collidepoint(mouse_pos):
                    return True
                elif button2_location.collidepoint(mouse_pos):
                    return False
        
        pygame.display.flip()  # Update the display
        clock.tick(constants.FRAME_RATE)
    pygame.quit()