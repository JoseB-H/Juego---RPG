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

        self.item_images = {
            "wood": self.load_item_image("madera.png"),
            "stone": self.load_item_image("mini_stone.png")
        }
        self.energy = Constantes.MAX_ENERGY
        self.food = Constantes.MAX_FOOD
        self.thirst = Constantes.MAX_THIRST

    def load_item_image(self,filename):
            path = os.path.join('assets','IMG','Objetos', filename)
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (40, 40))


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

        #gasto de energia, comida y sed
        self.update_energy(-0.1)
    
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

    def draw_inventory(self, screen):
            backgraund = pygame.Surface((Constantes.width, Constantes.height), pygame.SRCALPHA)
            backgraund.fill((0, 0, 0, 180))  # Fondo semitransparente
            screen.blit(backgraund, (0, 0))

            font = pygame.font.Font(None, 36)
            title = font.render("Inventario", True, Constantes.white)
            screen.blit(title, (Constantes.width // 2 - title.get_width() // 2, 20))
            item_font = pygame.font.Font(None, 24)
            y_offset = 80
            for item, quantity in self.inventory.items():
                if quantity > 0:
                    screen.blit(self.item_images[item], (Constantes.width // 2 - 60, y_offset))
                    text = item_font.render(f"{item.capitalize()}: {quantity}", True, Constantes.white)
                    screen.blit(text, (Constantes.width // 2 +   10, y_offset + 10))
                    y_offset += 50

            close_text = item_font.render("Presiona 'I' para cerrar el inventario", True, Constantes.white)
            screen.blit(close_text, (Constantes.width // 2 - close_text.get_width() // 2, Constantes.height - 40))

    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, Constantes.MAX_ENERGY))

    def update_food(self, amount):
        self.food = max(0, min(self.food + amount, Constantes.MAX_FOOD))

    def update_thirst(self, amount):
        self.thirst = max(0, min(self.thirst + amount, Constantes.MAX_THIRST))  
 
    def draw_status_bar(self, screen):
        bar_width = 100
        bar_height = 20
        x_offset = 10
        y_offset = 10

    # Energy Bar
        pygame.draw.rect(screen, Constantes.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        
        pygame.draw.rect(screen, Constantes.ENERGY_COLOR,(x_offset, y_offset,bar_width * (self.energy / Constantes.MAX_ENERGY), bar_height))