"""
Number tile management for Math Snake.

This module handles the creation, positioning, and rendering of digit tiles (0-9)
that appear on the game grid for the snake to collect.
"""

import pygame
import random
from grid import GRID
from config import SQUARE_PER_ROW, SQUARE_PER_COL, SPOT_WIDTH, SPOT_HEIGHT

class Number:
    """
    Represents a single digit tile on the game grid.
    
    Each Number object corresponds to one digit (0-9) and can be repositioned
    when collected by the snake. Numbers are rendered centered within their
    grid cell.
    """
    
    def __init__(self, width, height, number, font_size):
        """
        Initialize a number tile at a random grid position.
        
        Args:
            width (int): Width of the grid cell
            height (int): Height of the grid cell
            number (str): The digit to display ("0" through "9")
            font_size (int): Font size for rendering the digit
        """
        self.number = number
        self.row = random.randint(1, SQUARE_PER_ROW - 1)
        self.col = random.randint(1, SQUARE_PER_COL - 1)
        self.width = width
        self.height = height
        self.font_size = font_size
        self.spot = GRID[self.row][self.col]
        self.font = pygame.font.Font("freesansbold.ttf", self.font_size)

    def get_number(self):
        """
        Get the digit value of this number tile.
        
        Returns:
            str: The digit string ("0" through "9")
        """
        return self.number

    def draw_Number(self, color, screen):
        """
        Render the number centered within its grid cell.
        
        Uses get_rect(center=...) to automatically calculate the top-left
        coordinates needed to center the text within the spot.
        
        Args:
            color (tuple): RGB color tuple for the digit
            screen (pygame.Surface): The game screen to draw on
        """
        text_surface = self.font.render(str(self.number), True, color)
        # use get_rect(center =) to auto calc. the top left coords when we align the number at the center
        # of the spot
        # get_rect(center=...) only moves the rectangle so its center is at the position we want
        text_rect = text_surface.get_rect(center=(self.spot.x + self.width//2, self.spot.y + self.height//2))
        screen.blit(text_surface, text_rect)

    def collision(self, x, y):
        """
        Check if the given position collides with this number's position.
        
        Args:
            x (int): Row coordinate to check
            y (int): Column coordinate to check
            
        Returns:
            bool: True if positions match, False otherwise
        """
        return True if (self.row, self.col) == (x, y) else False

    def createNewPos(self, visited):
        """
        Generate a new random position that doesn't overlap with visited positions.
        
        Keeps generating random positions until finding one that's not in the
        visited set (snake body or other numbers).
        
        Args:
            visited (set): Set of (row, col) tuples representing occupied positions
        """
        # calculate available positions
        total_positions = (SQUARE_PER_ROW - 1) * (SQUARE_PER_COL - 1)
        if len(visited) >= total_positions:
            # fallback: if grid is full, just pick random (shouldn't happen in normal gameplay)
            self.row = random.randint(1, SQUARE_PER_ROW - 1)
            self.col = random.randint(1, SQUARE_PER_COL - 1)
        else:
            # keep trying random positions (expected iterations is low when grid isn't crowded)
            # worse case is still O(N) cuz if we have N-1 cells occupied and we only have 1 free cell
            # left, the probability of choosing it is 1/N
            # the expected tries will be 1/(1/N) = N.
            # Because the number of iterations follow a geometric distribution.
            while True:
                self.row = random.randint(1, SQUARE_PER_ROW - 1)
                self.col = random.randint(1, SQUARE_PER_COL - 1)
                if (self.row, self.col) not in visited:
                    break
        self.spot = GRID[self.row][self.col]

    def createNewNumber(self, color, screen, visited):
        """
        Reset the number's old position and move it to a new valid location.
        
        This is called when the snake collects the number. It clears the old
        grid cell and repositions the number to a new unoccupied spot.
        
        Args:
            color (tuple): RGB color for clearing the old position (typically WHITE)
            screen (pygame.Surface): The game screen to update
            visited (set): Set of (row, col) tuples representing occupied positions
        """
        self.spot.reset(screen)
        self.createNewPos(visited)
        self.draw_Number(color, screen)


def create_numbers():
    """
    Create and return a list of all 10 digit tiles (0-9).
    
    Each number is initialized at a random position on the grid with
    font size matching the grid cell width for optimal visibility.
    
    Returns:
        list: List of 10 Number objects representing digits 0 through 9
    """
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