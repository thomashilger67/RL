import pygame
import random

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    '''
    Objet serpent pour le jeu snake
    
    Parameters
    -------------
    color: couleur du serpent RGB
    window_width: longueur de la fenêtre de jeu
    window_height: hauteur de la fenêtre de jeu

    Attributs
    ----------------
    length: longueur du serpent 
    positions: positions du serpent 
    color: couleur du serpent 
    lost: si le serpent a perdu 
    '''

    def __init__(self,color,grid_size,window_width=640,window_height=480):
        self.length = 1
        self.positions = [((window_width / 2), (window_height / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = color
        self.lost=False
        self.grid_size=grid_size
        self.window_width=window_width
        self.window_height=window_height


    def get_head_position(self):
        '''
        Renvoie la position de la tête du serpent 
        '''
        return self.positions[0]


    def turn(self, point):
        '''
        Change la direction du serpent 

        Parameter 
        -----------
        point: directions (UP, DOWN, RIGHT, LEFT)
        '''

        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point


    def move(self):
        '''
        Fait avancer le serpent 
        '''
    
        cur = self.get_head_position()

        x, y = self.direction
        new = (((cur[0] + (x * self.grid_size)) % self.window_width), (cur[1] + (y * self.grid_size)) % self.window_height)
        
        if new in self.positions[2:]:
            self.lost=True 
        if new[0]>=self.window_width or new[0]<=0 or new[1]>= self.window_height or new[1]<=0:
            self.lost=True
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()


    def reset(self):
        '''
        Remise à zéro du serpent au centre du plateau 
        '''
        self.length = 1
        self.positions = [((self.window_width / 2), (self.window_height / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.lost=False


    def draw(self, surface):
        '''Dessine le serpent sur le plateau
        
        Parameter
        ---------
        surface: surface du plateau 
        '''

        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (self.grid_size, self.grid_size))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (0, 0, 0), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)



