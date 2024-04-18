import pygame

from global_variables import TILE_LENGTH

wall_edge_width = 4

def load_map(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()[1:]
    game_map = []
    for line in lines:
        row = [char for char in line.strip()]
        game_map.append(row)
    return game_map

def draw_map(game_map, screen):
    for j, row in enumerate(game_map):
        for i, elem in enumerate(row):
            if elem == '0':
                x = i * TILE_LENGTH
                y = j * TILE_LENGTH
                if j == 0 or game_map[j - 1][i] != '0':
                    pygame.draw.line(screen, pygame.Color(28, 28, 215), (x, y), (x + TILE_LENGTH, y), wall_edge_width)
                if j == len(game_map) - 1 or game_map[j + 1][i] != '0':
                    pygame.draw.line(screen, pygame.Color(28, 28, 215), (x, y + TILE_LENGTH), (x + TILE_LENGTH, y + TILE_LENGTH), wall_edge_width)
                if i == 0 or game_map[j][i - 1] != '0':
                    pygame.draw.line(screen, pygame.Color(28, 28, 215), (x, y), (x, y + TILE_LENGTH), wall_edge_width)
                if i == len(row) - 1 or game_map[j][i + 1] != '0':
                    pygame.draw.line(screen, pygame.Color(28, 28, 215), (x + TILE_LENGTH, y), (x + TILE_LENGTH, y + TILE_LENGTH), wall_edge_width)
            elif elem == '1':
                pygame.draw.circle(screen, pygame.Color(255, 185, 175), (i*TILE_LENGTH + TILE_LENGTH*0.5, j*TILE_LENGTH + TILE_LENGTH*0.5), 3)
            elif elem == '2':
                pygame.draw.circle(screen, pygame.Color(255, 185, 175), (i*TILE_LENGTH + TILE_LENGTH*0.5, j*TILE_LENGTH + TILE_LENGTH*0.5), TILE_LENGTH / 2 - 2)
            elif elem == '4':
                start_coordinates = (i * TILE_LENGTH, (j + 0.5) * TILE_LENGTH)
                end_coordinates = ((i+1) * TILE_LENGTH, (j + 0.5) * TILE_LENGTH)
                pygame.draw.line(screen, pygame.Color(255, 184, 255), start_coordinates, end_coordinates, 5)