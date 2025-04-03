import pygame
import sys

pygame.init()

icon = pygame.image.load("assets/icon/icon.png")
pygame.display.set_icon(icon)

WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sakludo Engine v1.2.1")

LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
SELECTED = (255, 255, 0)

TILE_SIZE = WIDTH // 8

INITIAL_BOARD = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]

PIECES = {
    "p": pygame.image.load("pieces/b_pawn.png"),
    "r": pygame.image.load("pieces/b_rook.png"),
    "n": pygame.image.load("pieces/b_knight.png"),
    "b": pygame.image.load("pieces/b_bishop.png"),
    "q": pygame.image.load("pieces/b_queen.png"),
    "k": pygame.image.load("pieces/b_king.png"),
    "P": pygame.image.load("pieces/w_pawn.png"),
    "R": pygame.image.load("pieces/w_rook.png"),
    "N": pygame.image.load("pieces/w_knight.png"),
    "B": pygame.image.load("pieces/w_bishop.png"),
    "Q": pygame.image.load("pieces/w_queen.png"),
    "K": pygame.image.load("pieces/w_king.png"),
}

def draw_board(board, selected=None):
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            
            if selected and selected == (col, row):
                color = SELECTED
            
            pygame.draw.rect(SCREEN, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
            piece = board[row][col]
            if piece:
                SCREEN.blit(pygame.transform.scale(PIECES[piece], (TILE_SIZE, TILE_SIZE)),
                            (col * TILE_SIZE, row * TILE_SIZE))

def is_valid_move(board, start, end, turn):
    sx, sy = start
    ex, ey = end
    piece = board[sy][sx]
    target = board[ey][ex]

    if turn == "white" and not piece.isupper():
        return False
    if turn == "black" and not piece.islower():
        return False

    if piece.lower() == "p":
        direction = -1 if piece.isupper() else 1
        start_row = 6 if piece.isupper() else 1

        if ex == sx and target == "":
            if (ey - sy) == direction:
                return True
            if (ey - sy) == 2 * direction and sy == start_row and board[sy + direction][sx] == "":
                return True

        if abs(ex - sx) == 1 and (ey - sy) == direction and target != "" and target.islower() != piece.islower():
            return True

    if piece.lower() == "r":
        if sx == ex or sy == ey:
            step_x = (ex - sx) // max(1, abs(ex - sx)) if ex != sx else 0
            step_y = (ey - sy) // max(1, abs(ey - sy)) if ey != sy else 0
            for i in range(1, max(abs(ex - sx), abs(ey - sy))):
                if board[sy + i * step_y][sx + i * step_x] != "":
                    return False
            return target == "" or target.islower() != piece.islower()

    if piece.lower() == "b":
        if abs(ex - sx) == abs(ey - sy):
            step_x = (ex - sx) // abs(ex - sx)
            step_y = (ey - sy) // abs(ey - sy)
            for i in range(1, abs(ex - sx)):
                if board[sy + i * step_y][sx + i * step_x] != "":
                    return False
            return target == "" or target.islower() != piece.islower()

    if piece.lower() == "q":
        if sx == ex or sy == ey:
            step_x = (ex - sx) // max(1, abs(ex - sx)) if ex != sx else 0
            step_y = (ey - sy) // max(1, abs(ey - sy)) if ey != sy else 0
            for i in range(1, max(abs(ex - sx), abs(ey - sy))):
                if board[sy + i * step_y][sx + i * step_x] != "":
                    return False
            return target == "" or target.islower() != piece.islower()

        if abs(ex - sx) == abs(ey - sy):
            step_x = (ex - sx) // abs(ex - sx)
            step_y = (ey - sy) // abs(ey - sy)
            for i in range(1, abs(ex - sx)):
                if board[sy + i * step_y][sx + i * step_x] != "":
                    return False
            return target == "" or target.islower() != piece.islower()

    if piece.lower() == "n":
        if (abs(ex - sx), abs(ey - sy)) in [(2, 1), (1, 2)]:
            return target == "" or target.islower() != piece.islower()

    if piece.lower() == "k":
        if max(abs(ex - sx), abs(ey - sy)) == 1:
            return target == "" or target.islower() != piece.islower()

    return False

def move_piece(board, start, end):
    sx, sy = start
    ex, ey = end
    board[ey][ex] = board[sy][sx]
    board[sy][sx] = ""

def main():
    board = [row[:] for row in INITIAL_BOARD]
    selected = None
    turn = "white"
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // TILE_SIZE, y // TILE_SIZE
                
                if selected:
                    if is_valid_move(board, selected, (col, row), turn):
                        move_piece(board, selected, (col, row))
                        turn = "black" if turn == "white" else "white"
                    selected = None
                else:
                    if board[row][col] != "":
                        selected = (col, row)
        
        draw_board(board, selected)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()