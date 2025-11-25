import pygame  
import sys
import Constantes
from Personajes import default
from mundo import mundo

pygame.init()

ventana = pygame.display.set_mode((Constantes.width, Constantes.height))
pygame.display.set_caption("Menu")

def main():
    clock = pygame.time.Clock()
    game_world = mundo(Constantes.width, Constantes.height)  
    personaje = default(Constantes.width // 2, Constantes.height // 2)
    show_inventory = False
    status_update_timer = 0

    camara_x = 0
    camara_y = 0

    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    personaje.interact(game_world)
                if event.key == pygame.K_i:
                    show_inventory = not show_inventory
                if event.key == pygame.K_f:
                    personaje.update_food(20)
                if event.key == pygame.K_t:
                    personaje.update_thirst(20)

            if event.type == pygame.MOUSEBUTTONDOWN:
                personaje.inventory.handle_click(pygame.mouse.get_pos(), event.button, show_inventory)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                personaje.inventory.handle_click(pygame.mouse.get_pos(), event.button, show_inventory)

        # Movimientos
        dx = dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 5
            
        #PARA CORRER
        personaje.is_runing = keys[pygame.K_LSHIFT] and personaje.stamina > 0
        personaje.movimiento(dx,dy,game_world)
        #ACTULIZA LOS CHUNKS BASADOS EN LE PERSONJAE
        game_world.update_chunks(personaje.x, personaje.y)
        #CAMARA SIGUE A PERSONAJE XD
        camara_x = personaje.x - Constantes.width // 2
        camara_y = personaje.y - Constantes.height // 2

        # Actualizar tiempo del mundo
        game_world.update_time(dt)

        status_update_timer += dt
        personaje.update_status()
        if status_update_timer >= Constantes.STATUS_UPDATE_INTERVAL:
            personaje.update_food(-1)
            personaje.update_thirst(-1)
            status_update_timer = 0

        if personaje.energy <= 0 or personaje.food <= 0 or personaje.thirst <= 0:
            print("Game Over")
            pygame.quit()
            sys.exit()

        ventana.fill((0,0,0))
        
        # Dibujar mundo y personaje
        game_world.draw(ventana, camara_x, camara_y)  
        personaje.draw(ventana, camara_x, camara_y)  

        #siempre visible (Ahora usando la función de la clase Inventory)
        personaje.inventory.draw(ventana, show_inventory)
        
        font = pygame.font.SysFont('Arial', 24)

        # Usamos int() para mostrar solo la parte entera.
        energy_text = font.render(f"Energía: {int(personaje.energy)}", True, Constantes.white)
        food_text = font.render(f"Comida: {int(personaje.food)}", True, Constantes.white)
        thirst_text = font.render(f"Sed: {int(personaje.thirst)}", True, Constantes.white)
        stamina_text = font.render(f"Stamina: {int(personaje.stamina)}", True, Constantes.white)
        
        MS_PER_DAY = Constantes.DAY_LENGTH
        # Hay 1440 minutos en un día (24 * 60)
        MS_PER_MINUTE = MS_PER_DAY / 1440 
        # 1. Ajustar el tiempo actual al ciclo de 24hd
        current_time_in_cycle = game_world.current_time % MS_PER_DAY
        # 2. Convertir milisegundos a minutos totales (usamos round para precisión)
        total_minutes = int(round(current_time_in_cycle / MS_PER_MINUTE))
        # 3. Calcular la hora y los minutos
        current_hour = (total_minutes // 60) % 24
        current_minute = total_minutes % 60
        time_display = f"{str(current_hour).zfill(2)}:{str(current_minute).zfill(2)}"
        time_text = font.render(f"Hora: {time_display}", True, Constantes.white)

        # ✔ FIX: subir los textos (antes estaban demasiado abajo)
        ventana.blit(energy_text, (0, Constantes.height - 150))
        ventana.blit(food_text,   (0, Constantes.height - 120))
        ventana.blit(thirst_text, (0, Constantes.height - 90))
        ventana.blit(time_text, (0, Constantes.height - 60))
        ventana.blit(stamina_text, (0, Constantes.height - 30))

        pygame.display.flip()

if __name__ == "__main__":
    main()
