import pygame

from global_variables import TILE_LENGTH
from global_variables import Direction

def load_ghosts_hero_imgs():
    red_ghost_img = pygame.image.load(r"pacman_game/resources/blinky.png").convert_alpha()
    red_ghost_img = pygame.transform.smoothscale(red_ghost_img, (TILE_LENGTH, TILE_LENGTH))

    pink_ghost_img = pygame.image.load(r"pacman_game/resources/pinky.png").convert_alpha()
    pink_ghost_img = pygame.transform.smoothscale(pink_ghost_img, (TILE_LENGTH, TILE_LENGTH))

    cyan_ghost_img = pygame.image.load(r"pacman_game/resources/inky.png").convert_alpha()
    cyan_ghost_img = pygame.transform.smoothscale(cyan_ghost_img, (TILE_LENGTH, TILE_LENGTH))

    orange_ghost_img = pygame.image.load(r"pacman_game/resources/clyde.png").convert_alpha()
    orange_ghost_img = pygame.transform.smoothscale(orange_ghost_img, (TILE_LENGTH, TILE_LENGTH))

    pcm_imgs = load_pacman_imgs()
    
    return red_ghost_img, pink_ghost_img, cyan_ghost_img, orange_ghost_img, pcm_imgs
    
def load_pacman_imgs():
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
    return pcm_imgs