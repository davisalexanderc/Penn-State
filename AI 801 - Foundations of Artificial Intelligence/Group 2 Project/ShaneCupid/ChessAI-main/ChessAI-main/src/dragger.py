# Class Dragger:
# Tracks the piece being dragged.
# Updates the position of the dragged piece.
# Manages the initial and current mouse positions during dragging.


import pygame
from const import *

class Dragger:
    def __init__(self):
        # Initialize the dragger with default values
        self.piece = None         # The piece being dragged
        self.dragging = False     # Indicates if a piece is being dragged
        self.mouseX = 0           # Current X position of the mouse
        self.mouseY = 0           # Current Y position of the mouse
        self.initial_row = 0      # Initial row position of the piece
        self.initial_col = 0      # Initial column position of the piece

    # Method to update the blit (render) of the piece being dragged
    def update_blit(self, surface):
        # Set the texture size of the piece to 128 pixels
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # Load the image of the piece
        img = pygame.image.load(texture)
        # Get the rectangle of the image with the center at the current mouse position
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        # Draw the piece at its new position
        surface.blit(img, self.piece.texture_rect)

    # Method to update the mouse position
    def update_mouse(self, pos):
        # Set the mouseX and mouseY to the current position
        self.mouseX, self.mouseY = pos

    # Method to save the initial position of the piece being dragged
    def save_initial(self, pos):
        # Calculate the initial row and column based on the position
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    # Method to start dragging the piece
    def drag_piece(self, piece):
        self.piece = piece        # Set the piece being dragged
        self.dragging = True      # Set dragging to True

    # Method to stop dragging the piece
    def undrag_piece(self):
        self.piece = None         # Clear the piece being dragged
        self.dragging = False     # Set dragging to False
