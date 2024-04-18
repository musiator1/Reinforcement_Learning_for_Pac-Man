import pygame
import numpy as np

from hero import Pacman
from ghosts import Red_Ghost, Pink_Ghost, Cyan_Ghost, Orange_Ghost

from global_variables import TILE_LENGTH
from global_variables import SCREEN_WIDTH
from global_variables import GAME_SPEED
from global_variables import Direction
from global_variables import Mode

from map import load_map
from map import draw_map

from user_interfaces import show_start_menu
from user_interfaces import show_end_screen

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
        self.game_map = load_map(r"pacman_game/resources/initial_map.txt")
        draw_map(self.game_map, self.screen)
        
        #display initial score
        self.font = pygame.font.SysFont("Consolas" , 36)
        self.text = self.font.render("Score: 0", True, "white")
        
        #init hero and ghosts
        self.pacman = Pacman(self.pcm_imgs)
        self.red_ghost = Red_Ghost(self.red_ghost_img)
        self.pink_ghost = Pink_Ghost(self.pink_ghost_img)
        self.cyan_ghost = Cyan_Ghost(self.cyan_ghost_img)
        self.orange_ghost = Orange_Ghost(self.orange_ghost_img)
        self.ghosts = [self.red_ghost, self.pink_ghost, self.cyan_ghost, self.orange_ghost]
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
        if delta_score == 10:
            for ghost in self.ghosts:
                if ghost.mode != Mode.DEAD:
                    ghost.be_frightened(600)
        
        collision_code = 0        
        collision_code |= self.red_ghost.move(self.game_map, self.pacman.position, self.pacman.direction, self.ghost_counter)
        collision_code |= self.pink_ghost.move(self.game_map, self.pacman.position, self.pacman.direction, self.ghost_counter)
        if self.score >= 30:
            collision_code |= self.cyan_ghost.move(self.game_map, self.pacman.position, self.pacman.direction, self.ghost_counter, self.red_ghost.position)
        if self.score >= 80:
            collision_code |= self.orange_ghost.move(self.game_map, self.pacman.position, self.pacman.direction, self.ghost_counter)
            
        self.state = self.get_state()
        
        #draw actual state of the game    
        self.screen.fill("black")
        draw_map(self.game_map, self.screen)
        self.screen.blit(self.pacman.actual_image, self.pacman.position)
        self.screen.blit(self.red_ghost.image, self.red_ghost.position)
        self.screen.blit(self.pink_ghost.image, self.pink_ghost.position)
        self.screen.blit(self.cyan_ghost.image, self.cyan_ghost.position)
        self.screen.blit(self.orange_ghost.image, self.orange_ghost.position)
        
        #display actual score
        self.text = self.font.render(f"Score: {self.score}", True, "white")
        self.screen.blit(self.text, (0, 31 * TILE_LENGTH))
        
        #init return values
        game_over = False
        reward = delta_score
        
        #check collision with ghost
        if collision_code == 1:
            game_over = True
            reward -= 20
            #if show_end_screen(self.screen, False) == False:
            #    return 1
            self.reset_game()
            self.game_map = load_map(r"pacman_game/resources/initial_map.txt")
        
        #check if hero won    
        if self.score == 280:
            game_over = True
            #if show_end_screen(self.screen, True) == False:
            #    return 1
            self.reset_game()
            self.game_map = load_map(r"pacman_game/resources/initial_map.txt")

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
        
        self.pink_ghost.position.x = TILE_LENGTH * 13.5
        self.pink_ghost.position.y = TILE_LENGTH * 14
        
        self.cyan_ghost.position.x = TILE_LENGTH * 11
        self.cyan_ghost.position.y = TILE_LENGTH * 14
        
        self.orange_ghost.position.x = TILE_LENGTH * 16
        self.orange_ghost.position.y = TILE_LENGTH * 14
        
    def get_state(self):
        game_map_copy = self.game_map.copy()
        game_map_copy[12][11] = '3'
        game_map_copy[12][16] = '3'
        game_map_copy = np.array(game_map_copy).astype(int)
        
        player_positions = np.array([
            self.pacman.position.x, self.pacman.position.y,
            self.red_ghost.position.x, self.red_ghost.position.y,
            self.pink_ghost.position.x, self.pink_ghost.position.y,
            self.cyan_ghost.position.x, self.cyan_ghost.position.y,
            self.orange_ghost.position.x, self.orange_ghost.position.y
        ])
        
        state = np.concatenate((game_map_copy.flatten(), player_positions))
        
        return state
