import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
longueur = 800
hauteur = 400
 
dis = pygame.display.set_mode((longueur, hauteur)) 
pygame.display.set_caption('Snake for Q-learning')
 
clock = pygame.time.Clock()
 
snake_unite = 10
snake_vitesse = 10
 
font = pygame.font.SysFont("bahnschrift", 25)
 
def Score(score):
    value = font.render("score : " + str(score), True, black)
    dis.blit(value, [0, 0])
 
 
 
def snake(snake_unite, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_unite, snake_unite])
 
 
def message(msg, color):
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [longueur / 6, hauteur / 3])
 
 
def Game():
    game_over = False
    game_close = False
 
    x1 = longueur / 2
    y1 = hauteur / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    longueur_du_snake = 1
 
    foodx = round(random.randrange(0, longueur - snake_unite) / 10.0) * 10.0
    foody = round(random.randrange(0, hauteur - snake_unite) / 10.0) * 10.0
 
    while not game_over:
 
        while game_close == True:
            dis.fill(white)
            message("Partie perdue ! Pour quitter ctrl q ou rejouer ctrl c", black)
            Score(longueur_du_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        Game()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_unite
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_unite
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_unite
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_unite
                    x1_change = 0
 
        if x1 >= longueur or x1 < 0 or y1 >= hauteur or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, red, [foodx, foody, snake_unite, snake_unite])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > longueur_du_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        snake(snake_unite, snake_List)
        Score(longueur_du_snake - 1)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, longueur - snake_unite) / 10.0) * 10.0
            foody = round(random.randrange(0, hauteur - snake_unite) / 10.0) * 10.0
            longueur_du_snake += 1
 
        clock.tick(snake_vitesse)
 
    pygame.quit()
    quit()
 
 
Game()
