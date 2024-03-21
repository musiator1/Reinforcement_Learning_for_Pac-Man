import pygame

from hero import Pacman
from ghosts import Blinky, Pinky, Inky, Clyde

from global_variables import TILE_LENGTH
from global_variables import SCREEN_WIDTH
from global_variables import Direction

from map import load_map
from map import draw_map

from user_interfaces import show_start_menu
from user_interfaces import show_end_screen

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, TILE_LENGTH * 31 + 50))

### LOAD ALL IMAGES ###
blinky_img = pygame.image.load(r"pacman_game/resources/blinky.png").convert_alpha()
blinky_img = pygame.transform.smoothscale(blinky_img, (TILE_LENGTH, TILE_LENGTH))

pinky_img = pygame.image.load(r"pacman_game/resources/pinky.png").convert_alpha()
pinky_img = pygame.transform.smoothscale(pinky_img, (TILE_LENGTH, TILE_LENGTH))

inky_img = pygame.image.load(r"pacman_game/resources/inky.png").convert_alpha()
inky_img = pygame.transform.smoothscale(inky_img, (TILE_LENGTH, TILE_LENGTH))

clyde_img = pygame.image.load(r"pacman_game/resources/clyde.png").convert_alpha()
clyde_img = pygame.transform.smoothscale(clyde_img, (TILE_LENGTH, TILE_LENGTH))

pcm_imgs = {}
directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
directions_string = ["up", "down", "left", "right"]
mouths = ["closed", "middle", "open"]
for direction_str, direction in zip(directions_string, directions):
    row = []
    for mouth_status in mouths:
        image = pygame.image.load(f"pacman_game/resources/pacman_{direction_str}_{mouth_status}.png").convert_alpha()
        image = pygame.transform.smoothscale(image, (TILE_LENGTH, TILE_LENGTH))
        row.append(image)
    pcm_imgs[direction] = row
        
pygame.display.set_caption("Pacman")
pygame.display.set_icon(pcm_imgs[Direction.RIGHT][2])

game_map = load_map(r"pacman_game/resources/initial_map.txt")
draw_map(game_map, screen)

font = pygame.font.SysFont("Consolas" , 36)
text = font.render("Score: 0", True, "white")

clock = pygame.time.Clock()
running = True

pacman = Pacman(pcm_imgs, TILE_LENGTH * 13.5, TILE_LENGTH * 23)
red_ghost = Blinky(blinky_img, TILE_LENGTH * 13, TILE_LENGTH * 12)
pink_ghost = Pinky(pinky_img, TILE_LENGTH * 13.5, TILE_LENGTH * 14)
cyan_ghost = Inky(inky_img, TILE_LENGTH * 11, TILE_LENGTH * 14)
orange_ghost = Clyde(clyde_img, TILE_LENGTH * 16, TILE_LENGTH * 14)
ghosts = [red_ghost, pink_ghost, cyan_ghost, orange_ghost]

def reset_game():
    pacman.position.x = TILE_LENGTH * 13.5
    pacman.position.y = TILE_LENGTH * 23
    pacman.direction = Direction.NULL
    pacman.desired_direction = Direction.NULL
    pacman.score = 0
    
    red_ghost.position.x = TILE_LENGTH * 13
    red_ghost.position.y = TILE_LENGTH * 11
    
    pink_ghost.position.x = TILE_LENGTH * 13.5
    pink_ghost.position.y = TILE_LENGTH * 14
    pink_ghost.direction = Direction.NULL
    
    cyan_ghost.position.x = TILE_LENGTH * 11
    cyan_ghost.position.y = TILE_LENGTH * 14
    
    orange_ghost.position.x = TILE_LENGTH * 16
    orange_ghost.position.y = TILE_LENGTH * 14    

def is_hero_caught():
    for ghost in ghosts:
        y = ghost.position.y
        x = ghost.position.x
        in_range_x = x - 5 < pacman.position.x < x + 5
        in_range_y = y - 5 < pacman.position.y < y + 5
        if in_range_x and in_range_y:
            return True
    return False

show_start_menu(screen)

while running:
    screen.fill("black")
    draw_map(game_map, screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    score = pacman.move(game_map)
    screen.blit(pacman.actual_image, pacman.position)
    
    red_ghost.move(game_map, pacman.position, pacman.direction)
    screen.blit(red_ghost.image, red_ghost.position)
    
    pink_ghost.move(game_map, pacman.position, pacman.direction)
    screen.blit(pink_ghost.image, pink_ghost.position)
    
    if score >= 30:
        cyan_ghost.move(game_map, pacman.position, pacman.direction, red_ghost.position)
    screen.blit(cyan_ghost.image, cyan_ghost.position)
    
    if score >= 80:
        orange_ghost.move(game_map, pacman.position, pacman.direction)
    screen.blit(orange_ghost.image, orange_ghost.position)
    
    text = font.render(f"Score: {score}", True, "white")
    screen.blit(text, (0, 31 * TILE_LENGTH))
    
    if is_hero_caught():
        show_end_screen(screen, False)
        reset_game()
        game_map = load_map(r"pacman_game/resources/initial_map.txt")

    pygame.display.flip()
    clock.tick(60)
pygame.quit()

