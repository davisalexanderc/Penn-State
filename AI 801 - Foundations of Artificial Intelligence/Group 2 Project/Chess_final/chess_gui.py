import pygame
import chess

pygame.init()

# Constants
WIDTH, HEIGHT = 850, 1000
SQUARE_SIZE = 100
BOARDER = 25
PIECE_SIZE = 100

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TAN = (210, 180, 140) # For the board color
DARKGRAY = (100, 100, 100)

def load_piece_images():
    pieces = {}
    black_pieces = ['r', 'n', 'b', 'q', 'k', 'p']
    white_pieces = ['R', 'N', 'B', 'Q', 'K', 'P']
    for piece in black_pieces:
        pieces[piece] = pygame.transform.scale(pygame.image.load(f'assets/Images/black_pieces/{piece}.png'), (PIECE_SIZE, PIECE_SIZE))

    for piece in white_pieces:
        pieces[piece] = pygame.transform.scale(pygame.image.load(f'assets/Images/white_pieces/{piece}.png'), (PIECE_SIZE, PIECE_SIZE))    
    
    return pieces

# Draw Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')
piece_images = load_piece_images()
pygame.draw.rect(screen, TAN, (0, 0, 850, 1000), 25)
pygame.draw.rect(screen, TAN, (0, 825, 850, 825), 25) 

def draw_board(screen, board, piece_images):
    for row in range(8):
        for col in range(8):
            color = DARKGRAY if (row + col) % 2 == 0 else WHITE
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE + BOARDER, row * SQUARE_SIZE + BOARDER, SQUARE_SIZE, SQUARE_SIZE))
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                piece_image = piece_images[piece.symbol()] 
                screen.blit(piece_image, (col * SQUARE_SIZE + BOARDER, row * SQUARE_SIZE + BOARDER))
    pygame.display.flip()

def update_display(board):
    draw_board(screen, board, piece_images)

def main_loop(board):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_display(board)
    pygame.quit()