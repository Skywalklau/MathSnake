"""
Grid system and statistics display for Math Snake.

This module creates and manages the game grid, handles grid line rendering,
and displays game statistics (collected numbers and time) at the top of the screen.
"""

import pygame
import math
from config import *

class Spot:
    """
    Represents a single cell in the game grid.
    
    Each spot knows its grid coordinates (row, col), screen coordinates (x, y),
    dimensions, and color. Spots can be reset to their default appearance.
    """
    
    def __init__(self, row, col, x, y, width, height):
        """
        Initialize a grid spot with position and dimensions.
        
        Args:
            row (int): Row index in the grid
            col (int): Column index in the grid
            x (int): X-coordinate on screen (pixels)
            y (int): Y-coordinate on screen (pixels)
            width (int): Width of the spot in pixels
            height (int): Height of the spot in pixels
        """
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = WHITE

    def reset(self, screen):
        """
        Clear the spot by drawing it with its default color.
        
        Used to erase numbers or snake segments when they move.
        
        Args:
            screen (pygame.Surface): The game screen to draw on
        """
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

def make_grid(row, col):
    """
    Create a 2D grid of Spot objects covering the entire game area.
    
    Builds a row x col grid where each spot represents one playable cell.
    Each spot is initialized with its grid coordinates and screen position.
    
    Args:
        row (int): Number of rows in the grid
        col (int): Number of columns in the grid
        
    Returns:
        list: 2D list of Spot objects, indexed as grid[row][col]
    """
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
    """
    Draw the grid lines that separate each cell.
    
    Renders horizontal and vertical lines to create the visible grid structure.
    Lines start at row 1 to leave space for the stats bar at the top.
    
    Args:
        row (int): Number of rows in the grid
        col (int): Number of columns in the grid
    """
    # draw horizontal lines
    for i in range(row):
        y = i * SPOT_HEIGHT
        pygame.draw.line(SCREEN, BLACK, (0, y), (SCREEN_WIDTH, y), width=2)

    # draw vertical lines
    for j in range(col):
        x = j * SPOT_WIDTH
        pygame.draw.line(SCREEN, BLACK, (x, SPOT_HEIGHT), (x, SCREEN_HEIGHT), width=2)

def drawStats(screen, color, nums, time):
    """
    Display game statistics in the top bar of the screen.
    
    Shows:
    - Collected digits sequence (on the left side, centered)
    - Elapsed game time in frames (on the right side)
    
    The stats bar is drawn with a black background spanning the full width
    and occupying the top row of the grid.
    
    Args:
        screen (pygame.Surface): The game screen to draw on
        color (tuple): RGB color for the stats bar background (typically BLACK)
        nums (list): List of collected digit strings to display
        time (int): Elapsed time in frames since game start
    """
    pygame.draw.rect(screen, color, pygame.Rect(0, 0, SCREEN_WIDTH, SPOT_HEIGHT))

    Number = FONT_BIG.render("".join(nums), True, GREEN)
    Time = FONT_BIG.render("Time : " + str(time), True, GREEN)

    screen.blit(Time, (0.02 * SCREEN_WIDTH, SPOT_HEIGHT * 0.25))
    screen.blit(Number, (0.42 * SCREEN_WIDTH, SPOT_HEIGHT * 0.25))

# Create the global game grid
GRID = make_grid(SQUARE_PER_ROW, SQUARE_PER_COL)