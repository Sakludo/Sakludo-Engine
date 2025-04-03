import pygame
import sys

pygame.init()

icon = pygame.image.load("assets/icon/icon.png")
pygame.display.set_icon(icon)

WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sakludo Engine v1.2.0")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)

TILE_SIZE = WIDTH // 8

def draw_board():
    # Draws the chessboard
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(SCREEN, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def main():
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()