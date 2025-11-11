import pygame

# Initialize pygame first
pygame.init()

# FPS
FPS = 60

# SCREEN SIZE
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# STAR COUNT
STAR_COUNT = 100

# NUMBER OF ROWS/COLS
SQUARE_PER_ROW = 30
SQUARE_PER_COL = 30

# SPOT DIMENSIONS
SPOT_WIDTH = SCREEN_WIDTH // SQUARE_PER_COL
SPOT_HEIGHT = SCREEN_HEIGHT // SQUARE_PER_ROW

# FONTS FOR MENU
HEADER_1 = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH * 0.05))
HEADER_2 = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH * 0.04))

# FONTS FOR IN-GAME 
FONT_BIG = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH * 0.03))
FONT_SMALL = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH * 0.02))
FONT_SPOT = pygame.font.Font("freesansbold.ttf", int(SPOT_WIDTH * 0.9))

# SNAKE SPEED (lower value --> faster)
SNAKE_SPEED = 100

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
MAROON = (128, 0, 0)
PURPLE = (200, 0, 255)
TURQUOISE = (48, 213, 200)
BLUEBERRY_BLUE = (79, 134, 247)
GOLD = (255, 215, 0)
CYAN = (0, 255, 255)
PINK = (255, 105, 180) 
REDDISH_PINK = (255, 100, 100)
ORANGE = (255, 165, 0)

# Difficulty colors
EASY_COLOR = (0, 255, 0)
MEDIUM_COLOR = (255, 255, 0)
HARD_COLOR = (255, 0, 0)
INSANE_COLOR = (128, 0, 0)

# TONE FREQUENCIES
C5 = 523
E5 = 659
G5 = 784
C6 = 1047

# SCREEN
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))