import pygame
import math
from config import *

class Spot:
    def __init__(self, row, col, x, y, width, height):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = WHITE

    def reset(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

def make_grid(row, col):
    grid = []
    y = 0

    for i in range(row):
        temp = []
        x = 0
        for j in range(col):
            spot = Spot(i, j, x, y, SPOT_WIDTH, SPOT_HEIGHT)
            temp.append(spot)
            x += SPOT_WIDTH
        y += SPOT_HEIGHT
        grid.append(temp)

    return grid

def draw_lines(row, col):
    # draw horizontal lines
    for i in range(row):
        y = i * SPOT_HEIGHT
        pygame.draw.line(SCREEN, BLACK, (0, y), (SCREEN_WIDTH, y), width=2)

    # draw vertical lines
    for j in range(col):
        x = j * SPOT_WIDTH
        pygame.draw.line(SCREEN, BLACK, (x, SPOT_HEIGHT), (x, SCREEN_HEIGHT), width=2)

def drawStats(screen, color, nums, time):
    pygame.draw.rect(screen, color, pygame.Rect(0, 0, SCREEN_WIDTH, SPOT_HEIGHT))

    Number = FONT_BIG.render("".join(nums), True, GREEN)
    Time = FONT_BIG.render("Time : " + str(time), True, GREEN)

    screen.blit(Time, (0.02 * SCREEN_WIDTH, SPOT_HEIGHT * 0.25))
    screen.blit(Number, (0.42 * SCREEN_WIDTH, SPOT_HEIGHT * 0.25))

GRID = make_grid(SQUARE_PER_ROW, SQUARE_PER_COL)