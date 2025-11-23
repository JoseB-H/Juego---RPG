import pygame
import Constantes
import os

class InventoryItem:
    def __init__(self, name, image_path, quantity = 1):
        self.name = name
        self.quantity = quantity
        self.image = pygame.image.load(image_path).convert_alpha
        self.image = pygame.transform.scale(self.image, (Constantes.SLOT_SIZE - 10, Constantes.SLOT_SIZE - 10))
        self.dragging = False
        self.drag_offset = (0,0)

class Inventory:
    def __init__(self):
        self.hotbar = [None] * Constantes.HOTBAR_SLOTS
        self.inventory = [[None for _ in range(Constantes.INVENTORY_COLS)] for _ in range ]
        self.dragged_item = None
        self.font = pygame.font.Font(None,24)

        self.item_images = {
            'wood': os.path.join('assets', 'IMG', 'Objetos', 'madera.png'),
            'mini_stone': os.path.join('assets', 'IMG', 'Objetos', 'mini_stone.png')
        }

    def add_item(self, item_name, quantity = 1):
        for i, slot in enumerate(self.hotbar):
            if slot and slot_name == item_name:
                slot.quantity += quantity
                return True
            
        for row in range(Constantes.INVENTORY_ROWS):
            for col in range(Constantes.INVENTORY_COLS):
                if self.inventory[row][col] and self.inventory[row][col].name == item_name:
                    self.inventory[row][col].quantity += quantity
                    return True
        #buscar slot vacio       
        for i, slot in enumerate(self.hotbar):
            if slot is None:
                self.hotbar[i] = InventoryItem(item_name, self.item_images[item_name], quantity)
                return True
        return False
    
    def draw(self, screen, show_inventory=False):
        self._draw_hotbar(screen)

        if show_inventory:
            background = pygame.surface((Constantes.white, Constantes.height), pygame.SRCALPHA)
            background.fill((0, 0, 0, 128))
            screen.blit(background, (0,0))

            self._draw_main_inventory(screen)
        #para arastrar el item en el inventario xd
        if self.dragged_item:
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(self.dragged_item.image, (mouse_pos[0] - self.dragged_item.dragg_offset[0],mouse_pos[1] - self.dragged_item.dragg_offset[1]))
            if self.dragged_item.quantity > 1:
                text = self.font.render(str(self.dragged_item.quantity), True, Constantes.white)
                text_rect = text.get_rect()
                text_rect.bottomright = (mouse_pos[0] + self.dragged_item.image.get_width()// 2- 5, mouse_pos[1] + self.dragged_item.image.get_height()// 2- 5)
                screen.blit(text, text_rect)

    def _draw_hotbar (self, screen):
        for i  in range(Constantes.HOTBAR_SLOTS):
            x = Constantes.HOTBAR_X + (i * Constantes.SLOT_SIZE)
            y = Constantes.HOTBAR_Y 
            #fondo del slot
            pygame.draw.rect(screen, Constantes.SLOT_BORDER, (x,y, Constantes.SLOT_SIZE, Constantes.SLOT_SIZE))
            pygame.draw.rect(screen, Constantes.SLOT_COLOR, (x + 2, y + 2, Constantes.SLOT_SIZE - 4, Constantes.SLOT_SIZE- 4))
            #si existe item mostar
            if self.hotbar[i]:
                self._draw_item(screen, self.hotbar[i], x, y)

    def _draw_item(self, screen, item, x, y):
        item_x = x + (Constantes.SLOT_SIZE - item.image.get_width()) // 2
        item_y = y + (Constantes.SLOT_SIZE - item.image.get_height()) // 2
        screen.blit(item.image, (item_x, item_y))

        if item.quantity > 1:
            text = self.font.render(str(item.quantity), True, Constantes.white)
            text_rect = text.get_rect()
            text_rect.bottomright = (x + Constantes.SLOT_SIZE - 5, y + Constantes.SLOT_SIZE - 5)
            screen.blit(text, text_rect)

    def handle_click(self, pos, button, show_inventory = False):
        mouse_x , mouse_y = pos

        if Constantes.HOTBAR_Y <= mouse_y <= Constantes.HOTBAR_Y + Constantes.SLOT_SIZE:
            slot_index = (mouse_x - Constantes.HOTBAR_X) // Constantes.SLOT_SIZE
            if 0 <= slot_index < Constantes.HOTBAR_SLOTS:
                self._handle_slot_click(button, self.hotbar, slot_index, Constantes.HOTBAR_SLOTS + (slot_index * Constantes.SLOT_SIZE), Constantes.HOTBAR_Y)
                return True
            
        if show_inventory and Constantes.INVENTORY_Y <= mouse_y <= Constantes.INVENTORY_Y + (Constantes.INVENTORY_ROWS * Constantes.SLOT_SIZE)