import math 
import random
import pygame

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
    def __init__(self, image):
        self.image = image
        self.position = image.get_rect()
        self.direction = Direction.NULL
        self.mode = Mode.SCATTER
        self.scatter_mode_target_position = None
        self.frightened_image = pygame.image.load(r"pacman_game/resources/frightened.png")
        self.frightened_image = pygame.transform.smoothscale(self.frightened_image, (TILE_LENGTH, TILE_LENGTH))
        self.frightened_counter = 0
        self.normal_image = image
        self.change_mode_values = [900, 3470, 4370, 6940, 7583, 10153, 10796]
        self.is_dead = False
    
    def move(self, game_map, pacman_position, packman_direction, counter, red_ghost_position= None):
        #helping operation in changing direction while switching modes
        counter -= GAME_SPEED
        ret_value = 0
        #setting speed
        remained_movement = GAME_SPEED
        if self._is_in_tunnel():
            remained_movement *= 0.6
        if self.mode == Mode.FRIGHTENED:
            remained_movement *= 0.5
        if self.mode == Mode.DEAD:
            remained_movement *= 0.7
        
        #moving loop
        new_position = self.position.copy()
        while remained_movement > 0:
            counter += 1
            self._set_mode(counter)          
            new_position.move_ip(self.direction.value)

            #moving in portal
            if new_position.x <= 0 and new_position.y == 14 * TILE_LENGTH:                
                new_position.x = 26.9 * TILE_LENGTH
            if new_position.x >= 27 * TILE_LENGTH and new_position.y == 14 * TILE_LENGTH: 
                new_position.x = 0
            
            #rest of the movement
            if self._detect_tile(game_map, new_position) != "wall":
                self.position = new_position.copy()
            else: 
                new_position = self.position.copy()
                
            if self.position.x == TILE_LENGTH * 13.5 and self.position.y == TILE_LENGTH * 14:
                self.is_dead = False
                self.image = self.normal_image
                
            #checking collision with hero
            in_range_x = self.position.x - 5 < pacman_position.x < self.position.x + 5
            in_range_y = self.position.y - 5 < pacman_position.y < self.position.y + 5
            if in_range_x and in_range_y:
                if self.mode != Mode.FRIGHTENED and self.mode != Mode.DEAD:
                    ret_value = 1 #ending game collision
                elif self.mode == Mode.FRIGHTENED:
                    self.be_dead()
                
            if (self.position.x % TILE_LENGTH == 0 and self.position.y % TILE_LENGTH == 0) or self.direction == Direction.NULL:
                self._set_direction(game_map, pacman_position, packman_direction, red_ghost_position)     
            remained_movement -= 1
            
        return ret_value
            
    def be_frightened(self, time):
        if self.direction != Direction.NULL:
            self.frightened_counter = time
            self.direction = Direction.get_opposite_direction(self.direction)
            self.image = self.frightened_image
            
    def be_dead(self):
        self.mode = Mode.DEAD
        dead_image = pygame.image.load(r"pacman_game/resources/eyes.png")
        self.image = pygame.transform.smoothscale(dead_image, (TILE_LENGTH, TILE_LENGTH))
        self.frightened_counter = 0
        self.is_dead = True
        pass

    def _set_mode(self, counter):
        if self.frightened_counter > 0:
            self.mode = Mode.FRIGHTENED
            self.frightened_counter -= 1
        elif self.is_dead:
            self.mode = Mode.DEAD
        else:
            if self.image != self.normal_image:
                self.image = self.normal_image
            if counter in self.change_mode_values:
                self.change_mode_values.remove(counter)
                self.direction = Direction.get_opposite_direction(self.direction)
            
            if counter <= 900:
                self.mode = Mode.SCATTER
            elif 900 < counter <= 3470:
                self.mode = Mode.CHASE
            elif 3470 < counter <= 4370:
                self.mode = Mode.SCATTER
            elif 4370 < counter <= 6940:
                self.mode = Mode.CHASE
            elif 6940 < counter <= 7583:
                self.mode = Mode.SCATTER
            elif 7583 < counter <= 10153:
                self.mode = Mode.CHASE
            elif 10153 < counter <= 10796:
                self.mode = Mode.SCATTER
            else:
                self.mode = Mode.CHASE
         
    def _set_direction(self, game_map, pacman_position, packman_direction, red_ghost_position):
        directions = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]
        for sc in special_crossings:
            if [self.position.x, self.position.y] == sc:
                directions.remove(Direction.UP)
        if self.mode == Mode.CHASE:
            target_position = self._get_target_position(pacman_position, packman_direction, red_ghost_position)
        elif self.mode == Mode.SCATTER:
            target_position = self.scatter_mode_target_position
        elif self.mode == Mode.DEAD:
            target_position = TILE_LENGTH * 13.5, TILE_LENGTH * 14
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
        if self._detect_tile(game_map, new_position) == "line" and direction == Direction.DOWN and self.mode != Mode.DEAD:
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
        
class Red_Ghost(Ghost):
    def __init__(self, image):
        super().__init__(image)
        self.scatter_mode_target_position = [TILE_LENGTH * 28, TILE_LENGTH * -2]
        
    def _get_target_position(self, packman_position, packman_direction, red_ghost_position):
        return [packman_position.x, packman_position.y]
    
class Pink_Ghost(Ghost):
    def __init__(self, image):
        super().__init__(image)
        self.scatter_mode_target_position = [TILE_LENGTH * 2, TILE_LENGTH * -2]
        
    def _get_target_position(self, packman_position, packman_direction, red_ghost_position):
        if packman_direction == Direction.UP:
            return [packman_position.x - TILE_LENGTH * 4, packman_position.y - TILE_LENGTH * 4]
        else:
            x = packman_position.x + packman_direction.value[0] * TILE_LENGTH * 4
            y = packman_position.y + packman_direction.value[1] * TILE_LENGTH * 4
            return [x, y]
        
class Cyan_Ghost(Ghost):
    def __init__(self, image):
        super().__init__(image)
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
    
class Orange_Ghost(Ghost):
    def __init__(self, image):
        super().__init__(image)
        self.scatter_mode_target_position = [TILE_LENGTH * 0, TILE_LENGTH * 33]
        
    def _get_target_position(self, packman_position, packman_direction, red_ghost_position):
        if math.sqrt((packman_position.x - self.position.x)**2 + (packman_position.y - self.position.y)**2) > TILE_LENGTH * 8:
            return [packman_position.x, packman_position.y]
        else:
            return self.scatter_mode_target_position