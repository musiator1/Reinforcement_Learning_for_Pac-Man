import torch
import pygame
import random
import numpy as np
from collections import deque
from game import Pacman_Game_AI
from global_variables import Direction
from user_interfaces import show_start_menu
from model import network

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 10    #controll taking random actions
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = network(17, 4)
        self.model.load_state_dict(torch.load(r"model/trained_model.pth"))
        self.model.eval()

    def get_state(self, game):
        return game.get_state()
    
    def get_action(self, state): 
        final_move = [0, 0, 0, 0]
        if random.randint(0, 100) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            
        return final_move
    
def train():
    agent = Agent()
    game = Pacman_Game_AI()
    game.reset_game()
    
    #game loop
    running = show_start_menu(game.screen)
    while running:
        #check for game ending events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #get old state
        state_old = agent.get_state(game)
        
        #get move
        final_move = agent.get_action(state_old)
        
        #perform move and get new state
        reward, game_over, score = game.play_step(final_move)
        
        if game_over:
            game.reset_game()
                            
        game.clock.tick(60)

train()