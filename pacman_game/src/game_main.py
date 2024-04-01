import pygame

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

def reset_game():
    global ghost_counter
    pacman.position.x = TILE_LENGTH * 13.5
    pacman.position.y = TILE_LENGTH * 23
    pacman.direction = Direction.NULL
    pacman.desired_direction = Direction.NULL
    pacman.score = 0
    ghost_counter = 0
    
    for ghost in ghosts:
        ghost.direction = Direction.NULL
        ghost.change_mode_values = [900, 3470, 4370, 6940, 7583, 10153, 10796]
        if ghost.mode == Mode.FRIGHTENED:
            ghost.frightened_counter = 0
            ghost.image = ghost.normal_image
    
    red_ghost.position.x = TILE_LENGTH * 13
    red_ghost.position.y = TILE_LENGTH * 11
    
    pink_ghost.position.x = TILE_LENGTH * 13.5
    pink_ghost.position.y = TILE_LENGTH * 14
    
    cyan_ghost.position.x = TILE_LENGTH * 11
    cyan_ghost.position.y = TILE_LENGTH * 14
    
    orange_ghost.position.x = TILE_LENGTH * 16
    orange_ghost.position.y = TILE_LENGTH * 14    

#init game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, TILE_LENGTH * 31 + 50))  
pygame.display.set_caption("Pacman") 
clock = pygame.time.Clock()

#load images
red_ghost_img, pink_ghost_img, cyan_ghost_img, orange_ghost_img, pcm_imgs = load_ghosts_hero_imgs()
pygame.display.set_icon(pcm_imgs[Direction.RIGHT][2])

#load map
game_map = load_map(r"pacman_game/resources/initial_map.txt")
draw_map(game_map, screen)

#display score
font = pygame.font.SysFont("Consolas" , 36)
text = font.render("Score: 0", True, "white")

#init hero and ghosts
pacman = Pacman(pcm_imgs, TILE_LENGTH * 13.5, TILE_LENGTH * 23)
red_ghost = Red_Ghost(red_ghost_img, TILE_LENGTH * 13, TILE_LENGTH * 11)
pink_ghost = Pink_Ghost(pink_ghost_img, TILE_LENGTH * 13.5, TILE_LENGTH * 14)
cyan_ghost = Cyan_Ghost(cyan_ghost_img, TILE_LENGTH * 11, TILE_LENGTH * 14)
orange_ghost = Orange_Ghost(orange_ghost_img, TILE_LENGTH * 16, TILE_LENGTH * 14)
score = 0
ghost_counter = 0
ghosts = [red_ghost, pink_ghost, cyan_ghost, orange_ghost]

#game loop
running = True
continue_playing = show_start_menu(screen)
while running and continue_playing:
    #check for game ending events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #check if any ghost is in frightened mode
    if not any(ghost.mode == Mode.FRIGHTENED for ghost in ghosts):
        ghost_counter += GAME_SPEED
    
    #actualize state of the game and get information about collision
    old_score = score      
    score = pacman.move(game_map)
    if score - old_score == 10:
        for ghost in ghosts:
            if ghost.mode != Mode.DEAD:
                ghost.be_frightened(600)
    
    collision_code = 0        
    collision_code |= red_ghost.move(game_map, pacman.position, pacman.direction, ghost_counter)
    collision_code |= pink_ghost.move(game_map, pacman.position, pacman.direction, ghost_counter)
    if score >= 30:
        collision_code |= cyan_ghost.move(game_map, pacman.position, pacman.direction, ghost_counter, red_ghost.position)
    if score >= 80:
        collision_code |= orange_ghost.move(game_map, pacman.position, pacman.direction, ghost_counter)
    
    #draw actual state of the game    
    screen.fill("black")
    draw_map(game_map, screen)
    screen.blit(pacman.actual_image, pacman.position)
    screen.blit(red_ghost.image, red_ghost.position)
    screen.blit(pink_ghost.image, pink_ghost.position)
    screen.blit(cyan_ghost.image, cyan_ghost.position)
    screen.blit(orange_ghost.image, orange_ghost.position)
    
    #display actual score
    text = font.render(f"Score: {score}", True, "white")
    screen.blit(text, (0, 31 * TILE_LENGTH))
    
    #check collision with ghost
    if collision_code == 1:
        if show_end_screen(screen, False) == False:
            break
        reset_game()
        game_map = load_map(r"pacman_game/resources/initial_map.txt")
       
    #check if hero won    
    if score == 280:
        if show_end_screen(screen, True) == False:
            break
        reset_game()
        game_map = load_map(r"pacman_game/resources/initial_map.txt")

    pygame.display.flip()
    clock.tick(60)
pygame.quit()