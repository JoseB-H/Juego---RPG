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
        self.inventory = {"wood": 0, "stone": 0}

    def draw(self, screen):   # <-- antes se llamaba mover
        screen.blit( self.image, (self.x, self.y))

    def movimiento(self, dx, dy, mundo):
        new_x = self.x + dx
        new_y = self.y + dy 

        for arbol in mundo.arbol:
            if self.check_collision(new_x, new_y, arbol):
                return

        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, Constantes.width - self.size))
        self.y = max(0, min(self.y, Constantes.height - self.size))
    
    def check_collision(self, x, y, obj):
        return (x < obj.x + obj.size*.75 and x + self.size > obj.x and y < obj.y + obj.size*.75 and y + self.size > obj.y)
    
    def is_near(self, obj): 
        return (abs(self.x - obj.x) <= max(self.size, obj.size)+5 and abs(self.y - obj.y) <= max(self.size, obj.size)+5)
    
    def interact(self, mundo):
        for arbol in mundo.arbol:
            if self.is_near(arbol):
                if arbol.talar():
                    self.inventory['wood'] += 1
                    if arbol.wood == 0:
                        mundo.arbol.remove(arbol)
                    print("talando arbol")

        for piedra in mundo.mini_stone:
            if self.is_near(piedra):
                self.inventory['stone'] += piedra.stone
                mundo.mini_stone.remove(piedra)
                print("recogiendo piedra")