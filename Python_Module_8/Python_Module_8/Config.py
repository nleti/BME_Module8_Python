# Assets
import os
BASE_DIR = os.path.dirname(__file__)

# Join paths safely across all operating systems
SPRITESHEET_PATH = os.path.join(BASE_DIR, "Assets", "SpriteSheets", "Virus Game")
LEVELS_PATH = os.path.join(BASE_DIR, "Assets")

# Window Settings
WINDOW_WIDTH,WINDOW_HEIGHT = 960, 540

TILESIZE = 16

GRAVITY = 0.3

SPEED_HERO = 4
ANIMSPEED_HERO_DEFAULT = 0.25
ANIMSPEED_HERO_IDLE = 0.1
ANIMSPEED_HERO_JUMP = 0.2

# -- Virus --
SPEED_VIRUS_RED = 2.1
ANIMSPEED_VIRUS = 0.1
ATTACK_RANGE = 100
