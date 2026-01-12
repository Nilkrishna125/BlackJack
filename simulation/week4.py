import numpy as np
import matplotlib.pyplot as plt

from blackjack import BlackJack
from typing import List


class tasks_week4:
    def __init__(self):
        pass
    
    def state_index(self, s: tuple):
        return (s[0]-1) + 31*(s[1] - 1) + 31*11*s[2] 
    
    def q_action_index(self, a: tuple): #(state, action)
        return (a[0][0]-1) + 31*(a[0][1] - 1) + 31*11*a[0][2] + 31*11*2*a[1] #0 for hit and 1 for stay


    def task1(self):
        episodes = 10_000
        game = BlackJack()
        Returns = np.zeros(341*2)
        hit = "hit"
        stay = "stay"
        state_count = np.ones(341*2)

        while episodes > 0:

            state, reward, done = game.reset()
            state_matrix = np.zeros(341*2) #31*11
            index = self.state_index(state)
            index_list = [index]
            state_count[index] += 1
            # try:
            #     state_matrix[index] = 1
            #     Returns[index] += reward
            # except:
            #     print(state)

            while not done:
                if game.player_hand.value() < 20:
                    state, reward, done = game.step(hit)
                    index = self.state_index(state)
                    if not state_matrix[index]:
                        state_matrix[index] = 1
                        index_list.append(index)
                        state_count[index] += 1

                else:
                    state, reward, done = game.step(stay)
                    index = self.state_index(state)
                    if not state_matrix[index]:
                        state_matrix[index] = 1
                        index_list.append(index)
                        state_count[index] += 1

            for i in index_list:
                Returns[i] += reward
            episodes -= 1
                
        for i in range(341*2):
            if state_count[i]:
                Returns[i] /= state_count[i]

        
        print("Player sum 21 : ", Returns[20::31].sum()) 
        print("Player sum 5 : ", Returns[4::31].sum()) 

    def task2(self):
        episodes = 500_000
        alpha = 1 
        beta = 0.1

        game = BlackJack()
        Q_values = np.zeros(341*2*2) #states*actions
        hit = "hit"
        stay = "stay"

        while episodes > 0:

            state, reward, done = game.reset()
            state_value_list = []

            if done:
                index = self.q_action_index((state, 1))
                Q_values[index] += beta*(reward - Q_values[index])

            while not done:
                l = np.random.default_rng().uniform(0,1)
                if l < alpha:
                    choice = np.random.choice([hit, stay])
                    s = 0 if choice == hit else 1
                    state1, reward, done = game.step(choice)
                    state_value_list.append((state, s))
                    state = state1

                else:

                    q_hit = Q_values[self.q_action_index((state, 0))]
                    q_stay = Q_values[self.q_action_index((state, 1))]
                    if q_hit >= q_stay:
                        state1, reward, done = game.step(hit)
                        state_value_list.append((state, 0))
                        state = state1
    
                    else:
                        state1, reward, done = game.step(stay)
                        state_value_list.append((state, 1))
                        state = state1

            for state, action in state_value_list:
                index = self.q_action_index((state, action))
                Q_values[index] += beta*(reward - Q_values[index])

            episodes -= 1
            alpha *= 0.999

        

        for i in Q_values:
            print(i)

    def task3(self):
        episodes = 500_000
        alpha = 1
        beta = 0.1 #gamma
        avg_roll = [0]

        game = BlackJack()
        Q_values = np.zeros(341*2*2) #states*actions
        Q_values[31*11*2+20::31] = 1
        hit = "hit"
        stay = "stay"

        while episodes > 0:

            state, reward, done = game.reset()
            state_value_list = []

            if done:
                index = self.q_action_index((state, 1))
                Q_values[index] += beta*(reward - Q_values[index])

            while not done:
                l = np.random.default_rng().uniform(0,1)
                if l < alpha:
                    choice = np.random.choice([hit, stay])
                    s = 0 if choice == hit else 1
                    state1, reward, done = game.step(choice)
                    state_value_list.append((state, s))
                    state = state1

                else:

                    q_hit = Q_values[self.q_action_index((state, 0))]
                    q_stay = Q_values[self.q_action_index((state, 1))]
                    if q_hit >= q_stay:
                        state1, reward, done = game.step(hit)
                        state_value_list.append((state, 0))
                        state = state1
    
                    else:
                        state1, reward, done = game.step(stay)
                        state_value_list.append((state, 1))
                        state = state1

            for state, action in state_value_list:
                index = self.q_action_index((state, action))
                Q_values[index] += beta*(reward - Q_values[index])
            
            n = len(avg_roll)
            avg_roll.append((avg_roll[-1]*(n-1) + reward)/n)

            episodes -= 1
            alpha *= 0.99999
    
        game_number = np.arange(len(avg_roll))
        
        plt.figure(figsize=(20,10))
        plt.plot(game_number, avg_roll)
        plt.xlabel("Game Number")
        plt.ylabel("Avg Win")
        plt.title("Rolling Average Win")
        plt.show()

        fig, axes = plt.subplots(1,2, figsize=(20,10))

        # taking no ace here ###################

        grid = np.zeros((10,10)) #2-10 then the last for the dealer having the ace #the player sum from 12 onwards
        for i in range(10):
            for j in range(10):
                q_hit = Q_values[self.q_action_index(((i + 12,j+2,0), 0))]
                q_stay = Q_values[self.q_action_index(((i + 12,j+2,0), 1))]
                grid[i][j] = 0 if q_hit >= q_stay else 1

        im = axes[0].imshow(grid, origin='lower', extent=[2, 11, 12, 21], cmap='viridis')
        axes[0].set_title("Heat Map 1, Without ACE", fontsize=30)
        axes[0].set_xlabel("Dealer Sum", fontsize=25)
        axes[0].set_ylabel("Player Sum", fontsize=25)
        plt.colorbar(im, ax=axes[0])

        # taking ace here ###################

        grid = np.zeros((10,10)) #2-10 then the last for the dealer having the ace #the player sum from 12 onwards
        for i in range(10):
            for j in range(10):
                q_hit = Q_values[self.q_action_index(((i + 12,j+2,1), 0))]
                q_stay = Q_values[self.q_action_index(((i + 12,j+2,1), 1))]
                grid[i][j] = 0 if q_hit >= q_stay else 1
        
        im2 = axes[1].imshow(grid, origin='lower', extent=[2, 11, 12, 21], cmap='viridis')
        axes[1].set_title("Heat Map 2, With ACE", fontsize=30)
        axes[1].set_xlabel("Dealer Sum", fontsize=25)
        axes[1].set_ylabel("Player Sum", fontsize=25)
        plt.colorbar(im2, ax=axes[1])

        fig.text(0.05, 0.95, "0 = Hit, 1 = Stay", ha='center', fontsize=15)


        plt.tight_layout()
        plt.show()



            




task = tasks_week4()
task.task3()