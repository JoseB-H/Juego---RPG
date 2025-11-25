import os
import pygame
import Constantes
from Constantes import *
from inventory import Inventory

class default:
    def __init__(self, x, y):
        self.x = x  
        self.y = y

        img_path = os.path.join('assets','IMG','Personajes', 'Player.png')
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Constantes.personaje, Constantes.personaje))
        self.size = self.image.get_width()

        self.inventory = Inventory()

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
        self.is_runing = False

        # cargamos todas las animaciones
        self.animations = self.load_animations()
        
        self.item_images = {
            "wood": self.load_item_images("madera.png"),
            "stone": self.load_item_images("mini_stone.png"),
        }

        self.energy = Constantes.MAX_ENERGY
        self.food = Constantes.MAX_FOOD
        self.thirst = Constantes.MAX_THIRST
        self.stamina = Constantes.MAX_STAMINA

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
            #AJUSTAR LA VELOCIDAD DE LA NIMACION
            animation_speed = RUNNING_ANIMATION_DELAY if self.is_runing else ANIMATION_DELAY
            if current_time - self.animation_timer > animation_speed:
                self.animation_timer = current_time
                self.animation_frame = (self.animation_frame + 1) % BASIC_FRAMES

    def load_item_images(self, filename):
        path = os.path.join('assets','IMG','Objetos', filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (40,40))  

    def draw(self, screen, camara_x, camara_y):
        screen_x = self.x - camara_x
        screen_y = self.y - camara_y

        current_frame = self.animations[self.current_state][self.animation_frame]
        if self.moving_left:
            current_frame = pygame.transform.flip(current_frame, True, False)
        screen.blit(current_frame,(screen_x,screen_y))
        self.draw_status_bars(screen)

    def movimiento(self, dx, dy, mundo):
        self.moving = dx != 0 or dy != 0
        if self.moving:
            #ajustar la velocidad
            speed_multiplier = RUN_SPEED if self.is_runing and self.stamina > 0 else WALK_SPEED
            dx *= speed_multiplier / WALK_SPEED
            dy *= speed_multiplier / WALK_SPEED
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

        for tree_obj in mundo.trees:
            if self.check_collision(new_x, new_y, tree_obj):
                self.moving = False
                return

        self.x += dx
        self.y += dy
        self.update_animations()
        
        if self.moving:
            if self.is_runing and self.stamina > 0:
                self.update_stamina(-STAMINA_DECREASE_RATE)
                self.update_energy(-MOVEMENT_ENERGY_COST)
            else:
                self.update_energy(-MOVEMENT_ENERGY_COST)
                if not self.moving:
                    self.update.stamina(STAMINA_INCREASE_RATE)

    def check_collision(self, x, y, obj):
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
        # Talando arboles
        for tree_obj in mundo.trees:
            if self.is_near(tree_obj):
                if tree_obj.talar():
                    self.inventory.add_item('wood')
                    if tree_obj.wood == 0:
                        for chunk in mundo.active_chunk.values():
                            if tree_obj in chunk.trees:
                                chunk.trees.remove(tree_obj)
                                break
                    print("talando arbol")

        # Recogiendo piedras
        for stone in mundo.mini_stone:
            if self.is_near(stone):
                self.inventory.add_item('stone')
                for chunk in mundo.active_chunk.values():
                    if stone in chunk.mini_stone:
                        chunk.mini_stone.remove(stone)
                        break
                print("recogiendo piedra")


    def draw_inventory(self, screen, show_inventory=False):
        #dibujamos el inventario
        self.inventory.draw(screen, show_inventory)
        #texto abrir y cerrar
        if show_inventory:
            font = pygame.font.Font(None,24)
            close_text = font.render("Press 'I' cerrar inventory", True, Constantes.white)
            screen.blit(close_text, (Constantes.white // 2 - close_text.get_width() // 2, Constantes.height -40))

    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, Constantes.MAX_ENERGY))

    def update_food(self, amount):
        self.food = max(0, min(self.food + amount, Constantes.MAX_FOOD))

    def update_thirst(self, amount):
        self.thirst = max(0, min(self.thirst + amount, Constantes.MAX_THIRST))

    def update_stamina(self, amount):
        self.stamina = max(0, min(self.stamina + amount, Constantes.MAX_STAMINA))

    def draw_status_bars(self, screen):
        bar_width = 100
        bar_height = 20
        x_offset = 10
        y_offset = 10

        pygame.draw.rect(screen, Constantes.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, Constantes.ENERGY_COLOR, (x_offset, y_offset, bar_width * (self.energy / Constantes.MAX_ENERGY), bar_height))

        y_offset += 15
        pygame.draw.rect(screen, Constantes.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, Constantes.FOOD_COLOR, (x_offset, y_offset, bar_width * (self.food / Constantes.MAX_FOOD), bar_height))

        y_offset += 15
        pygame.draw.rect(screen, Constantes.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, Constantes.THIRST_COLOR, (x_offset, y_offset, bar_width * (self.thirst / Constantes.MAX_THIRST), bar_height))

        y_offset += 15
        pygame.draw.rect(screen, Constantes.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, Constantes.STAMINA_COLOR, (x_offset, y_offset, bar_width * (self.stamina / Constantes.MAX_STAMINA), bar_height))

    def update_status(self):
        #APLICAMOS MULTIPLICADORES
        food_rate = FOOD_DECREASE_RATE * (RUN_FOOD_DECREASE_MULTIPLIER if self.is_runing else 1)
        thirst_rate = THIRST_DECREASE_RATE * (RUN_THIRST_DECREASE_MULTIPLIER if self.is_runing else 1)

        self.update_food(-Constantes.FOOD_DECREASE_RATE)
        self.update_thirst(-Constantes.THIRST_DECREASE_RATE)

        if self.food < Constantes.MAX_FOOD * 0.2 or self.thirst < Constantes.MAX_THIRST * 0.2:
            self.update_energy(-Constantes.ENERGY_DECREASE_RATE)
        else:
            self.update_energy(Constantes.ENERGY_INCREASE_RATE)
        #RECUPERE STAMINA SI NO ESTA CORRIENDO
        if not self.is_runing:
            self.update_stamina(STAMINA_INCREASE_RATE)
