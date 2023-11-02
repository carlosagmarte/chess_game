import pygame
import os

pygame.init()

WIDTH, HEIGHT = 800, 800  # Size of the game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

ASSETS_DIR = './assets/'
SQUARE_SIZE = 100
SCALE_FACTOR = 1
PIECE_SIZE = int(SQUARE_SIZE * SCALE_FACTOR)

# Load and scale the board
BOARD = pygame.image.load(ASSETS_DIR + 'board.png')
BOARD = pygame.transform.scale(BOARD, (WIDTH, HEIGHT))

# Load and scale black pieces
B_PAWN = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'b_pawn.png'), (PIECE_SIZE, PIECE_SIZE))
B_ROOK = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'b_rook.png'), (PIECE_SIZE, PIECE_SIZE))
B_KNIGHT = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'b_knight.png'), (PIECE_SIZE, PIECE_SIZE))
B_BISHOP = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'b_bishop.png'), (PIECE_SIZE, PIECE_SIZE))
B_QUEEN = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'b_queen.png'), (PIECE_SIZE, PIECE_SIZE))
B_KING = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'b_king.png'), (PIECE_SIZE, PIECE_SIZE))

# Load and scale white pieces
W_PAWN = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'w_pawn.png'), (PIECE_SIZE, PIECE_SIZE))
W_ROOK = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'w_rook.png'), (PIECE_SIZE, PIECE_SIZE))
W_KNIGHT = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'w_knight.png'), (PIECE_SIZE, PIECE_SIZE))
W_BISHOP = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'w_bishop.png'), (PIECE_SIZE, PIECE_SIZE))
W_QUEEN = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'w_queen.png'), (PIECE_SIZE, PIECE_SIZE))
W_KING = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'w_king.png'), (PIECE_SIZE, PIECE_SIZE))

# Declare a move history list
move_history = []





def load_images():
    images = {}
    pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['w', 'b']
    for color in colors:
        for piece in pieces:
            image = pygame.image.load(f"{ASSETS_DIR}{color}_{piece}.png")
            images[f"{color}_{piece}"] = pygame.transform.scale(image, (PIECE_SIZE, PIECE_SIZE))
    return images

IMAGES = load_images()

class Piece:
    def __init__(self, color, type):
        self.color = color
        self.type = type
        self.has_moved = False  # New attribute for castling
        self.en_passant_target = False  # New attribute for en passant

    def __str__(self):
        return f"{self.color[0]}{self.type[0]}"

board = [[None for _ in range(8)] for _ in range(8)]


for i in range(8):
    board[1][i] = Piece("black", "pawn")
    board[6][i] = Piece("white", "pawn")

# Rooks
board[0][0], board[0][7] = Piece("black", "rook"), Piece("black", "rook")
board[7][0], board[7][7] = Piece("white", "rook"), Piece("white", "rook")

# Knights
board[0][1], board[0][6] = Piece("black", "knight"), Piece("black", "knight")
board[7][1], board[7][6] = Piece("white", "knight"), Piece("white", "knight")

# Bishops
board[0][2], board[0][5] = Piece("black", "bishop"), Piece("black", "bishop")
board[7][2], board[7][5] = Piece("white", "bishop"), Piece("white", "bishop")

# Queens
board[0][3] = Piece("black", "queen")
board[7][3] = Piece("white", "queen")

# Kings
board[0][4] = Piece("black", "king")
board[7][4] = Piece("white", "king")


def is_check(board, king_color):
    # Find the king's position
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece and piece.color == king_color and piece.type == "king":
                king_position = (x, y)
                break

    # Check if any opponent's pieces can move to the king's position
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece and piece.color != king_color:
                if king_position in valid_moves(piece, x, y):
                    return True
    return False

def is_checkmate(board, color):
    # If the player is not in check, they can't be in checkmate
    if not is_check(board, color):
        return False

    # Check all possible moves for the current player
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece and piece.color == color:
                initial_position = (x, y)
                for move in valid_moves(piece, x, y):
                    # Make the move
                    board[move[1]][move[0]] = piece
                    board[y][x] = None

                    # Check if the player is still in check after the move
                    still_in_check = is_check(board, color)

                    # Undo the move
                    board[y][x] = piece
                    board[move[1]][move[0]] = None



def promote_pawn(row, col, color):
    """Promote a pawn to a piece of the player's choice."""
    # Define the promotion options
    pieces = ['queen', 'rook', 'bishop', 'knight']
    piece_images = {
        "white": [W_QUEEN, W_ROOK, W_BISHOP, W_KNIGHT],
        "black": [B_QUEEN, B_ROOK, B_BISHOP, B_KNIGHT]
    }

    # Draw the promotion options on the screen
    for index, image in enumerate(piece_images[color]):
        win.blit(image, (col * 100, row * 100 + index * 100))
    pygame.display.update()

    # Wait for the player's choice
    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_x, clicked_y = event.pos
                print(f"Clicked at: {clicked_x}, {clicked_y}")  # Debugging
                if col * 100 <= clicked_x <= (col + 1) * 100:
                    choice_index = (clicked_y - row * 100) // 100
                    if 0 <= choice_index < 4:
                        print(f"Chose piece: {pieces[choice_index]}")  # Debugging
                        board[row][col] = Piece(color, pieces[choice_index])
                        choosing = False
    draw_window()  # Update the board display after the promotion



# Helper functions for each piece type:
def valid_moves(piece, x, y):
    if piece.type == "pawn":
        return valid_moves_pawn(piece, x, y)
    elif piece.type == "rook":
        return valid_moves_rook(piece, x, y)
    elif piece.type == "knight":
        return valid_moves_knight(piece, x, y)
    elif piece.type == "bishop":
        return valid_moves_bishop(piece, x, y)
    elif piece.type == "queen":
        return valid_moves_queen(piece, x, y)
    elif piece.type == "king":
        return valid_moves_king(piece, x, y)
    else:
        return []


def valid_moves_pawn(piece, x, y):
    moves = []

    # Define direction based on color
    direction = -1 if piece.color == "white" else 1
    opponent = "black" if piece.color == "white" else "white"
    start_row = 6 if piece.color == "white" else 1
    en_passant_row = 3 if piece.color == "white" else 4

    # Forward move
    if 0 <= y + direction < 8 and not board[y + direction][x]:
        moves.append((x, y + direction))

        # Double forward move from starting position
        if y == start_row and not board[y + 2*direction][x]:
            moves.append((x, y + 2*direction))

    # Diagonal captures
    for dx in [-1, 1]:
        if 0 <= x + dx < 8:
            if board[y + direction][x + dx] and board[y + direction][x + dx].color == opponent:
                moves.append((x + dx, y + direction))
            # En passant
            if y == en_passant_row and board[y][x + dx] and board[y][x + dx].type == "pawn" and board[y][x + dx].color == opponent and board[y][x + dx].en_passant_target:
                moves.append((x + dx, y + direction))

    return moves



def valid_moves_rook(piece, x, y):
    moves = []
            # Rook Movement Logic
    if piece.type == "rook":
                # Horizontal and Vertical Movement
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < 8 and 0 <= ny < 8:
                        if not board[ny][nx]:
                            moves.append((nx, ny))
                        else:
                            if board[ny][nx].color != piece.color:
                                moves.append((nx, ny))
                            break
                        nx += dx
                        ny += dy

    return moves

def valid_moves_knight(piece, x, y):
    moves = []
            # Knight Movement Logic
    if piece.type == "knight":
                knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
                for dx, dy in knight_moves:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 8 and 0 <= ny < 8 and (not board[ny][nx] or board[ny][nx].color != piece.color):
                        moves.append((nx, ny))

    return moves

def valid_moves_bishop(piece, x, y):
    moves = []
    if piece.type == "bishop":
                # Diagonal Movement
                for dx, dy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < 8 and 0 <= ny < 8:
                        if not board[ny][nx]:
                            moves.append((nx, ny))
                        else:
                            if board[ny][nx].color != piece.color:
                                moves.append((nx, ny))
                            break
                        nx += dx
                        ny += dy

    return moves

def valid_moves_queen(piece, x, y):
    moves = []
            # Queen Movement Logic
    if piece.type == "queen":
                # Combining Rook and Bishop Movement
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < 8 and 0 <= ny < 8:
                        if not board[ny][nx]:
                            moves.append((nx, ny))
                        else:
                            if board[ny][nx].color != piece.color:
                                moves.append((nx, ny))
                            break
                        nx += dx
                        ny += dy
    return moves

def valid_moves_king(piece, x, y):
    moves = []
    # Implement king-specific logic here...
    if piece.type == "king":
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 8 and 0 <= ny < 8 and (not board[ny][nx] or board[ny][nx].color != piece.color):
                        moves.append((nx, ny))

    return moves

    if piece.type == "king" and not piece.has_moved and not is_check(board, piece.color):

        if x + 3 < 8 and not board[y][x + 1] and not board[y][x + 2] and not board[y][x + 3] and board[y][
            x + 3].type == "rook" and not board[y][x + 3].has_moved:
            # Check if squares the king moves through are attacked
            if not is_check(board, piece.color, (x + 1, y)) and not is_check(board, piece.color, (x + 2, y)):
                moves.append((x + 2, y))

        if x - 4 >= 0 and not board[y][x - 1] and not board[y][x - 2] and not board[y][x - 3] and board[y][
            x - 4].type == "rook" and not board[y][x - 4].has_moved:
            # Check if squares the king moves through are attacked
            if not is_check(board, piece.color, (x - 1, y)) and not is_check(board, piece.color, (x - 2, y)):
                moves.append((x - 2, y))

    # Inside valid_moves function
    if piece.type == "pawn" and y == 3 and board[y - 1][x + 1] and board[y - 1][x + 1].type == "pawn" and board[y - 1][
        x + 1].color != piece.color and board[y - 1][x + 1].en_passant_target:
        moves.append((x + 1, y - 1))

    if piece.type == "pawn" and y == 3 and board[y - 1][x - 1] and board[y - 1][x - 1].type == "pawn" and board[y - 1][
        x - 1].color != piece.color and board[y - 1][x - 1].en_passant_target:
        moves.append((x - 1, y - 1))

    if piece.type == "pawn":
        if piece.color == "white" and y == 0:
            promote_pawn(y, x, "white")
        elif piece.color == "black" and y == 7:
            promote_pawn(y, x, "black")
    return moves

def move_piece(selected_piece, selected_position, row, col):
    """Move a piece on the board from the selected_position to (row, col)."""
    board[row][col] = selected_piece
    board[selected_position[0]][selected_position[1]] = None


def draw_window():
    win.blit(BOARD, (0, 0))
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece:
                win.blit(IMAGES[f"{piece.color[0]}_{piece.type}"], (j * 100, i * 100))
    pygame.display.update()
    pygame.display.update()


selected_piece = None
selected_position = None


# ... [The rest of the code remains unchanged]

def main():
    global selected_piece, selected_position
    current_turn = "white"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // 100, y // 100
                if not selected_piece and board[row][col] and board[row][col].color == current_turn:
                    selected_piece = board[row][col]
                    selected_position = (row, col)
                elif selected_piece:  # This line was fixed (indentation)
                    if (row, col) in valid_moves(selected_piece, selected_position[1], selected_position[0]):
                        move_piece(selected_piece, selected_position, row, col)
                        selected_piece = None
                        selected_position = None
                        current_turn = "black" if current_turn == "white" else "white"
                    else:
                        print("Invalid move!")

        # Check for pawn promotion
        if selected_piece and selected_piece.type == "pawn":
            if selected_piece.color == "white" and row == 0:
                promote_pawn(row, col, "white")
            elif selected_piece.color == "black" and row == 7:
                promote_pawn(row, col, "black")

        if is_checkmate(board, current_turn):
            print(f"{current_turn} is in checkmate!")
            running = False
        elif is_check(board, current_turn):
            print(f"{current_turn} is in check!")

        draw_window()


if __name__ == "__main__":
    main()
    pygame.quit()
