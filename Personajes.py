import pygame
import Constantes
import os
from Constantes import *

class default:
    def __init__(self, x, y):
        self.x = x  
        self.y = y

        img_path = os.path.join('assets','IMG','Personajes', 'Player.png')
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Constantes.personaje, Constantes.personaje))
        self.size = self.image.get_width()

        self.inventory = {"wood": 0, "stone": 0}
        # Cargamos los sprites
        img_path = os.path.join('assets','IMG','Personajes','jugador.png')
        self.sprite_sheet = pygame.image.load(img_path).convert_alpha()

        # PROPIEDADES DE ANIMACIÓN
        self.frame_size = ANIMATION_FRAME
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = ANIMATION_DELAY
        self.current_state = IDLE_DOWN
        self.moving = False
        self.moving_left = False

        # cargamos todas las animaciones
        self.animations = self.load_animations()
        
        self.item_images = {
            "wood": self.load_item_images("Arbol.png"),
            "stone": self.load_item_images("mini_stone.png"),
        }

        self.energy = Constantes.MAX_ENERGY
        self.food = Constantes.MAX_FOOD
        self.thirst = Constantes.MAX_THIRST

    def load_animations(self):
        animations = {}
        for state in range(6):
            frames = []
            for frame in range(BASIC_FRAMES):
                surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                surface.blit(self.sprite_sheet, (0,0),
                             (frame * self.frame_size,
                              state * self.frame_size,
                              self.frame_size,
                              self.frame_size))
                
                if Constantes.personaje != self.frame_size:
                    surface = pygame.transform.scale(surface,(Constantes.personaje, Constantes.personaje))
                frames.append(surface)
            animations[state] = frames
        return animations

    def update_animations(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.animation_timer = current_time
            self.animation_frame = (self.animation_frame + 1) % BASIC_FRAMES

    def load_item_images(self, filename):
        path = os.path.join('assets','IMG','Objetos', filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (40,40))  

    def draw(self, screen):
        current_frame = self.animations[self.current_state][self.animation_frame]
        if self.moving_left:
            current_frame = pygame.transform.flip(current_frame, True, False)
        screen.blit(current_frame,(self.x,self.y))
        self.draw_status_bars(screen)

    def movimiento(self, dx, dy, mundo):
        self.moving = dx !=0 or dy!=0
        if self.moving:
            if dy < 0:
                self.current_state = WALK_DOWN
                self.moving_left = False
            elif dy > 0:
                self.current_state = WALK_UP
                self.moving_left = False
            elif dx > 0:
                self.current_state = WALK_RIGHT
                self.moving_left = False
            elif dx < 0:
                self.current_state = WALK_RIGHT
                self.moving_left = True
        else:
            if self.current_state == WALK_DOWN:
                self.current_state = IDLE_DOWN
            elif self.current_state == WALK_UP:
                self.current_state = IDLE_UP
            elif self.current_state == WALK_RIGHT:
                self.current_state = IDLE_RIGHT

        new_x = self.x + dx
        new_y = self.y + dy 

        for arbol in mundo.arbol:
            if self.check_collision(new_x, new_y, arbol):
                self.moving = False
                return

        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, Constantes.width - Constantes.personaje))
        self.y = max(0, min(self.y, Constantes.height - Constantes.personaje))

        self.update_animations()
        self.update_energy(-0.1)
        
    def check_collision(self, x, y, obj):
        # Factor de colisión centrado en el tronco del árbol
        collision_width = obj.size * 0.4
        collision_height = obj.size * 0.4
        collision_x = obj.x + (obj.size - collision_width) / 2
        collision_y = obj.y + (obj.size - collision_height) / 2

        return (
            x < collision_x + collision_width and
            x + Constantes.personaje > collision_x and
            y < collision_y + collision_height and
            y + Constantes.personaje > collision_y
        )

    
    def is_near(self, obj):
        return (
            abs(self.x - obj.x) <= max(self.size, obj.size) + 5 and
            abs(self.y - obj.y) <= max(self.size, obj.size) + 5
        )
    
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
        background = pygame.Surface((Constantes.width, Constantes.height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 180))
        screen.blit(background, (0, 0))

        font =pygame.font.SysFont(None, 36)
        title = font.render("Inventario", True, Constantes.white)
        screen.blit(title, (Constantes.width // 2 - title.get_width() // 2, 50))
        item_font = pygame.font.Font(None, 24)
        y_offset = 80
        for item, quantity in self.inventory.items():
            if quantity > 0:
                screen.blit(self.item_images[item], (Constantes.width // 2 - 100, y_offset))
                text = item_font.render(f"{item.capitalize()}: {quantity}", True, Constantes.white)
                screen.blit(text, (Constantes.width // 2 - 50, y_offset + 10))
                y_offset += 60

        close_text = font.render("Presiona 'I' para cerrar", True, Constantes.white)
        screen.blit(close_text, (Constantes.width // 2 - close_text.get_width() // 2, Constantes.height - 40))

    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, Constantes.MAX_ENERGY))

    def update_food(self, amount):
        self.food = max(0, min(self.food + amount, Constantes.MAX_FOOD))
    
    def update_thirst(self, amount):
        self.thirst = max(0, min(self.thirst + amount, Constantes.MAX_THIRST))

    def draw_status_bars(self, screen):
        bar_width = 100
        bar_height = 20
        x_offset = 10
        y_offset = 10

        pygame.draw.rect(screen, Constantes.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, Constantes.ENERGY_COLOR, (x_offset, y_offset, bar_width * (self.energy / Constantes.MAX_ENERGY), bar_height))

        y_offset +=15
        pygame.draw.rect(screen, Constantes.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, Constantes.FOOD_COLOR, (x_offset, y_offset, bar_width * (self.food / Constantes.MAX_FOOD), bar_height))

        y_offset +=15
        pygame.draw.rect(screen, Constantes.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, Constantes.THIRST_COLOR, (x_offset, y_offset, bar_width * (self.thirst / Constantes.MAX_THIRST), bar_height))

    def update_status(self):
        self.update_food(-0.00555)
        self.update_thirst(-0.00555)

        if self.food < Constantes.MAX_FOOD * 0.2 or self.thirst < Constantes.MAX_THIRST * 0.2:
            self.update_energy(-0.05)
        else:
            self.update_energy(0.01)
