import random 
import numpy as np 
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

class QLearn:
    '''
    Objet Qlearn qui implémente un agent qui va apprendre à jouer au jeu avec une stratégie de Q-learning

    Parameters
    ------------
    grid_size: taille de la grille
    q_table= historique des états
    epsilon
    alpha
    gamma
    '''
    def __init__(self,grid_size,eps=0.8,alpha=0.01,gamma=0.9):
        self.grid_size=grid_size
        self.q_table = {}
        self.epsilon = eps
        self.alpha = alpha
        self.gamma = gamma


    def get_state(self, snake, apple,window_height,window_width):
        '''
        Récupère l'état actuelle du jeu

        Parameters
        ------------
        snake : serpent
        apple : pomme à manger
        '''
        head_x, head_y = snake.get_head_position()
        diff_x = apple.position[0] - head_x
        diff_y = apple.position[1] - head_y
        direction=snake.direction
        if diff_x > 0:
            pos_x = '1' # la pomme est à droite du serpent 
        elif diff_x < 0:
            pos_x = '0' # la pomme est à gauche du serpent
        else:
            pos_x = 'SAME' # la pomme et le serpent sont sur la meme ligne

        if diff_y > 0:
            pos_y = '3' # la pomme est en dessous du serpent 
        elif diff_y < 0:
            pos_y = '2' # la pomme est au dessus du serpent 
        else:
            pos_y = 'SAME' #  la pomme et le serpent sont sur la meme colonne
        
        arround = [(head_x-self.grid_size, head_y),(head_x+self.grid_size, head_y),(head_x,head_y-self.grid_size),(head_x,head_y+self.grid_size)]
        
        autour_list = []
        for sq in arround:
            if sq[0] <= 0 or sq[1] <= 0: # frontière à gauche ou en haut
                autour_list.append('1')
            elif sq[0] >= window_width or sq[1] >= window_height: #frontière à droite ou en bas
                autour_list.append('1')
            elif sq in snake.positions[2:]: # s'est mordu la queue
                autour_list.append('1')
            else:
                autour_list.append('0')
        autour_resu = ''.join(autour_list)

        return ((pos_x,pos_y),autour_resu)



    def choose_action(self,state):
        '''
        Choisit l'action à prendre 

        '''
        if np.random.uniform() < self.epsilon:
            
            action = random.choice([UP, DOWN, LEFT, RIGHT])
        else:
            
            if str(state) in self.q_table:
                action = np.argmax(self.q_table[str(state)])
            else:
                
                action = random.choice([UP, DOWN, LEFT, RIGHT])
        return action

    def update_q_table(self,prev_state, action, reward, state):
        
        if action==UP:
            num=2
        elif action==DOWN:
            num=3
        elif action==RIGHT:
            num=1
        else:
            num=0
        
        if str(prev_state) not in self.q_table:
            self.q_table[str(prev_state)] = np.zeros(4)
        if str(state) not in self.q_table:
            self.q_table[str(state)] = np.zeros(4)
        
        prev_q = self.q_table[str(prev_state)][num]
        max_q = np.max(self.q_table[str(state)])
        
        new_q = (1 - self.alpha) * prev_q + self.alpha * (reward + self.gamma * max_q) # formule de q-learning

        self.q_table[str(prev_state)][num] = new_q

