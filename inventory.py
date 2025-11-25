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
        self.inventory = [[None for _ in range(Constantes.INVENTORY_COLS)] for _ in range(Constantes.INVENTORY_ROWS)]
        self.crafting_grid = [[None for _ in range(Constantes.CRAFTING_GRID_SIZE)] for _ in range(Constantes.CRAFTING_GRID_SIZE)]
        self.dragged_item = None
        self.crafting_result = None
        self.font = pygame.font.Font(None,24)

        self.item_images = {
            'wood': os.path.join('assets', 'IMG', 'Objetos', 'madera.png'),
            'stone': os.path.join('assets', 'IMG', 'Objetos', 'mini_stone.png'), 
            'axe': os.path.join('assets', 'IMG', 'Objetos', 'axe.png') 
        }

        # definir los crafteos
        self.recipes = {
            'axe':{
                'pattern': [('wood','stone'), (None,None)],
                'result': 'axe'
            }
        }

    def add_item(self, item_name, quantity = 1):
        # Primero busca en hotbar para apilar
        for i, slot in enumerate(self.hotbar):
            if slot and slot.name == item_name:
                slot.quantity += quantity
                return True
            
        # Luego busca en inventario principal para apilar
        for row in range(Constantes.INVENTORY_ROWS):
            for col in range(Constantes.INVENTORY_COLS):
                if self.inventory[row][col] and self.inventory[row][col].name == item_name:
                    self.inventory[row][col].quantity += quantity
                    return True
        
        # buscar slot vacio en hotbar
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
            background = pygame.Surface((Constantes.width, Constantes.height), pygame.SRCALPHA)
            background.fill((0, 0, 0, 128))
            screen.blit(background, (0,0))

            self._draw_main_inventory(screen)
            # CORREGIDO: Llamada al método con el guion bajo
            self._draw_crafting_grid(screen) 
            
        # para arrastrar el item en el inventario
        if self.dragged_item:
            mouse_pos = pygame.mouse.get_pos()
            # ajustar posición del mouse
            item_pos_x = mouse_pos[0] - self.dragged_item.drag_offset[0]
            item_pos_y = mouse_pos[1] - self.dragged_item.drag_offset[1]
            screen.blit(self.dragged_item.image, (item_pos_x, item_pos_y))
            
            if self.dragged_item.quantity > 1:
                text = self.font.render(str(self.dragged_item.quantity), True, Constantes.white)
                text_rect = text.get_rect()
                # Posición de la cantidad relativa a la imagen arrastrada
                text_rect.bottomright = (item_pos_x + self.dragged_item.image.get_width() - 5, 
                                         item_pos_y + self.dragged_item.image.get_height() - 5)
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
        for i in range(Constantes.HOTBAR_SLOTS):
            x = Constantes.HOTBAR_X + (i * Constantes.SLOT_SIZE)
            y = Constantes.HOTBAR_Y 
            # fondo del slot
            pygame.draw.rect(screen, Constantes.SLOT_BORDER, (x,y, Constantes.SLOT_SIZE, Constantes.SLOT_SIZE))
            pygame.draw.rect(screen, Constantes.SLOT_COLOR, (x + 2, y + 2, Constantes.SLOT_SIZE - 4, Constantes.SLOT_SIZE- 4))
            # si existe item mostar
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

        # Verificar hotbar
        if Constantes.HOTBAR_Y <= mouse_y <= Constantes.HOTBAR_Y + Constantes.SLOT_SIZE:
            slot_index = (mouse_x - Constantes.HOTBAR_X) // Constantes.SLOT_SIZE
            if 0 <= slot_index < Constantes.HOTBAR_SLOTS:
                slot_x = Constantes.HOTBAR_X + (slot_index * Constantes.SLOT_SIZE)
                slot_y = Constantes.HOTBAR_Y
                self._handle_slot_click(button, self.hotbar, slot_index, slot_x, slot_y)
                return True
            
        if show_inventory:
        # verificar el click en el inventario principal  
            if Constantes.INVENTORY_Y <= mouse_y <= Constantes.INVENTORY_Y + (Constantes.INVENTORY_ROWS * Constantes.SLOT_SIZE):
                row = (mouse_y - Constantes.INVENTORY_Y) // Constantes.SLOT_SIZE
                col = (mouse_x -Constantes.INVENTORY_X) // Constantes.SLOT_SIZE
                if(0 <= row < Constantes.INVENTORY_ROWS and 0 <= col < Constantes.INVENTORY_COLS):
                    slot_x = Constantes.INVENTORY_X + (col * Constantes.SLOT_SIZE)
                    slot_y = Constantes.INVENTORY_Y + (row * Constantes.SLOT_SIZE)
                    self._handle_grid_slot_click(button, row, col, slot_x, slot_y)
                    return True
                
            # verificar click de cuadricula de crafteo
            if Constantes.CRAFTING_GRID_Y <= mouse_y <= Constantes.CRAFTING_GRID_Y + (Constantes.CRAFTING_GRID_SIZE * Constantes.SLOT_SIZE):
                row = (mouse_y - Constantes.CRAFTING_GRID_Y) // Constantes.SLOT_SIZE
                col = (mouse_x -Constantes.CRAFTING_GRID_X) // Constantes.SLOT_SIZE
                # CORREGIDO: Validación de la columna 'col'
                if(0 <= row < Constantes.CRAFTING_GRID_SIZE and 0 <= col < Constantes.CRAFTING_GRID_SIZE): 
                    self._handle_crafting_grid_click(button, row, col)
                    return True
                
            # verificar el resultado del crafeteo
            if(Constantes.CRAFTING_RESULT_SLOT_X <= mouse_x <= Constantes.CRAFTING_RESULT_SLOT_X + Constantes.SLOT_SIZE and 
               Constantes.CRAFTING_RESULT_SLOT_Y <= mouse_y <= Constantes.CRAFTING_RESULT_SLOT_Y + Constantes.SLOT_SIZE):
                self._handle_crafting_result_click(button)
                return True
            
        # click fuera de los slots (devolver el item arrastrado)
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
                    # Intercambiar items
                    slot_list[index], self.dragged_item = self.dragged_item, slot_list[index]
                    return
                self.dragged_item = None
            elif slot_list[index]:
                # arrastrar el item
                self.dragged_item = slot_list[index]
                slot_list[index] = None
                
                # calcular offset para el arrastre centrado
                item_rect = self.dragged_item.image.get_rect()
                item_rect.center = (slot_x + Constantes.SLOT_SIZE // 2, slot_y + Constantes.SLOT_SIZE // 2)
                self.dragged_item.drag_offset = (mouse_x - item_rect.centerx, mouse_y - item_rect.centery)

    def _handle_grid_slot_click(self, button, row, col, slot_x, slot_y):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y, = mouse_pos
        if button == 1: # click izquierdo
            if self.dragged_item:# soltar item
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                else:
                    # Intercambiar items
                    self.inventory[row][col], self.dragged_item = self.dragged_item, self.inventory[row][col]
                    return
                self.dragged_item = None
            elif self.inventory[row][col]: 
                # comenzar a arrastrar
                self.dragged_item = self.inventory[row][col]
                self.inventory[row][col] = None
                
                # calcular para el arrastre centrado del offset
                item_rect = self.dragged_item.image.get_rect()
                item_rect.center = (slot_x + Constantes.SLOT_SIZE // 2, slot_y + Constantes.SLOT_SIZE // 2)
                self.dragged_item.drag_offset = (mouse_x - item_rect.centerx, mouse_y - item_rect.centery)

    def _return_dragged_item(self):
        # intentar devolver a hotbar
        for i, slot in enumerate(self.hotbar):
            if slot is None:
                self.hotbar[i] = self.dragged_item
                self.dragged_item = None
                return
        # si no hay espacio en hotbar, intentar inventario principal
        for row in range(Constantes.INVENTORY_ROWS):
            for col in range(Constantes.INVENTORY_COLS):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                    self.dragged_item = None
                    return
                
    def _draw_crafting_grid(self, screen):
        # dibujamos las casillas del crafteo
        for row in range(Constantes.CRAFTING_GRID_SIZE):
            for col in range(Constantes.CRAFTING_GRID_SIZE):
                x = Constantes.CRAFTING_GRID_X + (col * Constantes.SLOT_SIZE)
                y = Constantes.CRAFTING_GRID_Y + (row * Constantes.SLOT_SIZE)
                # fondo
                pygame.draw.rect(screen, Constantes.SLOT_BORDER,(x,y, Constantes.SLOT_SIZE, Constantes.SLOT_SIZE))
                pygame.draw.rect(screen, Constantes.SLOT_COLOR,(x + 2, y + 2, Constantes.SLOT_SIZE - 4, Constantes.SLOT_SIZE - 4))
                # item existente dibujar
                if self.crafting_grid[row][col]:
                    self._draw_item(screen, self.crafting_grid[row][col],x,y)

        # dibujar el slot de resultado
        pygame.draw.rect(screen, Constantes.SLOT_BORDER,(Constantes.CRAFTING_RESULT_SLOT_X, Constantes.CRAFTING_RESULT_SLOT_Y, Constantes.SLOT_SIZE, Constantes.SLOT_SIZE))
        pygame.draw.rect(screen, Constantes.SLOT_COLOR,(Constantes.CRAFTING_RESULT_SLOT_X + 2, Constantes.CRAFTING_RESULT_SLOT_Y + 2, Constantes.SLOT_SIZE - 4, Constantes.SLOT_SIZE - 4))

        # resultado existe
        if self.crafting_result:
            self._draw_item(screen, self.crafting_result, Constantes.CRAFTING_RESULT_SLOT_X, Constantes.CRAFTING_RESULT_SLOT_Y)

    def _handle_crafting_grid_click(self, button, row, col):
        # Determinar las coordenadas del slot
        slot_x = Constantes.CRAFTING_GRID_X + (col * Constantes.SLOT_SIZE)
        slot_y = Constantes.CRAFTING_GRID_Y + (row * Constantes.SLOT_SIZE)
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos

        if button == 1:
            if self.dragged_item:
                if self.crafting_grid[row][col] is None:
                    self.crafting_grid[row][col] = self.dragged_item
                    self.dragged_item = None
                else:
                    # intercambiar item al craftear
                    self.crafting_grid[row][col], self.dragged_item = self.dragged_item, self.crafting_grid[row][col]
            elif self.crafting_grid[row][col]:
                # comenzar a arrastrar
                self.dragged_item = self.crafting_grid[row][col]
                self.crafting_grid[row][col] = None
                
                # calcular offset para el arrastre centrado
                item_rect = self.dragged_item.image.get_rect()
                item_rect.center = (slot_x + Constantes.SLOT_SIZE // 2, slot_y + Constantes.SLOT_SIZE // 2)
                self.dragged_item.drag_offset = (mouse_x - item_rect.centerx, mouse_y - item_rect.centery)

            # verificar despues del cambio
            self._check_recipe()

    def _handle_crafting_result_click(self, button):
        if button == 1 and self.crafting_result:
            if self.dragged_item is None:
                # Mover el resultado al arrastre
                self.dragged_item = self.crafting_result
                self.crafting_result = None
                
                # consumo de materiales
                for row in range(Constantes.CRAFTING_GRID_SIZE):
                    for col in range(Constantes.CRAFTING_GRID_SIZE):
                        if self.crafting_grid[row][col]:
                            if self.crafting_grid[row][col].quantity > 1:
                                self.crafting_grid[row][col].quantity -= 1
                            else:
                                self.crafting_grid[row][col] = None
                # Vuelve a chequear si se puede craftear el siguiente
                self._check_recipe()
            else:
                # Si ya estamos arrastrando algo, no hacemos nada con el resultado por ahora
                pass


    def _check_recipe(self):
        # obtener el patron actual (nombres de los items)
        current_pattern = []
        for row in range(Constantes.CRAFTING_GRID_SIZE):
            pattern_row = []
            for col in range(Constantes.CRAFTING_GRID_SIZE):
                item = self.crafting_grid[row][col]
                pattern_row.append(item.name if item else None)
            current_pattern.append(tuple(pattern_row))

        # verificar coincidencia de crafteo
        for recipe_name, recipe in self.recipes.items():
            matches = True
            for row in range(Constantes.CRAFTING_GRID_SIZE):
                for col in range(Constantes.CRAFTING_GRID_SIZE):
                    excepted = recipe['pattern'][row][col]
                    actual = current_pattern[row][col]
                    if excepted != actual:
                        matches = False
                        break
                if not matches:
                    break
            if matches:
                # CORREGIDO: Usamos InventoryItem para crear el resultado
                self.crafting_result = InventoryItem(recipe['result'],self.item_images[recipe['result']])
                return True
            
        # CORREGIDO: Usar el operador de asignación (=)
        self.crafting_result = None