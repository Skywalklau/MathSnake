import pygame
import random
from grid import GRID
from config import SQUARE_PER_ROW, SQUARE_PER_COL, SPOT_WIDTH, SPOT_HEIGHT

class Number:
    def __init__(self, width, height, number, font_size):
        self.number = number
        self.row = random.randint(1, SQUARE_PER_ROW - 1)
        self.col = random.randint(1, SQUARE_PER_COL - 1)
        self.width = width
        self.height = height
        self.font_size = font_size
        self.spot = GRID[self.row][self.col]
        self.font = pygame.font.Font("freesansbold.ttf", self.font_size)

    def get_number(self):
        return self.number

    def draw_Number(self, color, screen):
        text_surface = self.font.render(str(self.number), True, color)
        # use get_rect(center =) to auto calc. the top left coords when we align the number at the center
        # of the spot
        # get_rect(center=...) only moves the rectangle so its center is at the position we want
        text_rect = text_surface.get_rect(center=(self.spot.x + self.width//2, self.spot.y + self.height//2))
        screen.blit(text_surface, text_rect)

    def collision(self, x, y):
        return True if (self.row, self.col) == (x, y) else False

    def createNewPos(self, visited):
        while True:
            self.row = random.randint(1, SQUARE_PER_ROW - 1)
            self.col = random.randint(1, SQUARE_PER_COL - 1)
            if (self.row, self.col) not in visited:
                break
        self.spot = GRID[self.row][self.col]

    def createNewNumber(self, color, screen, visited):
        self.spot.reset(screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)


def create_numbers():
    return [
        Number(SPOT_WIDTH, SPOT_HEIGHT, "0", SPOT_WIDTH),
        Number(SPOT_WIDTH, SPOT_HEIGHT, "1", SPOT_WIDTH),
        Number(SPOT_WIDTH, SPOT_HEIGHT, "2", SPOT_WIDTH),
        Number(SPOT_WIDTH, SPOT_HEIGHT, "3", SPOT_WIDTH),
        Number(SPOT_WIDTH, SPOT_HEIGHT, "4", SPOT_WIDTH),
        Number(SPOT_WIDTH, SPOT_HEIGHT, "5", SPOT_WIDTH),
        Number(SPOT_WIDTH, SPOT_HEIGHT, "6", SPOT_WIDTH),
        Number(SPOT_WIDTH, SPOT_HEIGHT, "7", SPOT_WIDTH),
        Number(SPOT_WIDTH, SPOT_HEIGHT, "8", SPOT_WIDTH),
        Number(SPOT_WIDTH, SPOT_HEIGHT, "9", SPOT_WIDTH)
    ]