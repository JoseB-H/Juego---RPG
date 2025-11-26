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

        #cargar spirte del hacha
        self.action_sprite_sheet = pygame.image.load(os.path.join('assets','IMG','Personajes','Player_Actions.png')).convert_alpha()

        #agregar propiedades del hacha
        self.is_talar = False
        self.talar_timer = 0
        self.talar_frame = 0

        #cargar animations del hacha
        self.axe_animations = self.load_axe_animations()

    def load_animations(self):
        """Carga y escala las animaciones normales (idle/walk) a Constantes.personaje."""
        animations = {}
        for state in range(6):
            frames = []
            for frame in range(BASIC_FRAMES):
                temp_surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                temp_surface.blit(self.sprite_sheet, (0,0),
                                 (frame * self.frame_size,
                                  state * self.frame_size,
                                  self.frame_size,
                                  self.frame_size))
                
                surface = pygame.Surface((Constantes.personaje, Constantes.personaje), pygame.SRCALPHA)
                scale_temp = pygame.transform.scale(temp_surface, (Constantes.personaje, Constantes.personaje))
                surface.blit(scale_temp, (0,0))
                frames.append(surface)
            animations[state] = frames
        return animations

    def load_axe_animations(self):
        animations = []
        # Definimos el orden de las filas del sprite sheet de acción: [Right, Down, Up]
        rows_to_load = [3, 4, 5]
        target_size = Constantes.personaje # 70

        for row in rows_to_load:
            frames = []
            for frame in range(AXE_FRAMES):
                temp_surface = pygame.Surface((Constantes.ACTION_FRAME_SIZE, Constantes.ACTION_FRAME_SIZE), pygame.SRCALPHA)
                x = (frame % AXE_COLS) * Constantes.ACTION_FRAME_SIZE
                frame_rect = pygame.Rect(x, row * Constantes.ACTION_FRAME_SIZE, Constantes.ACTION_FRAME_SIZE, Constantes.ACTION_FRAME_SIZE)
                temp_surface.blit(self.action_sprite_sheet, (0,0), frame_rect)
                final_surface = pygame.Surface((target_size, target_size), pygame.SRCALPHA)
                scaled_temp = pygame.transform.scale(temp_surface, (target_size, target_size))
                final_surface.blit(scaled_temp, (0,0)) 

                frames.append(final_surface)
            animations.append(frames)
        return animations

    def update_animations(self):
        current_time = pygame.time.get_ticks()

        if self.is_talar:
            if current_time - self.talar_timer > AXE_ANIMATION_DELAY:
                self.talar_timer = current_time
                self.talar_frame = (self.talar_frame + 1) % AXE_FRAMES
                if self.talar_frame == 0:
                    self.is_talar = False
        else:
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

        current_frame = None

        if self.is_talar:
            if self.current_state in [IDLE_RIGHT, WALK_RIGHT]:
                current_frame = self.axe_animations[0][self.talar_frame] # Fila 3 (Derecha/Izquierda)
            elif self.current_state in [IDLE_DOWN, WALK_DOWN]:
                current_frame = self.axe_animations[1][self.talar_frame] # Fila 4 (Abajo)
            elif self.current_state in [IDLE_UP, WALK_UP]:
                current_frame = self.axe_animations[2][self.talar_frame] # Fila 5 (Arriba)

            if current_frame and self.moving_left:
                current_frame = pygame.transform.flip(current_frame, True, False)
        else:
            # Animación normal
            current_frame = self.animations[self.current_state][self.animation_frame]
            if self.moving_left:
                current_frame = pygame.transform.flip(current_frame, True, False)

        if current_frame:
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
                self.current_state = WALK_UP # Moviendo hacia arriba (y disminuye)
                self.moving_left = False
            elif dy > 0:
                self.current_state = WALK_DOWN # Moviendo hacia abajo (y aumenta)
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
        for tree in mundo.trees:
            if self.is_near(tree):
                has_axe = self.inventory.has_axe_equipped()
                if has_axe:
                    self.is_talar = True
                    self.talar_timer = pygame.time.get_ticks()
                    self.talar_frame = 0
                
                wood_collected = tree.talar(with_axe=has_axe)
                if wood_collected > 0:
                    for _ in range(wood_collected):
                        self.inventory.add_item('wood')
                    print(f"recogiendo {wood_collected} madera")
                
                if tree.is_deleted(): 
                    for chunk in mundo.active_chunk.values():
                        if tree in chunk.trees:
                            chunk.trees.remove(tree)
                            break
                    print("Árbol talado y eliminado del chunk.")
                        
                break

        # Recogiendo piedras
        for stone in mundo.mini_stone:
            if self.is_near(stone):
                if stone.collect() > 0:
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
            screen.blit(close_text, (Constantes.width // 2 - close_text.get_width() // 2, Constantes.height -40))

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
        #RECUPERE STAMINA SI NO ESTA CORRIENDO Y NO SE ESTA MIVIENDO
        if not self.is_runing and not self.moving:
            self.update_stamina(STAMINA_INCREASE_RATE)