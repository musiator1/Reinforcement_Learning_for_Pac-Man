import torch
import pygame
import random
import numpy as np
from collections import deque
from game import Pacman_Game_AI
from global_variables import Direction
from user_interfaces import show_start_menu
from map import draw_map
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0    #controll taking random actions
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(878 ,256, 4)
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)
        # TODO: model, trainer

    def get_state(self, game):
        return game.state
    
    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)    
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
        
    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)
    
    def get_action(self, state):
        #random moves:
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            
        return final_move
    
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
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
        state_new = agent.get_state(game)
        
        #train short memory 
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        
        #remember
        agent.remember(state_old, final_move, reward, state_new, game_over)
        
        if game_over:
            #train long memeory
            game.reset_game()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score > record:
                record = score
                agent.model.save()
                
            print("Game:", agent.n_games, "Score:", score, "Record:", record)  
            
        #game.clock.tick(60)


train()