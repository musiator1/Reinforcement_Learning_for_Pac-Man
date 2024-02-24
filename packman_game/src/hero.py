import pygame
import math

from pygame.locals import *

from global_variables import TILE_LENGTH
from global_variables import GAME_SPEED
from global_variables import Direction

class Packman:
    def __init__(self, image, start_x, start_y):
        self.image = image
        self.position = image.get_rect()
        self.position.move_ip(start_x, start_y)
        self.direction = Direction.NULL
        self.desired_direction = Direction.NULL
        
    def move(self, game_map):
        self._set_direction(game_map)
        remained_movement = GAME_SPEED
        new_position = self.position.copy()
        while remained_movement > 0:    
            new_position.move_ip(self.direction.value)        

            if new_position.x <= 0 and new_position.y == 14 * TILE_LENGTH:
                new_position.x = 26.9 * TILE_LENGTH
                
            if new_position.x >= 27 * TILE_LENGTH and new_position.y == 14 * TILE_LENGTH:
                new_position.x = 0
            
            if self._can_move(game_map, new_position):
                self.position = new_position.copy()
            else: 
                new_position = self.position.copy()
                
            self._set_direction(game_map)
 
            print(self.position.x, self.position.y)
            remained_movement -= 1
            
    def _set_direction(self, game_map):
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.desired_direction = Direction.UP
        elif keys[K_DOWN]:
            self.desired_direction = Direction.DOWN
        elif keys[K_LEFT]:
            self.desired_direction = Direction.LEFT
        elif keys[K_RIGHT]:
            self.desired_direction = Direction.RIGHT
        
        if (self.position.x % TILE_LENGTH == 0 and self.position.y % TILE_LENGTH == 0) or self.direction == Direction.NULL:
            if self.desired_direction == Direction.UP and self._can_move(game_map, self.position.move(0, -TILE_LENGTH)):
                self.direction = Direction.UP
            elif self.desired_direction == Direction.DOWN and self._can_move(game_map, self.position.move(0, TILE_LENGTH)):
                self.direction = Direction.DOWN
            elif self.desired_direction == Direction.LEFT and self._can_move(game_map, self.position.move(-TILE_LENGTH, 0)):
                self.direction = Direction.LEFT
            elif self.desired_direction == Direction.RIGHT and self._can_move(game_map, self.position.move(TILE_LENGTH, 0)):
                self.direction = Direction.RIGHT
    
    def _can_move(self, game_map, new_position):
        tile_x = int(new_position.x / TILE_LENGTH)
        tile_y = int(new_position.y / TILE_LENGTH)
        
        if self.direction == Direction.RIGHT:
            tile_x = math.ceil(new_position.x / TILE_LENGTH)
        if self.direction == Direction.DOWN:
            tile_y = math.ceil(new_position.y / TILE_LENGTH)
        
        if game_map[tile_y][tile_x] == '0' or game_map[tile_y][tile_x] == '4':
            return False 
        
        return True