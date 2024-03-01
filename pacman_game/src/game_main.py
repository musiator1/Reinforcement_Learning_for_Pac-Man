import pygame

from hero import Pacman

from global_variables import TILE_LENGTH
from global_variables import SCREEN_WIDTH
from global_variables import Direction

### INITIALIZE MAP ###
def load_map(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()[1:]
        
    game_map = []
    for line in lines:
        row = [char for char in line.strip()]
        game_map.append(row)
        
    return game_map

def draw_map(game_map):
    i = 0
    j = 0
    for row in game_map:
        i = 0
        for elem in row:
            if elem == '0':
                pygame.draw.rect(screen, pygame.Color(28, 28, 215), (i*TILE_LENGTH, j*TILE_LENGTH, TILE_LENGTH, TILE_LENGTH), 2)
            elif elem == '1':
                pygame.draw.circle(screen, pygame.Color(255, 185, 175), (i*TILE_LENGTH + TILE_LENGTH*0.5, j*TILE_LENGTH + TILE_LENGTH*0.5), 3)
            elif elem == '2':
                pygame.draw.circle(screen, pygame.Color(255, 185, 175), (i*TILE_LENGTH + TILE_LENGTH*0.5, j*TILE_LENGTH + TILE_LENGTH*0.5), TILE_LENGTH / 2 - 2)
            elif elem == '4':
                start_coordinates = (i * TILE_LENGTH, (j + 0.5) * TILE_LENGTH)
                end_coordinates = ((i+1) * TILE_LENGTH, (j + 0.5) * TILE_LENGTH)
                pygame.draw.line(screen, pygame.Color(255, 184, 255), start_coordinates, end_coordinates, 5)
            i+=1
        j+=1    

### GAME ###
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, TILE_LENGTH * 31 + 50))

### LOAD ALL IMAGES ###
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
draw_map(game_map)

font = pygame.font.SysFont("Consolas", 36)
text = font.render("Score: 0", True, "white")

clock = pygame.time.Clock()
running = True
packman = Pacman(pcm_imgs, TILE_LENGTH * 13.5, TILE_LENGTH * 23)

while running:
    screen.fill("black")
    draw_map(game_map)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    score = packman.move(game_map)
    screen.blit(packman.actual_image, packman.position)
    text = font.render(f"Score: {score}", True, "white")
    screen.blit(text, (0, 31 * TILE_LENGTH))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

