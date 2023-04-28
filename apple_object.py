import random 
import pygame 
class Apple:
    '''
    Objet pomme qui est la nourriture du serpent

    Attributs
    ------------
    position: position de la pomme
    color: couleur de la pomme RGB

    '''
    def __init__(self,color,grid_size,window_height,window_width):
        self.position = (0, 0)
        self.color = color
        self.randomize_position(grid_size,window_height,window_width)

    def randomize_position(self,grid_size,window_height,window_width):
        '''Position aléatoire de la pomme

        Parameter
        --------
        grid_size: taille de la grille de jeu 
        '''
        grid_width = int(window_width / grid_size)
        grid_height = int(window_height / grid_size)
        self.position = (random.randint(0, grid_width - 1) * grid_size, random.randint(0, grid_height - 1) * grid_size)

    def draw(self, surface,grid_size):
        '''Dessiner la pomme sur le plateau
        
        Parameter
        ---------
        surface: surface du plateau 
        grid_size: taille de la grille de jeu 
        '''
        r = pygame.Rect((self.position[0], self.position[1]), (grid_size, grid_size))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (0, 0, 0), r, 1)
