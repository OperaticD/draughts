import pygame
from rules import BOARD, all_pieces, black_pieces, captured_position
import logging
import random

logger = logging.getLogger(__name__)

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


def click_move(selected_piece: object, selected_pos: tuple[int, int], new_pos: tuple[int, int], must_take: bool, allowed_pieces: list[object]) -> tuple[int, object]:
    # Must capture rule
    if must_take and selected_piece not in allowed_pieces:
        logger.error("Must capture a piece.")
        return None, None, None
    
    if selected_piece in allowed_pieces:
        # new_pos = (row, col)

        # calculate movement
        dr = new_pos[0] - selected_pos[0]
        dc = new_pos[1] - selected_pos[1]

        if abs(dr) == 1 and abs(dc) == 1 and must_take == False:
            success = selected_piece.move_single(selected_pos, new_pos)
            if success == 200:
                return success, None, None

        # if double move
        elif abs(dr) == 2 and abs(dc) == 2: # if must_take == False, there will be an error when we check valid move

            success = selected_piece.move_double(selected_pos, new_pos)
            if success == 200:
                if selected_piece.can_take():
                # The piece has just moved, so its new selected_pos is the old new_pos
                    selected_pos = new_pos
                    allowed_pieces = [selected_piece]
                    return 200, selected_piece, selected_pos
                else:
                    must_take = False
                    return 200, None, None

            return 200, None, None
            
    return 400, selected_piece, selected_pos
            

def ai_move():
    # check score of each can_move_double and track piece, new square, score
    active_black_pieces = [p for p in black_pieces if p.active]
    valid_moves = []
    must_take = False
    for piece in active_black_pieces:
        position = next((k for k, v in BOARD.items() if v == piece), None)
        if position is not None:
            double = piece.check_double(position) # returns [(piece, pos, new_pos, score)] or list if many double
            if double:
                must_take = True
                valid_moves.append(double)

            if not must_take:
                r, c = position
                # direction pairs for standard movement
                directions = [(1, -1), (1, 1)]
                if piece.king_status:
                    directions += [(-1, -1), (-1, 1)]

                for dr, dc in directions:
                    new_pos = (r + dr, c + dc)
                    valid = piece.is_square_free(new_pos)
                    if valid:
                        valid_moves.append((piece, position, new_pos, 0))

    if must_take:
        max_score = 0
        best_move = []
        for move in valid_moves:
            # begin score comparison
            score = 0
            if isinstance(move, list):
                for m in move:
                    score += m[-1]
            else:
                score = move[-1]

            if score > max_score:
                best_move = [move]
            elif score == max_score:
                best_move += move
    else:
        best_move = valid_moves
    
    chosen = random.choice(best_move)

    # all doubles give lists
    if isinstance(chosen, list):
        chosen_piece = chosen[0][0]
        for m in chosen:
            chosen_piece.move_double(position=m[1], new_position=m[2])
            # TODO: update board for each move
    else:
        chosen_piece = chosen[0]
        chosen_piece_pos = chosen[1]
        chosen_move = chosen[2]
        chosen_piece.move_single(chosen_piece_pos, chosen_move)

    return


def game():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Draughts Frontend")

    selected_piece = None
    selected_pos = None
    allowed_pieces = None

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
                new_pos = (row, col)
                # select piece
                if selected_piece is None:

                    my_pieces = [p for p in all_pieces if (p.colour == "white" and p.active)]
                    allowed_pieces = [p for p in my_pieces if p.can_take()]
                    must_take = bool(allowed_pieces)
                    print("Must take: ", must_take)
                    if not must_take:
                        allowed_pieces = my_pieces

                    piece = BOARD.get((row, col))
                    if piece and piece.colour == "white":
                        selected_piece = piece
                        selected_pos = (row, col)

                elif new_pos != selected_pos:
                    print("Must take: ", must_take)
                    success, selected_piece, selected_pos = click_move(selected_piece, selected_pos, new_pos, must_take, allowed_pieces)

                    if selected_piece is None and success == 200:
                        selected_piece = None
                        selected_pos = None
                        draw_board(win)
                        draw_pieces(win)
                        pygame.display.update()
                        # TODO: check win
                        ai_move()
                        # TODO: check win
                    

        draw_board(win)
        draw_pieces(win)
        pygame.display.update()

    pygame.quit()
