import os
import pygame
import Constantes

class arbol:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        path_tree = os.path.join('assets','IMG','Objetos','Arbol.png')
        self.image = pygame.image.load(path_tree).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Constantes.Tree, Constantes.Tree))
        self.size = self.image.get_width()
        self.wood = 5 # Inicia con 5 de madera

    def draw(self, screen, camara_x, camara_y):
        screen_x = self.x - camara_x
        screen_y = self.y - camara_y
        if -self.size < screen_x < Constantes.width and -self.size < screen_y < Constantes.height:
            screen.blit(self.image, (screen_x, screen_y))

    def talar(self, with_axe=False):
        """
        Reduce la madera del árbol y retorna la cantidad recolectada.
        Con hacha: 3 de daño. Sin hacha: 1 de daño.
        """
        if self.wood <= 0:
            return 0 # Devuelve 0 si ya está agotado
        damage = 1
        if with_axe:
            damage = 3 # Daño del hacha: asegura 2 golpes para 5 de madera
        # La cantidad recolectada es el mínimo entre el daño y la madera restante
        wood_collected = min(damage, self.wood)
        # Aplicamos el daño
        self.wood -= wood_collected
        # Devolvemos la cantidad exacta de madera
        return wood_collected

    def is_deleted(self):
        return self.wood <= 0

class Mini_stone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stone = 1
        path_stone = os.path.join('assets','IMG','Objetos','mini_stone.png')
        self.image = pygame.image.load(path_stone).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Constantes.smallStone, Constantes.smallStone))
        self.size = self.image.get_width()

    def draw(self, screen, camara_x, camara_y):
        screen_x = self.x - camara_x
        screen_y = self.y - camara_y
        if -self.size < screen_x < Constantes.width and -self.size < screen_y < Constantes.height:
            screen.blit(self.image, (screen_x, screen_y))

    def collect(self):
        if self.stone > 0:
            self.stone -= 1
            return True
        return False

    def is_deleted(self):
        return self.stone <= 0