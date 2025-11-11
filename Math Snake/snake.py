"""
Snake module for Math Snake game.

This module contains the Snake class which manages the snake's
position, movement, collision detection, and rendering.
"""

import pygame
import random
from collections import deque
from config import *
from grid import GRID

class Snake:
    """
    Represents the player-controlled snake in the game.
    
    The snake moves on a grid and grows when eating numbers.
    It can collide with walls or itself, ending the game.
    """
    
    def __init__(self, width, height):
        """
        Initialize the snake at a random position on the grid.
        
        Args:
            width (int): Width of each grid cell
            height (int): Height of each grid cell
        """
        self.row = random.randint(int(SQUARE_PER_ROW * 0.1), int(SQUARE_PER_ROW * 0.9))
        self.col = random.randint(int(SQUARE_PER_COL * 0.1), int(SQUARE_PER_COL * 0.9))
        self.width = width
        self.height = height
        self.body = deque([GRID[self.row][self.col]])
        self.visited = deque([(self.row, self.col)])
        self.collideWall = False

    def draw_head(self, color, screen):
        """
        Draw the snake's head at its current position.
        
        Args:
            color (tuple): RGB color tuple for the snake head
            screen (pygame.Surface): The game screen to draw on
        """
        self.spot = GRID[self.row][self.col]
        pygame.draw.rect(screen, color, pygame.Rect(self.spot.x, self.spot.y, self.width, self.height))

    def eat_number(self, x, y):
        """
        Check if the snake's head is at the target number's position.
        
        Args:
            x (int): Row coordinate of the target
            y (int): Column coordinate of the target
            
        Returns:
            bool: True if snake head is at target position, False otherwise
        """
        return (x, y) == (self.row, self.col)

    def update_tail(self, screen, spot):
        """
        Erase the tail segment when the snake moves without eating.
        
        Args:
            screen (pygame.Surface): The game screen to draw on
            spot (Spot): The grid spot to clear
        """
        pygame.draw.rect(screen, WHITE, pygame.Rect(spot.x, spot.y, spot.width, spot.height))

    def collisionWithSelf(self):
        """
        Check if the snake's head has collided with its own body.
        
        Returns:
            bool: True if collision detected, False otherwise
        """
        for i in range(1, len(self.visited)): # exclude head
            if (self.row, self.col) == self.visited[i]:
                return True
        return False

    def move_common(self, color, screen, x, y):
        """
        Common movement logic executed after directional input.
        
        Handles tail removal (if not eating), head drawing, and body/visited updates.
        
        Args:
            color (tuple): RGB color for the snake
            screen (pygame.Surface): The game screen to draw on
            x (int): Row of the target number
            y (int): Column of the target number
        """
        if not self.eat_number(x, y):
            spot = self.body.pop()
            self.visited.pop()
            self.update_tail(screen, spot)

        self.draw_head(color, screen)
        self.body.appendleft(self.spot)
        self.visited.appendleft((self.row, self.col))

    def move(self, color, screen, x, y):
        """
        Handle snake movement based on keyboard input (WASD keys).
        
        Checks boundaries, updates position, and sets collision flag if hitting walls.
        
        Args:
            color (tuple): RGB color for the snake
            screen (pygame.Surface): The game screen to draw on
            x (int): Row of the target number
            y (int): Column of the target number
        """
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