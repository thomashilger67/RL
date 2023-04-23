import random
import json

import dataclasses

@dataclasses.dataclass
class GameState:
    distance: tuple # distances horizontale et verticale entre le snake et la nourriture
    position: tuple # positions horizontale et verticale de la nourriture par rapport au snake
    surroundings: str # obstacles autour de la tête du snake (limites de l'écran ou queue du snake)
    food: tuple # position de la nourriture


class Learner(object):
    def __init__(self, longueur, hauteur, snake_unite):
        # Paramètres du jeu
        self.longueur = longueur
        self.hauteur = hauteur
        self.snake_unite = snake_unite

        # Paramètres pour l'apprentissage
        self.epsilon = 0.1
        self.lr = 0.7
        self.discount = 0.5

        # Historique des états et actions
        self.qvalues = self.LoadQvalues()
        self.history = []

        # Espace des actions
        self.actions = {
            0:'left',
            1:'right',
            2:'up',
            3:'down'
        }

    def Reset(self):
        self.history = []

    def LoadQvalues(self, path="qvalues.json"):
        with open(path, "r") as f:
            qvalues = json.load(f)
        return qvalues

    def SaveQvalues(self, path="qvalues.json"):
        with open(path, "w") as f:
            json.dump(self.qvalues, f)
            
    def act(self, snake, food):
        state = self._GetState(snake, food)

        # Epsilon greedy
        rand = random.uniform(0,1)
        if rand < self.epsilon:
            action_key = random.choices(list(self.actions.keys()))[0]
        else:
            state_scores = self.qvalues[self._GetStateStr(state)]
            action_key = state_scores.index(max(state_scores))
        action_val = self.actions[action_key]
        
        # Ajouter à l'historique l'action pour chaque état
        self.history.append({
            'state': state,
            'action': action_key
            })
        return action_val
    
    def UpdateQValues(self, game_over):
        history = self.history[::-1]
        for i, h in enumerate(history[:-1]):
            if game_over: # game over -> reward négatif
                sN = history[0]['state']
                aN = history[0]['action']
                state_str = self._GetStateStr(sN)
                reward = -1
                self.qvalues[state_str][aN] = (1-self.lr) * self.qvalues[state_str][aN] + self.lr * reward
            else:
                s1 = h['state'] # état actuel
                s0 = history[i+1]['state'] # état précédent
                a0 = history[i+1]['action'] # action effectuée à l'état précédent
                
                x1 = s0.distance[0] # distance horizontale à l'état actuel
                y1 = s0.distance[1] # distance verticale à l'état actuel
    
                x2 = s1.distance[0] # distance horizontale à l'état précédent
                y2 = s1.distance[1] # distance verticale à l'état précédent
                
                if s0.food != s1.food: # le snake mange -> reward positif
                    reward = 1
                elif (abs(x1) > abs(x2) or abs(y1) > abs(y2)): # le snake se rapproche de la nourriture -> reward positif
                    reward = 1
                else:
                    reward = -1 # le snake s'éloigne de la nourriture -> reward négatif
                    
                state_str = self._GetStateStr(s0)
                new_state_str = self._GetStateStr(s1)
                self.qvalues[state_str][a0] = (1-self.lr) * (self.qvalues[state_str][a0]) + self.lr * (reward + self.discount*max(self.qvalues[new_state_str]))


    def _GetState(self, snake, food):
        snake_head = snake[-1]
        dist_x = food[0] - snake_head[0]
        dist_y = food[1] - snake_head[1]

        if dist_x > 0:
            pos_x = '1' # la nourriture est à droite du snake
        elif dist_x < 0:
            pos_x = '0' # la nourriture est à gauche du snake
        else:
            pos_x = 'NA' # la nourriture et le snake sont au même niveau horizontalement

        if dist_y > 0:
            pos_y = '3' # la nourriture est en-dessous du snake
        elif dist_y < 0:
            pos_y = '2' # la nourriture est au-dessus du snake
        else:
            pos_y = 'NA' # la nourriture et le snake sont au même niveau verticalement

        sqs = [
            (snake_head[0]-self.snake_unite, snake_head[1]),   
            (snake_head[0]+self.snake_unite, snake_head[1]),         
            (snake_head[0],                  snake_head[1]-self.snake_unite),
            (snake_head[0],                  snake_head[1]+self.snake_unite),
        ]
        
        surrounding_list = []
        for sq in sqs:
            if sq[0] < 0 or sq[1] < 0: # en dehors de l'écran à gauche ou en haut
                surrounding_list.append('1')
            elif sq[0] >= self.longueur or sq[1] >= self.hauteur: # en dehors de l'écran à droite ou en bas
                surrounding_list.append('1')
            elif sq in snake[:-1]: # partie de la queue
                surrounding_list.append('1')
            else:
                surrounding_list.append('0')
        surroundings = ''.join(surrounding_list)

        return GameState((dist_x, dist_y), (pos_x, pos_y), surroundings, food)

    def _GetStateStr(self, state):
        return str((state.position[0],state.position[1],state.surroundings))