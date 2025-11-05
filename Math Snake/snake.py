import pygame
import random
from collections import deque
from config import *
from grid import GRID

class Snake:
    def __init__(self, width, height):
        self.row = random.randint(int(SQUARE_PER_ROW * 0.1), int(SQUARE_PER_ROW * 0.9))
        self.col = random.randint(int(SQUARE_PER_COL * 0.1), int(SQUARE_PER_COL * 0.9))
        self.width = width
        self.height = height
        self.body = deque([GRID[self.row][self.col]])
        self.visited = deque([(self.row, self.col)])
        self.collideWall = False

    def draw_head(self, color, screen):
        self.spot = GRID[self.row][self.col]
        pygame.draw.rect(screen, color, pygame.Rect(self.spot.x, self.spot.y, self.width, self.height))

    def eat_number(self, x, y): # coords of the current target digit will be (x,y)
        return (x, y) == (self.row, self.col)

    def update_tail(self, screen, spot):
        pygame.draw.rect(screen, WHITE, pygame.Rect(spot.x, spot.y, spot.width, spot.height))

    def collisionWithSelf(self):
        count = 0
        for x, y in self.visited:
            if count >= 1 and (self.row, self.col) == (x, y):
                return True
            count += 1
        return False

    def move_common(self, color, screen, x, y):
        if not self.eat_number(x, y):
            spot = self.body.pop()
            self.visited.pop()
            self.update_tail(screen, spot)

        self.draw_head(color, screen)
        self.body.appendleft(self.spot)
        self.visited.appendleft((self.row, self.col))

    def move(self, color, screen, x, y):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            if self.row - 1 >= 1:
                self.row -= 1
                self.move_common(color, screen, x, y)
            else:
                self.collideWall = True

        elif key[pygame.K_a]:
            if self.col - 1 >= 0:
                self.col -= 1
                self.move_common(color, screen, x, y)
            else:
                self.collideWall = True

        elif key[pygame.K_s]:
            if self.row + 1 <= SQUARE_PER_ROW - 1:
                self.row += 1
                self.move_common(color, screen, x, y)
            else:
                self.collideWall = True

        elif key[pygame.K_d]:
            if self.col + 1 <= SQUARE_PER_COL - 1:
                self.col += 1
                self.move_common(color, screen, x, y)
            else:
                self.collideWall = True
