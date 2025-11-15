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
            
        personaje.movimiento(dx,dy,game_world)

        game_world.update_chunks(personaje.x, personaje.y)

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

        # Dibujar inventario si está abierto
        if show_inventory:
            personaje.draw_inventory(ventana)

        font = pygame.font.SysFont('Arial', 24)
        energy_text = font.render(f"Energía: {personaje.energy}", True, Constantes.white)
        food_text = font.render(f"Comida: {personaje.food}", True, Constantes.white)
        thirst_text = font.render(f"Sed: {personaje.thirst}", True, Constantes.white)

        time_of_day = (game_world.current_time // Constantes.DAY_LENGTH) % 24
        time_text = font.render(f"Hora: {time_of_day}:00", True, Constantes.white)

        # ✔ FIX: subir los textos (antes estaban demasiado abajo)
        ventana.blit(energy_text, (10, Constantes.height - 150))
        ventana.blit(food_text,   (10, Constantes.height - 120))
        ventana.blit(thirst_text, (10, Constantes.height - 90))

        pygame.display.flip()

if __name__ == "__main__":
    main()
