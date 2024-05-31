import pygame

class Piece:
    def __init__(self, color, piece_type, position):
        """
        Initializes the Piece class.

        Parameters:
        - color (str): The color of the piece ('w' or 'b').
        - piece_type (str): The type of the piece ('P', 'R', 'K', 'B', 'Q', 'K').
        - position (tuple): The position of the piece on the board (row, column).

        This method:
        - Initializes the piece color and type.
        - Initializes the piece name based on the color and type.
        - Loads the piece image based on the piece name.
        - Initializes the piece image rectangle.
        """

        self.color = color
        self.piece_type = piece_type
        self.name = color + piece_type
        self.position = position
        self.image = self.load_image()

    def load_image(self):
        """
        Loads the image of the piece based on the color and type.

        This method:
        - Loads the image of the piece based on the color and type.
        - Returns the loaded image.
        """

        image = pygame.image.load(f'./assets/Images/{self.name}.png')
        scaler = 1.6
        scaled_image = pygame.transform.scale(image, (int(image.get_width() * scaler), int(image.get_height() * scaler)))
        return scaled_image

    def draw(self, screen):
        """
        Draws the piece on the screen.

        Parameters:
        - screen (pygame.Surface): The surface to draw the piece on.

        This method:
        - Draws the piece image on the screen at the specified position.
        """

        row, col = self.position
        x = col * 100 + 25
        y = row * 100 + 25
        screen.blit(self.image, (x, y))  # Blit the piece image on the screen at the specified position

