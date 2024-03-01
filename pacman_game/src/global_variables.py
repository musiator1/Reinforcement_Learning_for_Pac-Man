from enum import Enum

SCREEN_WIDTH = 560
TILE_LENGTH = SCREEN_WIDTH / 28
GAME_SPEED = 3

class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    NULL = (0, 0)