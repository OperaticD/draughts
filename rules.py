# Assume white pieces start in the bottom half, and black in the top. 
# Top right corner is (0,0) - (i,j) is row i, column j
# Assume that white is user and black is computer.

import logging

logger = logging.getLogger(__name__)


def captured_position(position: tuple[int, int], new_position: tuple[int, int]) -> tuple[int, int]:
    dr = new_position[0] - position[0]
    dc = new_position[1] - position[1]
    captured_pos_r = position[0] + dr // 2
    captured_pos_c = position[1] + dc // 2
    return (captured_pos_r, captured_pos_c)


class Piece:
    king_status: bool = False
    active: bool = True

    def check_valid_position(self, position: tuple[int, int]) -> bool:
        # square must be within the board and empty
        if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
            logger.error("Invalid position")
            return False
        else:
            return True

    def is_square_free(self, new_position: tuple[int, int]) -> bool:
        # check if piece can move diagonally right or left
        if not self.check_valid_position(new_position):
            return False

        if BOARD[new_position]:
            logger.error("Square is occupied")
            return False

        return True
    
    def can_move_double(self, new_position: tuple[int, int], captured_position: tuple[int, int]) -> tuple[bool, int]:
        if not self.is_square_free(new_position):
            return False, 0
        
        captured_piece = BOARD[captured_position]
        if captured_piece:
            if captured_piece.colour != self.colour:
                score = 2 if captured_piece.king_status else 1
                return True, score
            elif captured_piece.colour == self.colour:
                logger.error("Cannot take your own piece.")
                return False, 0
        else:
            return False, 0


class BlackPiece(Piece):
    colour = "black"
    # TODO: Check how double moves continue if can_move_double again.

    def move(self, position: tuple[int, int], new_position: tuple[int,int]) -> tuple[str, int]:
        BOARD[position] = None
        BOARD[new_position] = self
        logger.info(f"Black moved {'king' if self.king_status else 'piece'} at {position} to {new_position}.")
        if new_position[0] == 7:
            self.king_status = True

    def move_single(self, position: tuple[int, int], new_position: tuple[int,int]) -> int:
        dr = new_position[0] - position[0]
        # allowed if moving forward, or piece is a king
        can_move = self.is_square_free(new_position) and (dr == 1 or self.king_status)
        if can_move:
            self.move(position, new_position)

        return 200
    
    def move_double(self, new_position: tuple[int, int]) -> int:
        # TODO: figure out position from self
        position = next((k for k, v in BOARD.items() if v == self), None)
        dr = new_position[0] - position[0]
        captured_pos = captured_position(position, new_position)
        can_move = self.can_move_double(new_position, captured_pos) and (dr == 2 or self.king_status)

        if can_move:
            captured_piece = BOARD[captured_pos]
            captured_piece.active = False
            BOARD[captured_pos] = None
            self.move(position, new_position)

        return 200

    def can_take(self):
        # find current position
        position = next((k for k, v in BOARD.items() if v == self), None)
        if position:
            r, c = position
            # direction pairs for standard movement
            directions = [(2, -2), (2, 2)]
            if self.king_status:
                directions += [(-2, -2), (-2, 2)]

            for dr, dc in directions:
                new_pos = (r + dr, c + dc)
                captured = captured_position(position, new_pos)

                if self.can_move_double(new_pos, captured)[0]:
                    return True

        return False
    
    def check_double(self, position: tuple, moves: list = []) -> list:
        r, c = position
        # direction pairs for standard movement
        directions = [(2, -2), (2, 2)]
        if self.king_status:
            directions += [(-2, -2), (-2, 2)]

        for dr, dc in directions:
            new_pos = (r + dr, c + dc)
            captured = captured_position(position, new_pos)
            valid, score = self.can_move_double(new_pos, captured)
            if valid:
                moves.append((self, new_pos, score))
                # return to start with new position to see if piece can make another double move
                self.check_double(new_pos, moves)
        
        return moves


class WhitePiece(Piece):
    colour = "white"

    def move(self, position: tuple[int, int], new_position: tuple[int,int]) -> tuple[str, int]:
        BOARD[position] = None
        BOARD[new_position] = self
        logger.info(f"White moved {'king' if self.king_status else 'piece'} at {position} to {new_position}.")
        if new_position[0] == 0:
            self.king_status = True

    def move_single(self, position: tuple[int, int], new_position: tuple[int,int]) -> int:
        dr = new_position[0] - position[0]
        # allowed if moving forward, or piece is a king
        can_move = self.is_square_free(new_position) and (dr == -1 or self.king_status)
        if can_move:
            self.move(position, new_position)

        return 200

    def move_double(self, new_position: tuple[int, int], select_position: tuple[int,int] = None) -> int:
        position = select_position or next((k for k, v in BOARD.items() if v == self), None)
        dr = new_position[0] - position[0]
        captured_pos = captured_position(position, new_position)
        can_move = self.can_move_double(new_position, captured_pos)[0] and (dr == -2 or self.king_status)

        if can_move:
            captured_piece = BOARD[captured_pos]
            captured_piece.active = False
            BOARD[captured_pos] = None
            self.move(position, new_position)

        return 200
    
    def can_take(self):
        # find current position
        position = next((k for k, v in BOARD.items() if v == self), None)
        if position:
            r, c = position
            # direction pairs for standard movement
            directions = [(-2, -2), (-2, 2)]
            if self.king_status:
                directions += [(2, -2), (2, 2)]

            for dr, dc in directions:
                new_pos = (r + dr, c + dc)
                captured = captured_position(position, new_pos)

                if self.can_move_double(new_pos, captured)[0]:
                    return True

        return False


BOARD = {(r, c): None for r in range(8) for c in range(8)}
black_pieces = [BlackPiece() for _ in range(12)]
white_pieces = [WhitePiece() for _ in range(12)]
all_pieces = black_pieces + white_pieces


def setup_board():
    black_start_positions = [
        (0,1), (0,3), (0,5), (0,7), (1,0), (1,2), (1,4), (1,6), (2,1), (2,3), (2,5), (2,7)
        ]
    white_start_positions = [
        (7,0), (7,2), (7,4), (7,6), (6,1), (6,3), (6,5), (6,7), (5,0), (5,2), (5,4), (5,6)
        ]

    for piece, pos in zip(black_pieces, black_start_positions):
        BOARD[pos] = piece
    
    for piece, pos in zip(white_pieces, white_start_positions):
        BOARD[pos] = piece


# board contains layout of all pieces - grid of piece objects
    
# Before each move, check which pieces can be moved
    # Which pieces can take from opposite.
    # If none, then which piece can move single.
# Check if selected piece 
    
# SINGLE MOVES
# Player tries to move piece single space diagonally
# Call validity function for piece associated with move
# Check if it is possible to take with any of the pieces
# If True, change the position on the board of that piece by setting new_position and emptying old_position.
# (Error if False)
    
# KING MOVE is similar.
    
# DOUBLE MOVES - old idea
# Player tries to move piece double, quadruple, sextuple.
# For each check - see if opposite piece is in middle and there is a valid empty space.
# For double move - check validity of double and not quadruple.
# For quadruple move - check validity of double and quadruple and not sextuple
# For sextuple move - check validity of double and single and sextuple

# DOUBLES
# 1) see if opposite piece is in middle and there is a valid empty space.
# 2) move piece
# 3a) If possible to take another piece (left or right), move again
# 3b) If possible to take multiple pieces, wait for player


# AFTER EACH MOVE
# For black pieces, if position[1] == 8, update king status. Opposite for white.
# Check if opposite side has any pieces left
# Check if opposite side is able to make any moves

# Later
# Don't let player move while computer is calculating move
