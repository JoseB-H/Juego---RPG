import pygame # pyright: ignore[reportMissingImports]
import Constantes
import os # para trabajar con archivos

class default:
    def __init__(self, x, y):
        self.x = x  
        self.y = y
        img_path = os.path.join('assets','IMG','Personajes', 'Player.png')
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Constantes.personaje, Constantes.personaje))
        self.size = self.image.get_width()
        self.inventory = {"wood ": 0, "stone ": 0}

    def draw(self, screen):   # <-- antes se llamaba mover
        screen.blit( self.image, (self.x, self.y))

    def movimiento(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, Constantes.width - self.size))
        self.y = max(0, min(self.y, Constantes.height - self.size))
    