# game options/settings
TITLE = "Mario"
SCALE = 3
WIDTH = 256 * SCALE
HEIGHT = 240 * SCALE
FPS = 60
FONT_NAME = 'arial'
SPRITESHEET_WORLD = "World1-1.png"
SPRITESHEET_CHAR = "MarioSprite.png"
SPRITESHEET_TILE = "Tiles.png"

#Player Propperties
PLAYER_ACC = 0.4
PLAYER_FRICTION = -0.1
PLAYER_GRAV = 0.8
PLAYER_JUMP = 12#34*PLAYER_GRAV

# Starting platforms
PLATFORM_LIST = []


# GROUND
for x in range(0,15*69*SCALE,15*SCALE):
    PLATFORM_LIST.append((x, HEIGHT - 15*SCALE//2, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15*SCALE//2-15*SCALE, 0))

for x in range(15*71*SCALE,15*86*SCALE,15*SCALE):
    PLATFORM_LIST.append((x, HEIGHT - 15*SCALE//2, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15*SCALE//2-15*SCALE, 0))

for x in range(15*89*SCALE,15*153*SCALE,15*SCALE):
    PLATFORM_LIST.append((x, HEIGHT - 15*SCALE//2, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15*SCALE//2-15*SCALE, 0))

for x in range(15*155*SCALE,15*208*SCALE,15*SCALE):
    PLATFORM_LIST.append((x, HEIGHT - 15*SCALE//2, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15*SCALE//2-15*SCALE, 0))

# PIPES
PLATFORM_LIST.append((15*28*SCALE, HEIGHT - 18*SCALE//2-45*SCALE, 2))

PLATFORM_LIST.append((15*38*SCALE, HEIGHT - 18*SCALE//2-45*SCALE - 15*SCALE, 2))
PLATFORM_LIST.append((15*38*SCALE, HEIGHT - 18*SCALE//2-45*SCALE + 15*SCALE, 3))

# STEPS
for y in range(1, 5):
    for x in range(15*155*SCALE,15*(160-y)*SCALE,15*SCALE):
        PLATFORM_LIST.append((x, HEIGHT - 15*SCALE//2-(1+y)*15*SCALE, 1))

for y in range(1, 5):
    for x in range(15*140*SCALE,15*(145-y)*SCALE,15*SCALE):
        PLATFORM_LIST.append((x, HEIGHT - 15*SCALE//2-(1+y)*15*SCALE, 1))

for y in range(1, 5):
    for x in range(15*(133+y)*SCALE,15*138*SCALE,15*SCALE):
        PLATFORM_LIST.append((x, HEIGHT - 15*SCALE//2-(1+y)*15*SCALE, 1))

#PLATFORM_LIST.append((15*21*SCALE, HEIGHT - 15*SCALE//2-45*SCALE, 4))

# Blocks
BLOCKS_LIST = []

BLOCKS_LIST.append((15*21*SCALE, HEIGHT - 15*SCALE//2-45*SCALE, 4))





#Define colors
WHITE = ( 255, 255, 255 )
BLACK = (0, 0 , 0)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE