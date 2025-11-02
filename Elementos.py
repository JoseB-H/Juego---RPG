import os
import pygame  # pyright: ignore[reportMissingImports]
import Constantes

class arbol:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        path_Tree = os.path.join('assets','IMG','Objetos','Arbol.png')
        self.image = pygame.image.load(path_Tree).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Constantes.Tree, Constantes.Tree))
        self.size = self.image.get_width()
        self.wood = 5

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def talar (self):
        if self.wood > 0:
           self.wood -= 1
           return True
        return False

class Mini_stone: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stone = 1
        path_mini_stone = os.path.join('assets','IMG','Objetos','mini_stone.png')
        self.image = pygame.image.load(path_mini_stone).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Constantes.smallStone, Constantes.smallStone))
        self.size = self.image.get_width()

    def draw(self, screen): 
        screen.blit(self.image, (self.x, self.y))