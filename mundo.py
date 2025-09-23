import os
import random
import pygame # pyright: ignore[reportMissingImports]
import Constantes
import Elementos

class mundo:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.arbol = [Elementos.arbol(random.randint(0,width-40),random.randint(0,height-40)) for _ in range(10)] # rango de 10 arboles
        cesped_path = os.path.join('assets','IMG','Objetos','cesped.png')
        self.cesped = pygame.image.load(cesped_path).convert()
        self.cesped = pygame.transform.scale(self.cesped, (Constantes.cesped, Constantes.cesped))

    def draw(self,screen):
        for y in range(0, self.height, Constantes.cesped):
            for x in range(0, self.width, Constantes.cesped):
                screen.blit(self.cesped, (x, y))

        for arbol in self.arbol:
            arbol.draw(screen)
     