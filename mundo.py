import os
import random
import pygame
import Constantes
from Elementos import arbol, Mini_stone
from pygame import Surface

class mundoChunk:
    def __init__(self, x, y, width, height):
        self.chunk_size = Constantes.width
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Semilla del chunk para reproducibilidad
        chunk_seed = hash(f"{x},{y}")
        old_state = random.getstate()
        random.seed(chunk_seed)

        # Árboles
        self.trees = [
            arbol(
                self.x + random.randint(0, width - Constantes.Tree),
                self.y + random.randint(0, height - Constantes.Tree)
            ) for _ in range(10)
        ]

        # Piedras
        self.mini_stone = [
            Mini_stone(
                self.x + random.randint(0, width - Constantes.smallStone),
                self.y + random.randint(0, height - Constantes.smallStone)
            ) for _ in range(5)
        ]

        random.setstate(old_state)

    def draw(self, screen, cesped, camara_x, camara_y):
        # Dibujar césped
        start_x = max(0, camara_x - self.x - Constantes.cesped)//Constantes.cesped
        end_x = min(self.width // Constantes.cesped + 1, (camara_x + Constantes.width - self.x + Constantes.cesped)//Constantes.cesped + 1)
        start_y = max(0, camara_y - self.y - Constantes.cesped)//Constantes.cesped
        end_y = min(self.height // Constantes.cesped + 1, (camara_y + Constantes.height - self.y + Constantes.cesped)//Constantes.cesped + 1)

        for y in range(int(start_y), int(end_y)):
            for x in range(int(start_x), int(end_x)):
                screen_x = self.x + x * Constantes.cesped - camara_x
                screen_y = self.y + y * Constantes.cesped - camara_y
                screen.blit(cesped, (screen_x, screen_y))

        # Dibujar piedras
        for stone in self.mini_stone:
            if not stone.is_deleted():
                stone.draw(screen, camara_x, camara_y)

        # Dibujar árboles
        for tree in self.trees:
            if not tree.is_deleted():
                tree.draw(screen, camara_x, camara_y)


class mundo:
    def __init__(self, width, height):
        self.view_width = width
        self.view_height = height
        self.chunk_size = Constantes.width
        self.active_chunk = {}

        cesped_path = os.path.join('assets','IMG','Objetos','cesped.png')
        self.cesped = pygame.image.load(cesped_path).convert()
        self.cesped = pygame.transform.scale(self.cesped, (Constantes.cesped, Constantes.cesped))

        self.current_time = Constantes.MORNING_TIME
        self.day_overlay = Surface((width, height))
        self.day_overlay.set_alpha(0)

        # Generar chunk inicial y alrededores
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                self.generar_chunk(dx, dy)

    def get_chunk_key(self, x, y):
        return (x // self.chunk_size, y // self.chunk_size)

    def generar_chunk(self, chunk_x, chunk_y):
        key = (chunk_x, chunk_y)
        if key not in self.active_chunk:
            x = chunk_x * self.chunk_size
            y = chunk_y * self.chunk_size
            self.active_chunk[key] = mundoChunk(x, y, self.chunk_size, self.chunk_size)

    def update_chunks(self, player_x, player_y):
        current_chunk = self.get_chunk_key(player_x, player_y)

        for dx in [-2,-1,0,1,2]:
            for dy in [-2,-1,0,1,2]:
                self.generar_chunk(current_chunk[0]+dx, current_chunk[1]+dy)

        # Eliminar chunks lejanos
        to_remove = []
        for key in self.active_chunk.keys():
            if abs(key[0]-current_chunk[0])>2 or abs(key[1]-current_chunk[1])>2:
                to_remove.append(key)
        for key in to_remove:
            del self.active_chunk[key]

    def draw(self, screen, camara_x=0, camara_y=0):
        for chunk in self.active_chunk.values():
            chunk.draw(screen, self.cesped, camara_x, camara_y)
        screen.blit(self.day_overlay, (0, 0))

    def update_time(self, dt):
        self.current_time = (self.current_time + dt) % Constantes.DAY_LENGTH
        if Constantes.DAWN_TIME <= self.current_time < Constantes.MORNING_TIME:
            self.day_overlay.fill(Constantes.DAWN_DUSK_COLOR)
            progress = (self.current_time - Constantes.DAWN_TIME) / (Constantes.MORNING_TIME - Constantes.DAWN_TIME)
            alpha = int(Constantes.MAX_DARKNESS * (1 - progress))
        elif Constantes.MORNING_TIME <= self.current_time < Constantes.DUSK_TIME:
            self.day_overlay.fill(Constantes.DAY_COLOR)
            alpha = 0
        elif Constantes.DUSK_TIME <= self.current_time < Constantes.MIDNIGHT_TIME:
            self.day_overlay.fill(Constantes.DAWN_DUSK_COLOR)
            progress = (self.current_time - Constantes.DUSK_TIME) / (Constantes.MIDNIGHT_TIME - Constantes.DUSK_TIME)
            alpha = int(Constantes.MAX_DARKNESS * progress)
        else:
            self.day_overlay.fill(Constantes.NIGHT_COLOR)
            alpha = Constantes.MAX_DARKNESS
        self.day_overlay.set_alpha(alpha)

    @property
    def trees(self):
        all_trees = []
        for chunk in self.active_chunk.values():
            all_trees.extend(chunk.trees)
        return all_trees

    @property
    def mini_stone(self):
        all_stone = []
        for chunk in self.active_chunk.values():
            all_stone.extend(chunk.mini_stone)
        return all_stone
