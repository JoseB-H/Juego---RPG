import pygame  # pyright: ignore[reportMissingImports]
import sys
import Constantes
from Personajes import default
from mundo import mundo

# --- MENU ---
pygame.init()

ventana = pygame.display.set_mode((Constantes.width, Constantes.height))
pygame.display.set_caption("Menu")

def main():
    clock = pygame.time.Clock()
    game_world = mundo(Constantes.width, Constantes.height)  
    personaje = default(Constantes.width // 2, Constantes.height // 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit() 

        # --- movimientos del personaje
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            personaje.movimiento(-5, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            personaje.movimiento(5, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            personaje.movimiento(0, -5)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            personaje.movimiento(0, 5)

        game_world.draw(ventana)   # fondo
        personaje.draw(ventana)    # personaje
        pygame.display.flip()

        clock.tick(60)  # limita a 60 FPS

if __name__ == "__main__":
    main()
