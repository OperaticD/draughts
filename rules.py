# Assume white pieces start in the bottom half, and black in the top. 
# Top right corner is (0,0) - (i,j) is row i, column j
# Will assume that white is user and black is computer.

import logging

logger = logging.getLogger(__name__)

BOARD = {(r, c): None for r in range(8) for c in range(8)}

def setup_board():
    black_pieces = [BlackPiece() for _ in range(12)]
    black_start_positions = [
        (0,1), (0,3), (0,5), (0,7), (1,0), (1,2), (1,4), (1,6), (2,1), (2,3), (2,5), (2,7)
        ]
    white_pieces = [WhitePiece() for _ in range(12)]
    white_start_positions = [
        (7,0), (7,2), (7,4), (7,6), (6,1), (6,3), (6,5), (6,7), (5,0), (5,2), (5,4), (5,6)
        ]

    for piece, pos in zip(black_pieces, black_start_positions):
        BOARD[pos] = piece
    
    for piece, pos in zip(white_pieces, white_start_positions):
        BOARD[pos] = piece


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

    def can_move_single(self, new_position: tuple[int, int]) -> bool:
        # check if piece can move diagonally right or left
        if not self.check_valid_position(new_position):
            return False

        if BOARD[new_position]:
            logger.error("Square is occupied")
            return False

        return True

    
class BlackPiece(Piece):
    colour = "black"
    # store position?

    def move_right(self, position: tuple[int, int]) -> tuple[str, int]:
        new_position = (position[0] + 1, position[1] + 1)
        if self.can_move_single(new_position):
            # if valid, trigger board move
            BOARD[position] = None
            BOARD[new_position] = self
        return f"Black moved {'king' if self.king_status else 'piece'} to {new_position}.", 200


    def move_left(self, position: tuple[int, int]) -> tuple[str, int]:
        new_position = (position[0] + 1, position[1] - 1)
        if self.can_move_single(new_position):
            # if valid, trigger board move
            BOARD[position] = None
            BOARD[new_position] = self
        return f"Black moved {'king' if self.king_status else 'piece'} to {new_position}.", 200


    def can_move_double_right(self):
        # check valid new position
        # check +(1,1) is occupied by white,
        # check one of following is true
            # +(3,3) is empty, or
            # +(3,3) is occupied by black, or
            # +(3,3) is edge of board, or
            # +(3,3) and +(4,4) are occupied
            # *** OR call can_move_quadruple. If this is true, then return false ***

        pass

    def can_move_quadruple_right(self):
        pass
    
    def can_move_sextuple_right(self):
        pass


class WhitePiece(Piece):
    colour = "white"

    def move_right(self, position: tuple[int, int]) -> tuple[str, int]:
        new_position = (position[0] - 1, position[1] + 1)
        if self.can_move_single(new_position):
            # if valid, trigger board move
            BOARD[position] = None
            BOARD[new_position] = self
        return f"White moved {'king' if self.king_status else 'piece'} to {new_position}.", 200


    def move_left(self, position: tuple[int, int]) -> tuple[str, int]:
        new_position = (position[0] - 1, position[1] - 1)
        if self.can_move_single(new_position):
            # if valid, trigger board move
            BOARD[position] = None
            BOARD[new_position] = self
        return f"White moved {'king' if self.king_status else 'piece'} to {new_position}.", 200






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
