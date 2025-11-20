# entry point for application

from rules import BlackPiece, WhitePiece, setup_board
from frontend import pygame_loop

def main():
    setup_board()

    # Let white move first


if __name__ == "__main__":
    main()        # initialize backend + BOARD
    pygame_loop() # start the Pygame frontend
