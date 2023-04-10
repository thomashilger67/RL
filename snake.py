import pygame
import random
import Learner

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

longueur = 800
hauteur = 400

snake_unite = 10
snake_vitesse = 50000

font = pygame.font.SysFont("bahnschrift", 25)

qvalues_n = 100


def food(foodx, foody):
    pygame.draw.rect(dis, red, [foodx, foody, snake_unite, snake_unite])   

def snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_unite, snake_unite])

def Score(score):
    value = font.render("score : " + str(score), True, black)
    dis.blit(value, [0, 0])


def Game():
    global dis
    
    dis = pygame.display.set_mode((longueur, hauteur))
    pygame.display.set_caption('Snake for Q-learning')
    clock = pygame.time.Clock()

    # Position de départ du snake
    x1 = longueur / 2
    y1 = hauteur / 2
    x1_change = 0
    y1_change = 0
    snake_list = [(x1,y1)]
    longueur_du_snake = 1

    # Première nourriture
    foodx = round(random.randrange(0, longueur - snake_unite) / 10.0) * 10.0
    foody = round(random.randrange(0, hauteur - snake_unite) / 10.0) * 10.0

    dead = False
    while not dead:
        # Récupère l'action du learner
        action = learner.act(snake_list, (foodx,foody))
        if action == "left":
            x1_change = -snake_unite
            y1_change = 0
        elif action == "right":
            x1_change = snake_unite
            y1_change = 0
        elif action == "up":
            y1_change = -snake_unite
            x1_change = 0
        elif action == "down":
            y1_change = snake_unite
            x1_change = 0

        # Fait avancer le snake
        x1 += x1_change
        y1 += y1_change
        snake_head = (x1,y1)
        snake_list.append(snake_head)

        # Vérifie si le snake est en dehors de l'écran
        if x1 >= longueur or x1 < 0 or y1 >= hauteur or y1 < 0:
            dead = True

        # Vérifie si le snake se mord la queue
        if snake_head in snake_list[:-1]:
            dead = True

        # Vérifie si le snake mange la nourriture
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, longueur - snake_unite) / 10.0) * 10.0
            foody = round(random.randrange(0, hauteur - snake_unite) / 10.0) * 10.0
            longueur_du_snake += 1

        # Supprime la dernière partie du snake car le snake a été initialisé avec sa tête
        if len(snake_list) > longueur_du_snake:
            del snake_list[0]

        # Dessine la nourriture et le snake
        dis.fill(white)
        food(foodx, foody)
        snake(snake_list)

        # Met à jour le score
        Score(longueur_du_snake - 1)
        pygame.display.update()

        # Met à jour la Q-Table
        learner.UpdateQValues(dead)
        
        clock.tick(snake_vitesse)

    return longueur_du_snake - 1



game_count = 1

learner = Learner.Learner(longueur, hauteur, snake_unite)

while True:
    learner.Reset()
    if game_count > 100:
        learner.epsilon = 0
    else:
        learner.epsilon = .1
    score = Game()
    print(f"Games: {game_count}; Score: {score}") # Résultats de chaque jeu pendant la phase d'entrainement
    game_count += 1
    if game_count % qvalues_n == 0: # Enregistre les qvalues
        print("Save Qvals")
        learner.SaveQvalues()
