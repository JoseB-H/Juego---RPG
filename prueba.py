import pygame
import sys
import time
import subprocess

# Inicializar Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 240)
BLACK = (0, 0, 0)
GOLD = (212, 175, 55)
BROWN = (101, 67, 33)
DARK_RED = (139, 0, 0)
FPS = 60

# Ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú RPG Medieval")

# Fuente medieval (si tienes una TTF puedes cargarla)
try:
    font = pygame.font.Font("MedievalSharp-Regular.ttf", 50)
except:
    font = pygame.font.SysFont("Times New Roman", 50, bold=True)

# Botón estilo pergamino
class RPGButton:
    def __init__(self, text, x, y, w, h, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        # Fondo del botón
        pygame.draw.rect(surface, self.hover_color if is_hover else self.color, self.rect, border_radius=8)
        # Borde estilo antiguo
        pygame.draw.rect(surface, GOLD, self.rect, 4, border_radius=8)
        # Texto
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# Botones
start_button = RPGButton("Iniciar Juego", WIDTH//2-150, 150, 300, 70, BROWN, DARK_RED)
dificultades = ["Fácil", "Medio", "Difícil", "Insane", "Nivel Dina"]
buttons_dificultad = [RPGButton(d, WIDTH//2-150, 250 + i*80, 300, 60, BROWN, DARK_RED) for i, d in enumerate(dificultades)]

# Menú
menu = "principal"
dificultad_seleccionada = None

clock = pygame.time.Clock()
running = True

# Fondo estilo medieval
def draw_background(surface):
    try:
        bg_image = pygame.image.load("assets/IMG/Fondo/fondo_prueba.webp").convert()
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
        surface.blit(bg_image, (0, 0))
    except:
        # Si no hay imagen, fondo degradado rojo-dorado
        for y in range(HEIGHT):
            color = (139 + y//10, 0 + y//4, 0)
            pygame.draw.line(surface, color, (0, y), (WIDTH, y))

# Loop del menú
while running:
    draw_background(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if menu == "principal":
            if start_button.is_clicked(event):
                menu = "dificultad"
        elif menu == "dificultad":
            for i, btn in enumerate(buttons_dificultad):
                if btn.is_clicked(event):
                    dificultad_seleccionada = dificultades[i]
                    running = False
                    break

    if menu == "principal":
        start_button.draw(screen)
    elif menu == "dificultad":
        for btn in buttons_dificultad:
            btn.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

# Pantalla de carga estilo RPG
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cargando...")

try:
    loading_bg = pygame.image.load("assets/IMG/Fondo/prueba_carga.webp").convert()
    loading_bg = pygame.transform.scale(loading_bg, (WIDTH, HEIGHT))
    screen.blit(loading_bg, (0, 0))
except:
    screen.fill(BLACK)

font = pygame.font.Font(None, 60)
text = font.render(f"Cargando juego ({dificultad_seleccionada})...", True, GOLD)
rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
screen.blit(text, rect)
pygame.display.flip()
time.sleep(2)

pygame.quit()

# Ejecutar el juego real
subprocess.run(["python", "Menu.py"])
