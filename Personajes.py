import pygame # pyright: ignore[reportMissingImports]
import Constantes

class default:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tamaño = 20
        self.inventory = {"wood ": 0, "stone ": 0}

    def draw(self, screen):   # <-- antes se llamaba mover
        pygame.draw.rect(screen, Constantes.blue, (self.x, self.y, self.tamaño, self.tamaño))

    def movimiento(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, Constantes.width - self.tamaño))
        self.y = max(0, min(self.y, Constantes.height - self.tamaño))
    