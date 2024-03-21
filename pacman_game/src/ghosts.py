import math 
import random

from abc import ABC
from abc import abstractmethod

from global_variables import Direction
from global_variables import Mode
from global_variables import GAME_SPEED
from global_variables import TILE_LENGTH

special_crossings = [[12*TILE_LENGTH, 11*TILE_LENGTH],
                     [15*TILE_LENGTH, 11*TILE_LENGTH],
                     [12*TILE_LENGTH, 23*TILE_LENGTH],
                     [15*TILE_LENGTH, 23*TILE_LENGTH],]

tunnel_x_coordinates = [[0*TILE_LENGTH, 5*TILE_LENGTH],
                      [22*TILE_LENGTH, 27*TILE_LENGTH]]
tunnel_y_coordinate = 14*TILE_LENGTH

class Ghost(ABC):
    def __init__(self, image, start_x, start_y):
        self.image = image
        self.position = image.get_rect()
        self.position.move_ip(start_x, start_y)
        self.direction = Direction.NULL
        self.mode = Mode.CHASE
        self.scatter_mode_target_position = None
    
    def move(self, game_map, pacman_position, packman_direction, red_ghost_position= None):
        remained_movement = GAME_SPEED
        if self._is_in_tunnel():
            remained_movement *= 0.6
        new_position = self.position.copy()
        while remained_movement > 0:               
            new_position.move_ip(self.direction.value)

            if new_position.x <= 0 and new_position.y == 14 * TILE_LENGTH:                
                new_position.x = 26.9 * TILE_LENGTH
                
            if new_position.x >= 27 * TILE_LENGTH and new_position.y == 14 * TILE_LENGTH: 
                new_position.x = 0
            
            if self._detect_tile(game_map, new_position) != "wall":
                self.position = new_position.copy()
            else: 
                new_position = self.position.copy()
                
            if (self.position.x % TILE_LENGTH == 0 and self.position.y % TILE_LENGTH == 0) or self.direction == Direction.NULL:
                self._set_direction(game_map, pacman_position, packman_direction, red_ghost_position)
            
            remained_movement -= 1
         
    def _set_direction(self, game_map, pacman_position, packman_direction, red_ghost_position):
        directions = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]
        for sc in special_crossings:
            if [self.position.x, self.position.y] == sc:
                directions.remove(Direction.UP)
        if self.mode == Mode.CHASE:
            target_position = self._get_target_position(pacman_position, packman_direction, red_ghost_position)
        elif self.mode == Mode.SCATTER:
            target_position = self.scatter_mode_target_position
        elif self.mode == Mode.FRIGHTENED:
            while True:
                random_direction = random.choice(directions)
                if self._is_direction_possible(game_map, random_direction):
                    self.direction = random_direction
                    break
            return
            
        possible_directions = {}
        for direction in directions:
            if self._is_direction_possible(game_map, direction):
                new_position = self.position.move((direction.value[0] * TILE_LENGTH, direction.value[1] * TILE_LENGTH))
                possible_directions[direction] = (target_position[0] - new_position.x) ** 2 + (target_position[1] - new_position.y) ** 2
                    
        if possible_directions:
            self.direction = min(possible_directions, key=lambda x: possible_directions[x])
                
    def _is_direction_possible(self, game_map, direction):
        new_position = self.position.move((direction.value[0] * TILE_LENGTH, direction.value[1] * TILE_LENGTH))
        if self._detect_tile(game_map, new_position) == "wall" or direction == Direction.get_opposite_direction(self.direction):
            return False
        if self._detect_tile(game_map, new_position) == "line" and direction == Direction.DOWN:
            return False
        return True
          
    @abstractmethod    
    def _get_target_position(self, pacman_position, packman_direction, red_ghost_position):
        pass
            
    def _detect_tile(self, game_map, position):
        tile_x = int(position.x / TILE_LENGTH)
        tile_y = int(position.y / TILE_LENGTH)
        
        if self.direction == Direction.RIGHT:
            tile_x = math.ceil(position.x / TILE_LENGTH)
        if self.direction == Direction.DOWN or self.direction == Direction.NULL:
            tile_y = math.ceil(position.y / TILE_LENGTH)
            
        tile_type = game_map[tile_y][tile_x]
        
        if tile_type == '0':
            return "wall"
        if tile_type == '4':
            return "line"
        
    def _is_in_tunnel(self):
        if self.position.y == tunnel_y_coordinate:
            for txc in tunnel_x_coordinates:
                if txc[0] < self.position.x < txc[1]:
                    return True
        return False
        
class Blinky(Ghost):
    def __init__(self, image, start_x, start_y):
        super().__init__(image, start_x, start_y)
        self.scatter_mode_target_position = [TILE_LENGTH * 28, TILE_LENGTH * -2]
        
    def _get_target_position(self, packman_position, packman_direction, red_ghost_position):
        return [packman_position.x, packman_position.y]
    
class Pinky(Ghost):
    def __init__(self, image, start_x, start_y):
        super().__init__(image, start_x, start_y)
        self.scatter_mode_target_position = [TILE_LENGTH * 2, TILE_LENGTH * -2]
        
    def _get_target_position(self, packman_position, packman_direction, red_ghost_position):
        if packman_direction == Direction.UP:
            return [packman_position.x - TILE_LENGTH * 4, packman_position.y - TILE_LENGTH * 4]
        else:
            x = packman_position.x + packman_direction.value[0] * TILE_LENGTH * 4
            y = packman_position.y + packman_direction.value[1] * TILE_LENGTH * 4
            return [x, y]
        
class Inky(Ghost):
    def __init__(self, image, start_x, start_y):
        super().__init__(image, start_x, start_y)
        self.scatter_mode_target_position = [TILE_LENGTH * 28, TILE_LENGTH * 33]
        
    def _get_target_position(self, pacman_position, packman_direction, red_ghost_position):
        if packman_direction == Direction.UP:
            tmp_position = [pacman_position.x - TILE_LENGTH * 2, pacman_position.y - TILE_LENGTH * 2]
        else:
            x = pacman_position.x + packman_direction.value[0] * TILE_LENGTH * 2
            y = pacman_position.y + packman_direction.value[1] * TILE_LENGTH * 2
            tmp_position = [x, y]
        
        vector = [tmp_position[0] - red_ghost_position.x, tmp_position[1] - red_ghost_position.y]
        target_position = [tmp_position[0] + vector[0], tmp_position[1] + vector[1]]
        return target_position
    
class Clyde(Ghost):
    def __init__(self, image, start_x, start_y):
        super().__init__(image, start_x, start_y)
        self.scatter_mode_target_position = [TILE_LENGTH * 0, TILE_LENGTH * 33]
        
    def _get_target_position(self, packman_position, packman_direction, red_ghost_position):
        if math.sqrt((packman_position.x - self.position.x)**2 + (packman_position.y - self.position.y)**2) > TILE_LENGTH * 8:
            return [packman_position.x, packman_position.y]
        else:
            return self.scatter_mode_target_position