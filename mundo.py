import random
import pygame # pyright: ignore[reportMissingImports]
import Constantes
import Elementos

class mundo:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.arbol = [Elementos.arbol(random.randint(0,width-40),random.randint(0,height-40)) for _ in range(10)] # rango de 10 arboles

    def draw(self,screen):
        screen.fill(Constantes.green)
        for arbol in self.arbol:
            arbol.draw(screen)
     