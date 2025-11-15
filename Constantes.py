#TAMAÑOS
width, height = 1280, 720
personaje = 70
Tree = 100
cesped = 64
smallStone = 20

#ANIAMCIONES
BASIC_FRAMES=6
IDLE_DOWN = 0
IDLE_RIGHT = 1
IDLE_UP = 2
WALK_DOWN = 3
WALK_RIGHT = 4
WALK_UP = 5
ANIMATION_FRAME = 32
ANIMATION_DELAY = 100

#COLORES
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
gray = (128, 128, 128)
brown = (139, 69, 19)
#SISTEMA DE REGLAS

#BARRAS DE ESTADO
MAX_ENERGY = 100
MAX_FOOD = 100
MAX_THIRST = 100

#COLORES DE BARRAS
ENERGY_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 165, 0)
THIRST_COLOR = (0, 191, 255)
BAR_BACKGROUND = (100, 100, 100)

#INTEREVALO DE TIEMPO
STATUS_UPDATE_INTERVAL = 1000

#SISTEMA DE DIA / NOCHE
DAY_LENGTH = 240000
DAWN_TIME = 60000
MORNING_TIME = 80000
DUSK_TIME = 180000
MIDNIGHT_TIME = 240000
MAX_DARKNESS = 240

#COLORES DE LA ILUMINACION
NIGHT_COLOR = (20, 20, 50)
DAY_COLOR = (255, 255, 225)
DAWN_DUSK_COLOR = (255, 193, 137)

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
