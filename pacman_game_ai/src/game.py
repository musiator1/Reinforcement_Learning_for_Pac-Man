import pygame
import numpy as np
import math

from hero import Pacman
from ghosts import Red_Ghost

from global_variables import TILE_LENGTH
from global_variables import SCREEN_WIDTH
from global_variables import GAME_SPEED
from global_variables import Direction
from global_variables import Mode

from map import load_map
from map import draw_map

from image_loader import load_ghosts_hero_imgs
class Pacman_Game_AI:
    def __init__(self):
        #init screen
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, TILE_LENGTH * 31 + 50))  
        pygame.display.set_caption("Pacman") 
        self.clock = pygame.time.Clock()
        
        #init help variables
        self.score = 0
        self.ghost_counter = 0
        
        #load images
        self.red_ghost_img, self.pink_ghost_img, self.cyan_ghost_img, self.orange_ghost_img, self.pcm_imgs = load_ghosts_hero_imgs()
        pygame.display.set_icon(self.pcm_imgs[Direction.RIGHT][2])
        
        #load map
        self.game_map = load_map(r"pacman_game_ai/resources/initial_map.txt")
        draw_map(self.game_map, self.screen)
        
        #display initial score
        self.font = pygame.font.SysFont("Consolas" , 36)
        self.text = self.font.render("Score: 0", True, "white")
        
        #init hero and ghosts
        self.pacman = Pacman(self.pcm_imgs)
        self.red_ghost = Red_Ghost(self.red_ghost_img)
        self.ghosts = [self.red_ghost]
        self.reset_game()
        
        #define initial state
        self.state = self.get_state()
    
    def play_step(self, action):
        #check if any ghost is in frightened mode
        if not any(ghost.mode == Mode.FRIGHTENED for ghost in self.ghosts):
            self.ghost_counter += GAME_SPEED
        
        #actualize state of the game and get information about collision
        old_score = self.score   
        self.score = self.pacman.move(self.game_map, action)     
        delta_score = self.score - old_score
        reward = -0.3 #penalty for each step
        
        if delta_score == 1:
            reward += 10 #reward for collecting food
        elif delta_score == 10:
            reward += 100 #reward for collecting super food
            for ghost in self.ghosts:
                if ghost.mode != Mode.DEAD:
                    ghost.be_frightened(600)
        
        collision_code = 0        
        collision_code |= self.red_ghost.move(self.game_map, self.pacman.position, self.pacman.direction, self.ghost_counter)
            
        self.state = self.get_state()
        
        #draw actual state of the game
        self.screen.fill("black")
        draw_map(self.game_map, self.screen)
        self.screen.blit(self.pacman.actual_image, self.pacman.position)
        self.screen.blit(self.red_ghost.image, self.red_ghost.position)
        
        #display actual score
        self.text = self.font.render(f"Score: {self.score}", True, "white")
        self.screen.blit(self.text, (0, 31 * TILE_LENGTH))
        
        #init return values
        game_over = False
        
        #check collision with ghost
        if collision_code == 1:
            game_over = True
            reward -= 20
            self.reset_game()
            self.game_map = load_map(r"pacman_game_ai/resources/initial_map.txt")
        
        #check if hero won    
        if self.score == 188:
            game_over = True
            reward += 50
            self.reset_game()
            self.game_map = load_map(r"pacman_game_ai/resources/initial_map.txt")

        pygame.display.flip()
        return reward, game_over, self.score
        
    def reset_game(self):
        self.pacman.position.x = TILE_LENGTH * 13.5
        self.pacman.position.y = TILE_LENGTH * 23
        self.pacman.direction = Direction.NULL
        self.pacman.desired_direction = Direction.NULL
        self.pacman.score = 0
        self.ghost_counter = 0
        
        for ghost in self.ghosts:
            ghost.direction = Direction.NULL
            ghost.change_mode_values = [900, 3470, 4370, 6940, 7583, 10153, 10796]
            if ghost.mode == Mode.FRIGHTENED or ghost.mode == Mode.DEAD:
                ghost.frightened_counter = 0
                ghost.image = ghost.normal_image
        
        self.red_ghost.position.x = TILE_LENGTH * 13
        self.red_ghost.position.y = TILE_LENGTH * 11
        
        
    def get_state(self):
        state_grid = np.zeros((17))
        # najblizsze jedzenie z lewej, góry, prawej, dołu - state_grid[0:3]
        self._calculate_nearest_food(state_grid)  
        # wróg z lewej, góry, prawej, dołu (4 bool)  oraz wróg bliżej niż 4 kratki - state_grid[4:7]
        self._ghost_position(state_grid)
        # kierunek pacmana (lewo, góra, prawo, dół) (4 bool) - state_grid[8:11]
        if self.pacman.direction == Direction.LEFT:
            state_grid[8] = 1
        elif self.pacman.direction == Direction.UP:
            state_grid[9] = 1
        elif self.pacman.direction == Direction.RIGHT:
            state_grid[10] = 1
        elif self.pacman.direction == Direction.DOWN:
            state_grid[11] = 1
        # kierunek ducha (lewo, góra, prawo, dół) (4 bool) - state_grid[12:15]
        if self.red_ghost.direction == Direction.LEFT:
            state_grid[12] = 1
        elif self.red_ghost.direction == Direction.UP:
            state_grid[13] = 1
        elif self.red_ghost.direction == Direction.RIGHT:
            state_grid[14] = 1
        elif self.red_ghost.direction == Direction.DOWN:
            state_grid[15] = 1
        # czy przed duchem jest ściana
        if self.pacman._detect_tile(self.game_map, self.pacman.position.move(self.pacman.direction.value[0], self.pacman.direction.value[1])) == "wall":
            state_grid[16] = 1
            
        return state_grid

    def _calculate_nearest_food(self, state_grid):
        nearest_food_pos = [0, 0]
        pacman_pos = [self.pacman.position.x, self.pacman.position.y]
        min_distance = 100_000_000
        for i in range(0, 30):
            for j in range (0, 28):
                if self.game_map[i][j] == '1' or self.game_map[i][j] == '2':
                    food_pos = [j * TILE_LENGTH, i * TILE_LENGTH]
                    distance = (pacman_pos[0] - food_pos[0])**2 + (pacman_pos[1] - food_pos[1])**2
                    if distance < min_distance:
                        min_distance = distance
                        nearest_food_pos = food_pos
                        
        if nearest_food_pos[0] > pacman_pos[0]:
            state_grid[2] = 1
        elif nearest_food_pos[0] < pacman_pos [0]:
            state_grid[0] = 1
            
        if nearest_food_pos[1] > pacman_pos[1]:
            state_grid[3] = 1
        elif nearest_food_pos[1] < pacman_pos [1]:
            state_grid[1] = 1
            
    def _is_direction_possible(self, game_map, direction, position):
        new_position = position.move((direction.value[0] * TILE_LENGTH, direction.value[1] * TILE_LENGTH))
        tile_type = self.pacman._detect_tile(game_map, new_position)
        if tile_type == 'wall' or tile_type == 'line':
            return False
        return True

    def _ghost_position(self, state_grid):
        pacman_pos = [self.pacman.position.x, self.pacman.position.y]
        ghost_pos = [self.red_ghost.position.x, self.red_ghost.position.y]
        is_close = False
        if math.sqrt((pacman_pos[0] - ghost_pos[0])**2 + (pacman_pos[1] - ghost_pos[1])**2) < 4*TILE_LENGTH and self.red_ghost.mode != Mode.FRIGHTENED:
            is_close = True
        
        if is_close:
            if ghost_pos[0] > pacman_pos[0]:
                state_grid[6] = 1
            elif ghost_pos[0] < pacman_pos[0]:
                state_grid[4] = 1
                
            if ghost_pos[1] > pacman_pos[1]:
                state_grid[7] = 1
            elif ghost_pos[1] < pacman_pos[1]:
                state_grid[5] = 1