import torch
import pygame
import random
import numpy as np
from collections import deque
from game import Pacman_Game_AI
from user_interfaces import show_start_menu
from model import network, QTrainer
from plotter import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 100    #controll taking random actions
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = network(17, 4)
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)

    def get_state(self, game):
        return game.get_state()
    
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
        if self.n_games < 90:
            self.epsilon = 100 - self.n_games
        else:
            self.epsilon = 10
        
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
    plot_scores = []
    plot_mean_scores = [0]
    total_score = 0
    record = 0
    agent = Agent()
    game = Pacman_Game_AI()
    game.reset_game()
    rewards = 0
    
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
        
        rewards += reward
        
        #train short memory 
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        
        #remember
        agent.remember(state_old, final_move, reward, state_new, game_over)
        
        if game_over:
            #train long memeory
            game.reset_game()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score >= record:
                record = score
                agent.model.save()
                
            print("Game:", agent.n_games, "Score:", score, "Record:", record, "Reward:", rewards)
            rewards = 0
            
            plot_scores.append(score)
            total_score += score
            if agent.n_games % 20 == 0:
                mean_score = total_score / 20
                plot_mean_scores.append(mean_score)
                total_score = 0
            plot(plot_scores, plot_mean_scores)
            
        #game.clock.tick(60)

train()