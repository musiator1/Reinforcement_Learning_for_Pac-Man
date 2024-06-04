from enum import Enum
import numpy as np

SCREEN_WIDTH = 616
TILE_LENGTH = SCREEN_WIDTH / 28
GAME_SPEED = 5

class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    NULL = (0, 0)
    
    def get_opposite_direction(direction):
        if direction == Direction.UP:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.UP
        elif direction == Direction.LEFT:
            return Direction.RIGHT
        elif direction == Direction.RIGHT:
            return Direction.LEFT
        else:
            return Direction.NULL
    
class Mode(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2
    DEAD = 3