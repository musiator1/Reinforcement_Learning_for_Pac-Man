import pygame
import math

from pygame.locals import *

from global_variables import TILE_LENGTH
from global_variables import GAME_SPEED
from global_variables import Direction

class Pacman():
    def __init__(self, imgs, start_x, start_y):
        self.imgs = imgs
        self.actual_image = imgs[Direction.RIGHT][2]
        self.position = self.actual_image.get_rect()
        self.position.move_ip(start_x, start_y)
        self.direction = Direction.NULL
        self.desired_direction = Direction.NULL
        self.counter = 2
        self.score = 0
        
    def move(self, game_map):
        self._set_direction(game_map)
        remained_movement = GAME_SPEED
        new_position = self.position.copy()
        while remained_movement > 0:
            self.counter += 1
            if self.direction != Direction.NULL:
                self.actual_image = self.imgs[self.direction][int(self.counter % 45 / 15)]
                 
            new_position.move_ip(self.direction.value)     

            if new_position.x <= 0 and new_position.y == 14 * TILE_LENGTH:                
                new_position.x = 26.9 * TILE_LENGTH
                
            if new_position.x >= 27 * TILE_LENGTH and new_position.y == 14 * TILE_LENGTH: 
                new_position.x = 0
            
            if self._detect_tile(game_map, new_position) != "wall":
                self.position = new_position.copy()
            else:
                new_position = self.position.copy()
            self._set_direction(game_map)
            
            remained_movement -= 1
        
        return self.score
            
    
    def _detect_tile(self, game_map, position):
        tile_x = int(position.x / TILE_LENGTH)
        tile_y = int(position.y / TILE_LENGTH)
        
        if self.direction == Direction.RIGHT:
            tile_x = math.ceil(position.x / TILE_LENGTH)
        if self.direction == Direction.DOWN or self.direction == Direction.NULL:
            tile_y = math.ceil(position.y / TILE_LENGTH)
            
        tile_type = game_map[tile_y][tile_x]
        
        if tile_type == '0': #or tile_type == '4':
            return "wall" 
        elif tile_type == '1':
            game_map[tile_y][tile_x] = '3'
            self.score += 1
            return 'food'
        elif tile_type == '2':
            game_map[tile_y][tile_x] = '3'
            return 'super_food'
        elif tile_type == '3':
            return 'empty'
    
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
            if self.desired_direction == Direction.UP and self._detect_tile(game_map, self.position.move(0, -TILE_LENGTH)) != "wall":
                self.direction = Direction.UP
            elif self.desired_direction == Direction.DOWN and self._detect_tile(game_map, self.position.move(0, TILE_LENGTH)) != "wall":
                self.direction = Direction.DOWN
            elif self.desired_direction == Direction.LEFT and self._detect_tile(game_map, self.position.move(-TILE_LENGTH, 0)) != "wall":
                self.direction = Direction.LEFT
            elif self.desired_direction == Direction.RIGHT and self._detect_tile(game_map, self.position.move(TILE_LENGTH, 0)) != "wall":
                self.direction = Direction.RIGHT