import pygame
import Constantes
import os

class InventoryItem:
    def __init__(self, name, image_path, quantity = 1):
        self.name = name
        self.quantity = quantity
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Constantes.SLOT_SIZE - 10, Constantes.SLOT_SIZE - 10))
        self.dragging = False
        self.drag_offset = (0,0)

class Inventory:
    def __init__(self):
        self.hotbar = [None] * Constantes.HOTBAR_SLOTS
        # CORRECCIÓN: Inicialización correcta de la lista 2D
        self.inventory = [[None for _ in range(Constantes.INVENTORY_COLS)] for _ in range(Constantes.INVENTORY_ROWS)]
        self.dragged_item = None
        self.font = pygame.font.Font(None,24)

        self.item_images = {
            'wood': os.path.join('assets', 'IMG', 'Objetos', 'madera.png'),
            # Usar 'stone' para coincidir con la lógica de 'add_item' en la clase 'default'
            'stone': os.path.join('assets', 'IMG', 'Objetos', 'mini_stone.png') 
        }

    def add_item(self, item_name, quantity = 1):
        for i, slot in enumerate(self.hotbar):
            if slot and slot.name == item_name:
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
        # buscar slot vacío en inventario principal
        for row in range(Constantes.INVENTORY_ROWS):
            for col in range(Constantes.INVENTORY_COLS):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = InventoryItem(item_name, self.item_images[item_name], quantity)
                    return True
                    
        return False
    
    def draw(self, screen, show_inventory=False):
        self._draw_hotbar(screen)

        if show_inventory:
            # CORRECCIÓN: Usar Constantes.width y Constantes.height (asumiendo que son el ancho y alto de la ventana)
            background = pygame.Surface((Constantes.width, Constantes.height), pygame.SRCALPHA)
            background.fill((0, 0, 0, 128))
            screen.blit(background, (0,0))

            self._draw_main_inventory(screen)
        #para arrastrar el item en el inventario
        if self.dragged_item:
            mouse_pos = pygame.mouse.get_pos()
            # CORRECCIÓN: Corregir dragg_offset por drag_offset
            screen.blit(self.dragged_item.image, (mouse_pos[0] - self.dragged_item.drag_offset[0],mouse_pos[1] - self.dragged_item.drag_offset[1]))
            if self.dragged_item.quantity > 1:
                text = self.font.render(str(self.dragged_item.quantity), True, Constantes.white)
                text_rect = text.get_rect()
                text_rect.bottomright = (mouse_pos[0] + self.dragged_item.image.get_width()// 2- 5, mouse_pos[1] + self.dragged_item.image.get_height()// 2- 5)
                screen.blit(text, text_rect)

    def _draw_main_inventory(self, screen):
        inv_rect = pygame.Rect(Constantes.INVENTORY_X, Constantes.INVENTORY_Y, 
                               Constantes.INVENTORY_COLS * Constantes.SLOT_SIZE, 
                               Constantes.INVENTORY_ROWS * Constantes.SLOT_SIZE)
        pygame.draw.rect(screen, Constantes.SLOT_BORDER, inv_rect, 2)
        pygame.draw.rect(screen, Constantes.SLOT_COLOR, inv_rect.inflate(-4, -4))
        
        for row in range(Constantes.INVENTORY_ROWS):
            for col in range(Constantes.INVENTORY_COLS):
                x = Constantes.INVENTORY_X + (col * Constantes.SLOT_SIZE)
                y = Constantes.INVENTORY_Y + (row * Constantes.SLOT_SIZE)
                
                pygame.draw.rect(screen, Constantes.SLOT_BORDER, (x, y, Constantes.SLOT_SIZE, Constantes.SLOT_SIZE), 1)
                pygame.draw.rect(screen, Constantes.SLOT_COLOR, (x + 1, y + 1, Constantes.SLOT_SIZE - 2, Constantes.SLOT_SIZE- 2))
                
                if self.inventory[row][col]:
                    self._draw_item(screen, self.inventory[row][col], x, y)


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
                # CORRECCIÓN: Cálculo de slot_x
                self._handle_slot_click(button, self.hotbar, slot_index, Constantes.HOTBAR_X + (slot_index * Constantes.SLOT_SIZE), Constantes.HOTBAR_Y)
                return True
        #verificar el click en el inventario principal  
        if show_inventory and Constantes.INVENTORY_Y <= mouse_y <= Constantes.INVENTORY_Y + (Constantes.INVENTORY_ROWS * Constantes.SLOT_SIZE):
            row = (mouse_y - Constantes.INVENTORY_Y) // Constantes.SLOT_SIZE
            col = (mouse_x -Constantes.INVENTORY_X) // Constantes.SLOT_SIZE
            # CORRECCIÓN: La condición debe verificar row y col contra ROWS y COLS
            if(0 <= row < Constantes.INVENTORY_ROWS and 0 <= col < Constantes.INVENTORY_COLS):
                self._handle_grid_slot_click(button, row, col, Constantes.INVENTORY_X + (col * Constantes.SLOT_SIZE), Constantes.INVENTORY_Y + (row * Constantes.SLOT_SIZE))
                return True
            
        #click fuera de los slots
        if self.dragged_item and button == 1:
            self._return_dragged_item()

        return False
    
    def _handle_slot_click(self, button, slot_list, index, slot_x, slot_y):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y, = mouse_pos
        if button == 1:
            if self.dragged_item:
                if slot_list[index] is None:
                    slot_list[index] = self.dragged_item
                else:
                    slot_list[index], self.dragged_item = self.dragged_item, slot_list[index]
                    return
                self.dragged_item = None
            elif slot_list[index]:
                #arrastrar el item
                self.dragged_item = slot_list[index]
                slot_list[index] = None
                #calcular offset para el arrastre centrado
                item_rect = self.dragged_item.image.get_rect()
                item_rect.center = (slot_x + Constantes.SLOT_SIZE // 2, slot_y + Constantes.SLOT_SIZE // 2)
                self.dragged_item.drag_offset = (mouse_x - item_rect.centerx, mouse_y - item_rect.centery)

    def _handle_grid_slot_click(self, button, row, col, slot_x, slot_y):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y, = mouse_pos
        if button == 1: #click izquierdo
            if self.dragged_item:#soltar item
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                else:
                    self.inventory[row][col], self.dragged_item = self.dragged_item, self.inventory[row][col]
                    return
                self.dragged_item = None
            # CORRECCIÓN: Corregir 'Inventory' por 'inventory'
            elif self.inventory[row][col]: 
                #comenzar a arrastrar
                self.dragged_item = self.inventory[row][col]
                self.inventory[row][col] = None
                #calcular para el arrastre centrado del offset
                # CORRECCIÓN: Corregir 'item.get_rect()' por 'image.get_rect()' y 'drag.offset' por 'drag_offset'
                item_rect = self.dragged_item.image.get_rect()
                item_rect.center = (slot_x + Constantes.SLOT_SIZE // 2, slot_y + Constantes.SLOT_SIZE // 2)
                self.dragged_item.drag_offset = (mouse_x - item_rect.centerx, mouse_y - item_rect.centery)

    def _return_dragged_item(self):
        for i, slot in enumerate(self.hotbar):
            if slot is None:
                self.hotbar[i] = self.dragged_item
                self.dragged_item = None
                return
        #si no hay espacio
        for row in range(Constantes.INVENTORY_ROWS):
            for col in range(Constantes.INVENTORY_COLS):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                    self.dragged_item = None
                    return