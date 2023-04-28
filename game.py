import random 
import pygame 
from snake_object import Snake
from apple_object import Apple
import numpy as np 
from Qlearner import QLearn


# Paramètres d'affichage du jeu 
window_width = 640
window_height = 480
grid_size = 40
speed = 1000
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

grid_width = int(window_width / grid_size)
grid_height = int(window_height / grid_size)


# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# Lancement du jeu 
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((window_width, window_height), 0, 32)
surface = pygame.Surface(window.get_size())
surface = surface.convert()
surface.fill(white)
clock = pygame.time.Clock()


# Création du serpent et de la pomme
snake = Snake(green,grid_size,window_width,window_height)
apple = Apple(red,grid_size,window_height,window_width)
qlearn=QLearn(grid_size)

game_count=1
best_score=0
while True:


    clock.tick(speed)
    snake.handle_keys()
    surface.fill(white)
    state=qlearn.get_state(snake, apple,window_height,window_width)
    
    action=qlearn.choose_action(state)
    
    if action==1:
        action=(1, 0)
    elif action==0:
        action=(-1,0)
    elif action==2:
        action=(0,-1)
    elif action==3:
        action=(0,1)

    snake.turn(action)
    snake.move()
    if snake.lost :
        
        previous_state = state
        reward = -1
        new_state = qlearn.get_state(snake, apple,window_height,window_width)
        qlearn.update_q_table(previous_state,action,reward,new_state)
        snake.reset()
        apple=Apple(red,grid_size,window_height,window_width)
        game_count+=1
        print(game_count)
        


    if snake.get_head_position() == apple.position:
        
        snake.length += 1
        apple.randomize_position(grid_size,window_height,window_width)
        previous_state = state
        reward = 1
        new_state = qlearn.get_state(snake, apple,window_height,window_width)
        qlearn.update_q_table(previous_state,action,reward,new_state)

    snake.draw(surface)
    apple.draw(surface,grid_size)
    font = pygame.font.SysFont("comicsansms", 25)
    value = font.render(f"Score: {snake.length}", True, (0,0,0))

    font_best = pygame.font.SysFont("comicsansms", 15)
    value_best = font_best.render(f"best score: {best_score}", True, (0,0,0))
    window.blit(surface, (0,0))
    window.blit(value,(10,10))
    window.blit(value_best,(5,5))
    if snake.length>best_score:
            best_score=snake.length
    if game_count>40:
        qlearn.epsilon=0.7
    if game_count>80:
        qlearn.epsilon=0.4
    if game_count>120:
        qlearn.epsilon=0.1
    if game_count>200:
        qlearn.epsilon=0.01
    pygame.display.update()

