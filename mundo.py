import pygame # pyright: ignore[reportMissingImports]
import Constantes

class mundo:
    def __init__(self,width,height):
        self.width = width
        self.height = height

    def draw(self,screen):
        screen.fill(Constantes.green)

     