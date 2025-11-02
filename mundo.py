import os
import random
import pygame # pyright: ignore[reportMissingImports]
import Constantes
from Elementos import arbol, Mini_stone

class mundo:
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.arbol = [arbol(random.randint(0,width-Constantes.Tree),random.randint(0,height-Constantes.Tree)) for _ in range(10)] # rango de 10 arboles
        self.mini_stone = [Mini_stone(random.randint(0, width - Constantes.smallStone),random.randint(0, height - Constantes.smallStone)) for _ in range(20)]
        
        cesped_path = os.path.join('assets','IMG','Objetos','cesped.png')
        self.cesped = pygame.image.load(cesped_path).convert()
        self.cesped = pygame.transform.scale(self.cesped, (Constantes.cesped, Constantes.cesped))

    def draw(self,screen):
        for y in range(0, self.height, Constantes.cesped):
            for x in range(0, self.width, Constantes.cesped):
                screen.blit(self.cesped, (x, y))

        for arbol in self.arbol:
            arbol.draw(screen)

        for mini_stone in self.mini_stone:
            mini_stone.draw(screen)

    def draw_inventory(self, screen, Personajes):
        font: pygame.font.Font = pygame.font.SysFont('Arial', 40)
        wood_text = font.render(f"Wood: {Personajes.inventory['wood']}", True, Constantes.white)
        stone_text = font.render(f"Stone: {Personajes.inventory['stone']}", True, Constantes.white)
        screen.blit(wood_text, (10, 10))
        screen.blit(stone_text, (10, 50))