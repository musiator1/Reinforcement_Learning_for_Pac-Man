import pygame

from hero import Packman

from global_variables import TILE_LENGTH
from global_variables import SCREEN_WIDTH

def load_map(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()[1:]
        
    game_map = []
    for line in lines:
        row = line.strip()
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
screen = pygame.display.set_mode((SCREEN_WIDTH, TILE_LENGTH * 31))
pygame.display.set_caption("Packman")
packman_png = pygame.image.load(r"resources/packman_right_open.png").convert_alpha()
pygame.display.set_icon(packman_png)
packman_png = pygame.transform.smoothscale(packman_png, (TILE_LENGTH, TILE_LENGTH))
screen.fill("black")

game_map = load_map(r"resources/initial_map.txt")
draw_map(game_map)
background = screen.copy().convert()

clock = pygame.time.Clock()
running = True
packman = Packman(packman_png, TILE_LENGTH * 13.5, TILE_LENGTH * 23)


while running:
    screen.blit(background, packman.position, packman.position)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    packman.move(game_map)
    screen.blit(packman.image, packman.position)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

