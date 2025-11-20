# draughts

Using Python 3.12 and pygame 2.6.1

Work In Progress!
- Currently can make diagonal moves.
- Next: Code clean up and double moves logic.

<br><br>

Setup:
- Eight by eight board, with chequered squares. Dark square on bottom left corner.
- On the nearest twelve dark squares from each of the two opposite ends, twelve checkers are placed: white at one end, black at the other.

Player wins if 
A) all of the opponent's pieces have been removed from the board.
or
B) the opponent cannot make any legal moves.


Gameplay:
- The opening player may be decided by a coin toss.
- Each player moves a piece in turn:
    - one square forward diagonally to a vacant square;
    - numerous squares forward to capture opponent pieces:
        - a piece may move two squares diagonally forward to a vacant square, traversing a square occupied by an opponent piece, and capturing it;
        - if it is possible to capture any further pieces with the same piece, it must be done again in the same turn;
        - a move to capture a piece must be executed if possible;

- Any piece that advances to the furthest row whence it started has a piece of the same colour stacked onto it, forming a double piece king.

- A king may move one square diagonally forward or backward, or two squares to capture an opponent piece according to the same rules as a single piece.
