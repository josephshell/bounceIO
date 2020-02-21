import pygame

from src.Logger import debug
from src.BounceIo import bounce_io_debug
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
SIZE = (800, 600)


def main():
    bounce_io_debug(pygame, WHITE, RED, BLUE, SIZE, 10, 50, debug)


if __name__ == '__main__':
    main()
