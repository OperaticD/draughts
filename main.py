# entry point for application

from rules import BlackPiece, WhitePiece, setup_board
from frontend import game

def main():
    setup_board()
    game() # start the Pygame frontend


if __name__ == "__main__":
    main()        # initialize backend + BOARD
