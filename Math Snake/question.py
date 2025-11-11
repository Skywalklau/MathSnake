"""
Question generation and display module for Math Snake.

This module creates difficulty-based math expressions and displays them
with an animated countdown timer and interactive star field.
"""

import pygame
import random
import time
import math
from random import randint, choice
from config import *

class QuestionWindow:
    """
    Manages math expression generation and display based on difficulty level.
    
    Creates timed challenge screens with animated backgrounds where players
    must memorize the expression and its answer before gameplay begins.
    """
    
    def __init__(self, difficulty):
        """
        Initialize the question window with a difficulty level.
        
        Args:
            difficulty (str): The difficulty level ('Easy', 'Medium', 'Hard', 'Insane')
        """
        self.difficulty = difficulty
        self.mathSymbols = ["+", "-", "*"]
    
    def createEasy(self):
        """
        Generate an easy-level math expression.
        
        Creates expressions with 2-3 numbers in range 1-99,
        using only addition and subtraction.
        
        Returns:
            str: A math expression string (e.g., "42 + 17" or "65 - 23 + 11")
        """
        varCount = randint(2, 3)
        def limit(): return randint(1, 99)
        expression = ""

        if varCount == 2:
            expression = f"{limit()} {self.mathSymbols[randint(0, 1)]} {limit()}"
        else:
            expression = f"{limit()} {self.mathSymbols[randint(0, 1)]} {limit()} " \
                         f"{self.mathSymbols[randint(0, 1)]} {limit()}"

        return expression
    
    def createMedium(self):
        """
        Generate a medium-level math expression.
        
        Creates expressions with 2-4 numbers in range 100-999,
        using addition and subtraction.
        
        Returns:
            str: A math expression string
        """
        varCount = randint(2, 4)
        def limit(): return randint(100, 999)
        expression = ""

        if varCount == 2:
            expression = f"{limit()} {self.mathSymbols[randint(0, 1)]} {limit()}"
        elif varCount == 3:
            expression = f"{limit()} {self.mathSymbols[randint(0, 1)]} {limit()} " \
                         f"{self.mathSymbols[randint(0, 1)]} {limit()}"
        else:
            expression = f"{limit()} {self.mathSymbols[randint(0, 1)]} {limit()} " \
                         f"{self.mathSymbols[randint(0, 1)]} {limit()} " \
                         f"{self.mathSymbols[randint(0, 1)]} {limit()}"

        return expression

    def createHard(self):
        """
        Generate a hard-level math expression.
        
        Creates expressions with 2-4 numbers (excluding -100 to +100),
        using addition, subtraction, and multiplication with parentheses.
        
        Returns:
            str: A math expression string with parentheses
        """
        varCount = randint(2, 4)
        def limit(): return choice([randint(-999, -101), randint(101, 999)])
        expression = ""

        if varCount == 2:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} ({limit()})"
        elif varCount == 3:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} {limit()}"
        else:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} ({limit()})"

        return expression

    def createInsane(self):
        """
        Generate an insane-level math expression.
        
        Creates expressions with 3-4 large numbers (excluding -100 to +100),
        using all operations including multiplication with parentheses.
        
        Returns:
            str: A complex math expression string with multiple parentheses
        """
        varCount = randint(3, 4)
        def limit(): return choice([randint(-9999, -101), randint(101, 9999)])
        expression = ""

        if varCount == 3:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} {limit()}"
        else:
            expression = f"{limit()} {self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} ({limit()}) " \
                         f"{self.mathSymbols[randint(0, 2)]} ({limit()})"

        return expression

    def display_expression(self):
        """
        Display the math expression with a countdown timer and interactive star field.
        
        Creates a timed challenge screen where:
        - Stars fall and can be clicked to create burst effects
        - A progress bar shows remaining time
        - Colors change based on urgency (green -> yellow -> red)
        - Timer pulses when time is running out
        
        Time limits by difficulty:
        - Easy: 10 seconds
        - Medium: 20 seconds
        - Hard: 35 seconds
        - Insane: 70 seconds
        
        Returns:
            int: The evaluated answer to the expression, or "undefined" if division by zero
        """
        expression = ""

        if self.difficulty == "Easy": 
            expression = self.createEasy()
            time_limit = 10
        elif self.difficulty == "Medium": 
            expression = self.createMedium()
            time_limit = 20
        elif self.difficulty == "Hard": 
            expression = self.createHard()
            time_limit = 35
        else: 
            expression = self.createInsane()
            time_limit = 70

        start_time = time.time()

        num_stars = 50
        stars = [{'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-SCREEN_HEIGHT, 0),
                'size': random.randint(10, 15),
                'color': YELLOW,
                'hovered': False,
                'burst': False,
                'burst_particles': []} for _ in range(num_stars)]

        clock = pygame.time.Clock()

        while True:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, time_limit - elapsed_time)

            trail_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            trail_surface.fill((0, 0, 0, 20))
            SCREEN.blit(trail_surface, (0, 0))
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for star in stars:
                if star['burst']:
                    for particle in star['burst_particles']:
                        particle['x'] += particle['vx']
                        particle['y'] += particle['vy']
                        particle['life'] -= 10
                        pygame.draw.circle(SCREEN, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])
                        if particle['life'] <= 0:
                            star['burst_particles'].remove(particle)
                    continue

                if abs(star['x'] - mouse_x) < star['size'] and abs(star['y'] - mouse_y) < star['size']:
                    if not star['hovered']:
                        star['color'] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                        star['hovered'] = True

                    if pygame.mouse.get_pressed()[0]: # left mouse button pressed
                        star['burst'] = True
                        star['burst_particles'] = []
                        for _ in range(10):
                            particle = {
                                'x': star['x'],
                                'y': star['y'],
                                'vx': random.randint(-3, 3),
                                'vy': random.randint(-3, 3),
                                'size': random.randint(1, 3),
                                'color': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
                                'life': 260
                            }
                            star['burst_particles'].append(particle)
                else:
                    star['hovered'] = False

                pygame.draw.circle(SCREEN, star['color'], (star['x'], star['y']), star['size'])

                star['y'] += 2
                if star['y'] > SCREEN_HEIGHT:
                    star['y'] = 0
                    star['x'] = random.randint(0, SCREEN_WIDTH)
                    star['size'] = random.randint(5, 10)
                    star['color'] = YELLOW
                    star['burst'] = False

            # create timer display with progress bar and visual feedback
            timer_text = str(int(remaining_time))
            time_percentage = remaining_time / time_limit
            
            # color changes based on remaining time
            if time_percentage > 0.5:
                timer_color = GREEN
                bar_color = GREEN
            elif time_percentage > 0.25:
                timer_color = YELLOW
                bar_color = YELLOW
            else:
                timer_color = RED
                bar_color = RED
                # pulse effect when time is low
                pulse = 1.0 + 0.3 * abs(math.sin(elapsed_time * 5))
            
            # draw timer background box
            timer_box_width = SCREEN_WIDTH * 0.2
            timer_box_height = SCREEN_HEIGHT * 0.1
            timer_box_x = SCREEN_WIDTH * 0.025
            timer_box_y = SCREEN_HEIGHT * 0.025
            
            # make another canvas to remove the fading effect
            timer_bg = pygame.Surface((timer_box_width, timer_box_height), pygame.SRCALPHA)
            timer_bg.fill((0, 0, 0, 200))
            SCREEN.blit(timer_bg, (timer_box_x, timer_box_y))
            
            # border
            pygame.draw.rect(SCREEN, timer_color, 
                           (timer_box_x, timer_box_y, timer_box_width, timer_box_height), 3)
            
            # timer text
            if time_percentage <= 0.25:
                # scale text when time is running out
                timer_font = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH * 0.035 * pulse))
            else:
                timer_font = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH * 0.035))
            
            timerText = timer_font.render(timer_text + "s", True, timer_color)
            SCREEN.blit(timerText, (timer_box_x * 1.5, timer_box_y * 1.3))
            
            # progress bar
            bar_width = timer_box_width * 0.9
            bar_height = timer_box_height * 0.2
            bar_x = timer_box_x * 1.4
            bar_y = timer_box_y + timer_box_height * 0.7
            
            
            # filled portion
            filled_width = int(bar_width * time_percentage)
            if filled_width > 0:
                pygame.draw.rect(SCREEN, bar_color, (bar_x, bar_y, filled_width, bar_height))
            
            # bar border
            pygame.draw.rect(SCREEN, bar_color, (bar_x, bar_y, bar_width, bar_height), 2)

            title = HEADER_1.render("Solve the Expression", True, WHITE)
            expression_text = HEADER_2.render(expression, True, WHITE)

            SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT * 0.15))
            SCREEN.blit(expression_text, (SCREEN_WIDTH // 2 - expression_text.get_width() // 2, SCREEN_HEIGHT * 0.52))

            pygame.display.update()

            if elapsed_time > time_limit:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            clock.tick(30)

        try:
            answer = eval(expression)
        except ZeroDivisionError:
            answer = "undefined (division by zero)"

        return answer