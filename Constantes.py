#TAMAÑOS
width, height = 1280, 720
personaje = 40
Tree = 50
cesped = 64
smallStone = 20

#COLORES
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
gray = (128, 128, 128)
brown = (139, 69, 19)

#BARRA DE ESTADO
MAX_ENERGY = 100
MAX_FOOD = 100
MAX_THIRST = 100 

#COLORES DE LA BARRA DE ESTADO
ENERGY_COLOR = (255, 255, 0)  # AMARILLO
FOOD_COLOR = (255, 165, 0)   # NARANJA
THIRST_COLOR = (0, 191, 255) # AZUL CLARO
BAR_BACKGROUND = (50, 50, 50)  # GRIS OSCURO

hechos = [
    ("personaje", "heroe"),
    ("personaje", "ogro"),
    ("arma", "espada"),
    ("arma", "garrote")
]

reglas = [
    ("puede_usar", "heroe", "espada"),
    ("puede_usar", "ogro", "garrote")
]
