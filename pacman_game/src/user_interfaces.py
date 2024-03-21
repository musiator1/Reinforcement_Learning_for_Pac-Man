import pygame
from pygame.locals import *

from global_variables import TILE_LENGTH
from global_variables import SCREEN_WIDTH

def show_option_menu(screen, path1, path2):
    pygame.init()
    text_height = 50
    counter = 0
    screen_copy = screen.copy()
    screen_copy.set_alpha(100)
    screen.fill("black")
    screen.blit(screen_copy,(0, 0))
    
    logo = pygame.image.load(path1)
    logo = pygame.transform.smoothscale_by(logo, 300 / logo.get_height())
    button1 = pygame.image.load(path2)
    button1 = pygame.transform.smoothscale_by(button1, text_height / button1.get_height())
    button2 = pygame.image.load(r"pacman_game/resources/exit_bttn.png")
    button2 = pygame.transform.smoothscale_by(button2, text_height / button2.get_height())
    pointer = pygame.image.load(r"pacman_game/resources/pointer.png")
    pointer = pygame.transform.smoothscale(pointer, (text_height, text_height))
    
    logo_y = 30
    button1_y = logo_y + logo.get_height() + 30
    button2_y = button1_y + button1.get_height() + TILE_LENGTH * 2
    pointer_x = (SCREEN_WIDTH - button1.get_width()) / 2 - text_height - 20
    pointer_y = (button1_y)
    
    screen.blit(logo, ((SCREEN_WIDTH - logo.get_width()) / 2, logo_y))
    screen.blit(button1, ((SCREEN_WIDTH - button1.get_width()) / 2, button1_y))
    screen.blit(button2, ((SCREEN_WIDTH - button2.get_width()) / 2, button2_y))
    screen.blit(pointer, (pointer_x, pointer_y))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_TAB:
                    counter += 1
                elif event.key == pygame.K_UP:
                    counter -= 1
                pointer_y = button1_y + (counter % 2) * (text_height + TILE_LENGTH * 2)
                screen.fill("black")
                screen.blit(screen_copy,(0, 0))
                screen.blit(logo, ((SCREEN_WIDTH - logo.get_width()) / 2, logo_y))
                screen.blit(button1, ((SCREEN_WIDTH - button1.get_width()) / 2, button1_y))
                screen.blit(button2, ((SCREEN_WIDTH - button2.get_width()) / 2, button2_y))
                screen.blit(pointer, (pointer_x, pointer_y))
                pygame.display.flip()

                if event.key == pygame.K_RETURN:
                    if counter % 2 == 0:
                        waiting = False
                    else:
                        pygame.quit()

def show_start_menu(screen):
    show_option_menu(screen, r"pacman_game/resources/start_txt.png", r"pacman_game/resources/start_bttn.png")
                               
def show_end_screen(screen, game_won):
    if game_won == True:
        show_option_menu(screen, r"pacman_game/resources/win.png", r"pacman_game/resources/restart_bttn.png")
    else:
        show_option_menu(screen, r"pacman_game/resources/lose.png", r"pacman_game/resources/restart_bttn.png")