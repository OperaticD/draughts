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


def click_move(must_take: bool, allowed_pieces: list[object]) -> tuple[int, object]: # TODO check object
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
        # Check if any pieces can be taken

        if must_take and selected_piece not in allowed_pieces:
            logger.error("Must capture a piece.")
            # Reset and continue
            selected_piece = None
            selected_pos = None
        
        if selected_piece in allowed_pieces:
            new_pos = (row, col)

            # calculate movement
            dr = new_pos[0] - selected_pos[0]
            dc = new_pos[1] - selected_pos[1]

            if abs(dr) == 1 and abs(dc) == 1 and must_take == False:
                success = selected_piece.move_single(selected_pos, new_pos)
                if success == 200:
                    if current_turn == "white":
                        current_turn = "black"
                    else:
                        current_turn = "white"
                    return 200, None

            # if double move
            elif abs(dr) == 2 and abs(dc) == 2: # if must_take == False, there will be an error when we check valid move

                success = selected_piece.move_double(selected_pos, new_pos)
                if success == 200:
                # TODO fix double jump
                    if selected_piece.can_take():
                    # The piece has just moved, so its new selected_pos is the old new_pos
                        selected_pos = new_pos
                        return 200, selected_piece

                if current_turn == "white":
                    current_turn = "black"
                else:
                    current_turn = "white"
                return 200, None
            


# TODO add score to can_move_double depending on king 
def ai_move():
    # check score of each can_move_double and track piece, new square, score
    active_black_pieces = [p for p in black_pieces if p.active]
    valid_moves = []
    must_take = False
    for piece in active_black_pieces:
        position = next((k for k, v in BOARD.items() if v == piece), None)
        if position:
            double = piece.check_double(position)
            valid_moves += double
            if double:
                must_take = True

            if not must_take:
                r, c = position
                # # direction pairs for standard movement
                directions = [(1, -1), (1, 1)]
                if piece.king_status:
                    directions += [(-1, -1), (-1, 1)]

                for dr, dc in directions:
                    new_pos = (r + dr, c + dc)
                    valid = piece.can_move(new_pos)
                    if valid:
                        valid_moves += (piece, new_pos, 0)

    if must_take:
        max_score = 0
        best_move = []
        for move in valid_moves:
            # begin score comparison
            if move[2] > max_score:
                best_move = [move]
            elif move[2] == max_score:
                best_move += move
    else:
        best_move = valid_moves
    
    chosen = random.choice(best_move)

    chosen_piece = chosen[0]
    chosen_move = chosen[1]
    if chosen[2] > 0:
        # unpack move
        for move in chosen_move:
            chosen_piece.move_double(move)
    else:
        chosen_piece.move(chosen_move)
    
    # randomly pick from valid_moves


    # thought - use function to extend valid_moves
    # while it's possible to make double move again, call function (within function) 
    # later: can save time by tracking squares covered

    # use .get() for list of highest scores
    # if length greater than 1, pick at random
    # if length = 0, then try can_move and make list of possibilities
    # random single move

    # later add in if statement for king_status


    return


def game():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Draughts Frontend")

    selected_piece = None
    selected_pos = None
    allowed_pieces = []
    current_turn = "white"

    running = True
    while running:

        if allowed_pieces:
            must_take = True
        else:
            my_pieces = [p for p in all_pieces if (p.colour == current_turn and p.active)]
            allowed_pieces = [p for p in my_pieces if p.can_take()]
            if allowed_pieces:
                must_take = True
            else:
                allowed_pieces = my_pieces
                must_take = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                next_turn, must_move_piece = click_move(must_take, allowed_pieces)

                if not must_move_piece and next_turn == 200:
                    ai_move()
                    # else:
                    #     logger.error(f"piece in {selected_pos} can't be moved ")

                    # Reset selection
                
                if must_move_piece:
                    allowed_pieces = [must_move_piece]
                else:
                    allowed_pieces = []

                selected_piece = None
                selected_pos = None
                # must_take = False
                    

        draw_board(win)
        draw_pieces(win)
        pygame.display.update()

    pygame.quit()
