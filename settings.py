import pygame as pg

# Window settings
RES = WIDTH, HEIGHT = 1024, 1024
FPS = 60

# Scaling factor (Pixels per meter)
SCALE = 30  # Scale Factor: 30 pixels per meter
MAX_TIME_STEP = 1.0 / FPS  # Simulation step

# Define collision types
FLOOR_COLLISION_TYPE = 1
BOX_COLLISION_TYPE = 2


# Level Info
BUCKET_X = 200
BUCKET_Y = 120
NUMBER_OF_GRAINS = 150
LEVEL_GOAL = 100
LEVEL_START_POS = (WIDTH//2, HEIGHT - 20)

# User Defined Events
START_FLOW = pg.USEREVENT + 1
FLOW_DELAY = pg.USEREVENT + 2