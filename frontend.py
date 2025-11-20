import pygame
from rules import BOARD

# Pygame display settings
WIDTH, HEIGHT = 640, 640
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (240, 240, 240)
GREEN = (50, 140, 50)
LIGHT_YELLOW = (245, 235, 160)
BLACK = (20, 20, 20)
PIECE_WHITE = (255, 255, 255)
PIECE_BLACK = (0, 0, 0)


def draw_board(win):
    """Draw 8x8 board with alternating light/dark squares."""
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_YELLOW if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(win, color,
                             (col * SQUARE_SIZE, row * SQUARE_SIZE,
                              SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(win):
    """Draw pieces based on the backend BOARD dict."""
    for (row, col), piece in BOARD.items():
        if piece is None:
            continue

        radius = SQUARE_SIZE // 2 - 10
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2

        color = PIECE_WHITE if piece.colour == "white" else PIECE_BLACK
        pygame.draw.circle(win, color, (x, y), radius)

        # Draw a ring if it's a king
        if piece.king_status:
            pygame.draw.circle(win, (200, 200, 0), (x, y), radius - 5, 3)


def pygame_loop():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Draughts Frontend")

    selected_piece = None
    selected_pos = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE

                # 1) First click selects a piece
                if selected_piece is None:
                    if BOARD.get((row, col)) is not None:
                        selected_piece = BOARD[(row, col)]
                        selected_pos = (row, col)

                # 2) Second click attempts to move it
                else:
                    new_pos = (row, col)

                    # Example: try diagonal moves
                    dr = new_pos[0] - selected_pos[0]
                    dc = new_pos[1] - selected_pos[1]

                    if dr == 1 and dc == 1:
                        if selected_piece.colour == 'black':
                            selected_piece.move_right(selected_pos)
                        # elif selected_piece.colour == 'white':
                        #   selected_piece.move_back_right(selected_pos)

                    elif dr == 1 and dc == -1:
                        if selected_piece.colour == 'black':
                            selected_piece.move_left(selected_pos)

                    elif dr == -1 and dc == 1:
                        if selected_piece.colour == 'white':
                            selected_piece.move_right(selected_pos)
                    
                    elif dr == -1 and dc == -1:
                        if selected_piece.colour == 'white':
                            selected_piece.move_left(selected_pos)

                    # Reset selection
                    selected_piece = None
                    selected_pos = None

        draw_board(win)
        draw_pieces(win)
        pygame.display.update()

    pygame.quit()
