import pygame

# Initialize Pygame
pygame.init()

# Colors & Settings
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

class Piece:
    def __init__(self, color, type):
        self.color = color
        self.type = type
        self.has_moved = False

    def valid_moves(self, board, x, y, board_instance, check_castling=True):
        """Return a list of valid moves for this piece."""
        moves = []

        # Pawn Movement
        if self.type == "pawn":
            if self.color == "white":
                # Move one square forward if no piece is blocking
                if y - 1 >= 0 and board[y - 1][x] is None:
                    moves.append((x, y - 1))
                    # Move two squares forward from starting position if no piece is blocking
                    if y == 6 and board[y - 2][x] is None:
                        moves.append((x, y - 2))
                # Diagonal captures
                if y - 1 >= 0 and x - 1 >= 0 and board[y - 1][x - 1] and board[y - 1][x - 1].color == "black":
                    moves.append((x - 1, y - 1))
                if y - 1 >= 0 and x + 1 < 8 and board[y - 1][x + 1] and board[y - 1][x + 1].color == "black":
                    moves.append((x + 1, y - 1))
            else:  # If pawn is black
                # Move one square forward if no piece is blocking
                if y + 1 < 8 and board[y + 1][x] is None:
                    moves.append((x, y + 1))
                    # Move two squares forward from starting position if no piece is blocking
                    if y == 1 and board[y + 2][x] is None:
                        moves.append((x, y + 2))
                # Diagonal captures
                if y + 1 < 8 and x - 1 >= 0 and board[y + 1][x - 1] and board[y + 1][x - 1].color == "white":
                    moves.append((x - 1, y + 1))
                if y + 1 < 8 and x + 1 < 8 and board[y + 1][x + 1] and board[y + 1][x + 1].color == "white":
                    moves.append((x + 1, y + 1))

        # Rook Movement
        if self.type == "rook":
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, right, up, left
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 8 and 0 <= ny < 8:
                    if board[ny][nx] is None:
                        moves.append((nx, ny))
                    else:
                        if board[ny][nx].color != self.color:
                            moves.append((nx, ny))
                        break  # Stop if there's a piece blocking the path
                    nx += dx
                    ny += dy
        # Knight Movement
        if self.type == "knight":
            knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
            for dx, dy in knight_moves:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and (board[ny][nx] is None or board[ny][nx].color != self.color):
                    moves.append((nx, ny))

        # Bishop Movement
        if self.type == "bishop":
            directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]  # Diagonal directions
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 8 and 0 <= ny < 8:
                    if board[ny][nx] is None:
                        moves.append((nx, ny))
                    else:
                        if board[ny][nx].color != self.color:
                            moves.append((nx, ny))
                        break  # Stop if there's a piece blocking the path
                    nx += dx
                    ny += dy

        # Queen Movement
        if self.type == "queen":
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (-1, -1),
                          (1, -1)]  # Combining rook and bishop directions
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 8 and 0 <= ny < 8:
                    if board[ny][nx] is None:
                        moves.append((nx, ny))
                    else:
                        if board[ny][nx].color != self.color:
                            moves.append((nx, ny))
                        break  # Stop if there's a piece blocking the path
                    nx += dx
                    ny += dy


        # King Movement
        if self.type == "king":
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (-1, -1),
                          (1, -1)]  # All 8 surrounding squares
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and (board[ny][nx] is None or board[ny][nx].color != self.color):
                    moves.append((nx, ny))

            # Castling logic (moved outside the loop)
            if check_castling:  # <-- This is where you add the condition
                if not self.has_moved and not board_instance.is_square_attacked(x, y, board,
                                                                                "white" if self.color == "black" else "black"):
                    # King-side castling (short)
                    if board[y][x + 1] is None and board[y][x + 2] is None:
                        rook = board[y][x + 3]
                        if rook and rook.type == "rook" and not rook.has_moved:
                            if not board_instance.is_square_attacked(x + 1, y, board,
                                                                     "white" if self.color == "black" else "black") and \
                                    not board_instance.is_square_attacked(x + 2, y, board,
                                                                          "white" if self.color == "black" else "black"):
                                moves.append((x + 2, y))

                    # Queen-side castling (long)
                    if board[y][x - 1] is None and board[y][x - 2] is None and board[y][x - 3] is None:
                        rook = board[y][x - 4]
                        if rook and rook.type == "rook" and not rook.has_moved:
                            if not board_instance.is_square_attacked(x - 1, y, board,
                                                                     "white" if self.color == "black" else "black") and \
                                    not board_instance.is_square_attacked(x - 2, y, board,
                                                                          "white" if self.color == "black" else "black"):
                                moves.append((x - 2, y))

        return moves


# ... [previous code]

class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        # Pawn
        for i in range(8):
            board[1][i] = Piece("black", "pawn")
            board[6][i] = Piece("white", "pawn")


        # Rooks
        board[0][0] = Piece("black", "rook")
        board[0][7] = Piece("black", "rook")
        board[7][0] = Piece("white", "rook")
        board[7][7] = Piece("white", "rook")

        # Knights
        board[0][1] = Piece("black", "knight")
        board[0][6] = Piece("black", "knight")
        board[7][1] = Piece("white", "knight")
        board[7][6] = Piece("white", "knight")

        # Bishops
        board[0][2] = Piece("black", "bishop")
        board[0][5] = Piece("black", "bishop")
        board[7][2] = Piece("white", "bishop")
        board[7][5] = Piece("white", "bishop")

        # Queens
        board[0][3] = Piece("black", "queen")
        board[7][3] = Piece("white", "queen")

        # Kings
        board[0][4] = Piece("black", "king")
        board[7][4] = Piece("white", "king")

        return board

    def is_square_attacked(self, x, y, board, by_color):
        """Check if a square is attacked by the given color."""
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece and piece.color == by_color:
                    if (x, y) in piece.valid_moves(board, j, i, self, check_castling=False):
                        return True
        return False

    def draw(self, win, valid_moves=[]):  # Add valid_moves parameter with a default empty list

        # Draw squares
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(win, WHITE if (row + col) % 2 == 0 else BLACK,
                                 (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                # Draw piece if it exists
                piece = self.board[row][col]
                if piece:
                    # This is a basic representation; you'd replace this with actual graphics
                    pygame.draw.circle(win, BLACK if piece.color == "black" else WHITE,
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                       SQUARE_SIZE // 3)
                    font = pygame.font.SysFont(None, 55)

                    # Check if the piece is a knight and render lowercase "k" accordingly
                    char_to_render = piece.type[0]
                    if piece.type == "knight":
                        char_to_render = "k"

                    char_to_render = piece.type[0].lower() if piece.type == "knight" else piece.type[0].upper()
                    text = font.render(char_to_render, True, WHITE if piece.color == "black" else BLACK)
                    win.blit(text, (col * SQUARE_SIZE + (SQUARE_SIZE - text.get_width()) // 2,
                                    row * SQUARE_SIZE + (SQUARE_SIZE - text.get_height()) // 2))
                    # Inside the draw method of the Board class, after drawing the pieces

                    for move in valid_moves:
                        pygame.draw.circle(win, (255, 0, 0),  # Use red color for highlighting
                                           (move[0] * SQUARE_SIZE + SQUARE_SIZE // 2,
                                            move[1] * SQUARE_SIZE + SQUARE_SIZE // 2),
                                           10)  # Circle radius for highlighting

    def move(self, start, end):
        """Move a piece on the board."""
        x1, y1 = start
        x2, y2 = end
        piece = self.board[y1][x1]
        if piece and end in piece.valid_moves(self.board, x1, y1, self):
            piece.has_moved = True
            self.board[y2][x2] = piece
            self.board[y1][x1] = None

            # Castling logic
            if piece.type == "king" and abs(x2 - x1) == 2:
                if x2 > x1:  # King-side castling
                    self.board[y1][7], self.board[y1][5] = None, self.board[y1][7]
                else:  # Queen-side castling
                    self.board[y1][0], self.board[y1][3] = None, self.board[y1][0]


class Game:
    def __init__(self, win):
        self.win = win
        self.board = Board()
        self.selected_piece = None
        self.turn = "white"  # Start with white's turn by default
        self.valid_moves = []  # Initialize an empty list for valid moves

    def update_display(self):
        self.board.draw(self.win, self.valid_moves)  # Pass the valid moves list
        pygame.display.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    col, row = event.pos
                    col //= SQUARE_SIZE
                    row //= SQUARE_SIZE

                    piece = self.board.board[row][col]
                    if not self.selected_piece and piece and piece.color == self.turn:
                        self.selected_piece = (col, row)
                        self.valid_moves = piece.valid_moves(self.board.board, col, row, self.board)
                    elif self.selected_piece:
                        if (col, row) in self.valid_moves:
                            self.board.move(self.selected_piece, (col, row))
                            self.selected_piece = None
                            self.valid_moves = []
                            # Switch the turn only if a valid move was made
                            self.turn = "black" if self.turn == "white" else "white"
                        else:
                            # Deselect the piece if clicked again or if an invalid move was attempted
                            self.selected_piece = None
                            self.valid_moves = []

            self.update_display()

        pygame.quit()


# Run the game
game = Game(win)
game.run()
