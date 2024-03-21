import pygame

from global_variables import TILE_LENGTH

def load_map(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()[1:]
        
    game_map = []
    for line in lines:
        row = [char for char in line.strip()]
        game_map.append(row)
        
    return game_map

def draw_map(game_map, screen):
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