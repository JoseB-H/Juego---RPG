import pygame  # pyright: ignore[reportMissingImports]
import Constantes

class arbol:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.wood = 5

    def draw(self, screen):
        pygame.draw.rect(screen, Constantes.brown, (self.x, self.y, self.size, self.size)) 