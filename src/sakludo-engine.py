import pygame
import sys

pygame.init()

icon = pygame.image.load("assets/icon/icon.png")
pygame.display.set_icon(icon)

WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sakludo Engine v1.2.2")

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
    "p": pygame.image.load("assets/pieces/b_pawn.png"),
    "r": pygame.image.load("assets/pieces/b_rook.png"),
    "n": pygame.image.load("assets/pieces/b_knight.png"),
    "b": pygame.image.load("assets/pieces/b_bishop.png"),
    "q": pygame.image.load("assets/pieces/b_queen.png"),
    "k": pygame.image.load("assets/pieces/b_king.png"),
    "P": pygame.image.load("assets/pieces/w_pawn.png"),
    "R": pygame.image.load("assets/pieces/w_rook.png"),
    "N": pygame.image.load("assets/pieces/w_knight.png"),
    "B": pygame.image.load("assets/pieces/w_bishop.png"),
    "Q": pygame.image.load("assets/pieces/w_queen.png"),
    "K": pygame.image.load("assets/pieces/w_king.png"),
}

def draw_board(board, selected=None):
    font = pygame.font.Font(None, 24)
    
    text_color = (50, 50, 50)
    
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

            if col == 0:
                text = font.render(str(8 - row), True, text_color)
                SCREEN.blit(text, (col * TILE_SIZE + 5, row * TILE_SIZE + 5))

            if row == 7:
                text = font.render(chr(97 + col), True, text_color)
                SCREEN.blit(text, (col * TILE_SIZE + TILE_SIZE - 25, row * TILE_SIZE + TILE_SIZE - 30))
                
def is_valid_move(board, start, end, turn, castling_rights):
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

        if turn == "white" and piece == "K":
            if sx == 4 and sy == 7:
                if ex == 6 and castling_rights["white"]["king"] and board[7][5] == "" and board[7][6] == "":
                    return True
                if ex == 2 and castling_rights["white"]["queen"] and board[7][3] == "" and board[7][2] == "" and board[7][1] == "":
                    return True

        if turn == "black" and piece == "k":
            if sx == 4 and sy == 0:
                if ex == 6 and castling_rights["black"]["king"] and board[0][5] == "" and board[0][6] == "":
                    return True
                if ex == 2 and castling_rights["black"]["queen"] and board[0][3] == "" and board[0][2] == "" and board[0][1] == "":
                    return True

    return False

def move_piece(board, start, end, turn, castling_rights):
    sx, sy = start
    ex, ey = end
    piece = board[sy][sx]

    if piece.lower() == "k" and abs(ex - sx) == 2:
        if turn == "white" and sy == 7:
            if ex == 6:
                board[ey][ex] = board[sy][sx]
                board[ey][ex - 1] = board[7][7]
                board[7][7] = ""
                board[sy][sx] = ""
            elif ex == 2:
                board[ey][ex] = board[sy][sx]
                board[ey][ex + 1] = board[7][0]
                board[7][0] = ""
                board[sy][sx] = ""

        elif turn == "black" and sy == 0:
            if ex == 6:
                board[ey][ex] = board[sy][sx]
                board[ey][ex - 1] = board[0][7]
                board[0][7] = ""
                board[sy][sx] = ""
            elif ex == 2:
                board[ey][ex] = board[sy][sx]
                board[ey][ex + 1] = board[0][0]
                board[0][0] = ""
                board[sy][sx] = ""

    else:
        board[ey][ex] = board[sy][sx]
        board[sy][sx] = ""

    if piece == "K":
        castling_rights["white"]["king"] = False
        castling_rights["white"]["queen"] = False
    elif piece == "k":
        castling_rights["black"]["king"] = False
        castling_rights["black"]["queen"] = False

def main():
    board = [row[:] for row in INITIAL_BOARD]
    selected = None
    turn = "white"
    castling_rights = {
        "white": {"king": True, "queen": True},
        "black": {"king": True, "queen": True},
    }
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // TILE_SIZE, y // TILE_SIZE
                
                if selected:
                    if is_valid_move(board, selected, (col, row), turn, castling_rights):
                        move_piece(board, selected, (col, row), turn, castling_rights)
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