import os
import random
import pygame # pyright: ignore[reportMissingImports]
import Constantes
from Elementos import arbol, Mini_stone
from pygame import Surface

class mundo:
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.arbol = [arbol(random.randint(0,width-Constantes.Tree),random.randint(0,height-Constantes.Tree)) for _ in range(10)] # rango de 10 arboles
        self.mini_stone = [Mini_stone(random.randint(0, width - Constantes.smallStone),random.randint(0, height - Constantes.smallStone)) for _ in range(20)]
        
        cesped_path = os.path.join('assets','IMG','Objetos','cesped.png')
        self.cesped = pygame.image.load(cesped_path).convert()
        self.cesped = pygame.transform.scale(self.cesped, (Constantes.cesped, Constantes.cesped))

    #Sistema de dia / noche
        self.current_time = Constantes.MORNING_TIME
        self.day_overlay = Surface((width, height))
        self.day_overlay.set_alpha(0)

    def draw(self,screen):
        for y in range(0, self.height, Constantes.cesped):
            for x in range(0, self.width, Constantes.cesped):
                screen.blit(self.cesped, (x, y))

        for arbol in self.arbol:
            arbol.draw(screen)

        for mini_stone in self.mini_stone:
            mini_stone.draw(screen)

        #aplicamos los overlay dia y noche
        screen.blit(self.day_overlay, (0, 0))

    def update_time(self, dt):
        self.current_time = (self.current_time + dt) % Constantes.DAY_LENGTH

        if Constantes.DAWN_TIME <= self.current_time < Constantes.MORNING_TIME:
            # Amanecer
            self.day_overlay.fill(Constantes.DAWN_DUSK_COLOR)
            progress = (self.current_time - Constantes.DAWN_TIME) / (Constantes.MORNING_TIME - Constantes.DAWN_TIME)
            alpha = int(Constantes.MAX_DARKNESS * (1 - progress))

        elif Constantes.MORNING_TIME <= self.current_time < Constantes.DUSK_TIME:
            # Día
            self.day_overlay.fill(Constantes.DAY_COLOR)
            alpha = 0

        elif Constantes.DUSK_TIME <= self.current_time < Constantes.MIDNIGHT_TIME:
            # Atardecer
            self.day_overlay.fill(Constantes.DAWN_DUSK_COLOR)
            progress = (self.current_time - Constantes.DUSK_TIME) / (Constantes.MIDNIGHT_TIME - Constantes.DUSK_TIME)
            alpha = int(Constantes.MAX_DARKNESS * progress)

        else:
            # Noche
            self.day_overlay.fill(Constantes.NIGHT_COLOR)
            alpha = Constantes.MAX_DARKNESS

        self.day_overlay.set_alpha(alpha)

    def draw_inventory(self, screen, Personajes):
        font: pygame.font.Font = pygame.font.SysFont('Arial', 24)
        instructions_text = font.render("Press 'I' to open Inventory", True, Constantes.white)
        screen.blit(instructions_text, (10, 10))