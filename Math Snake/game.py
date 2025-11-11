"""
Main game module for Math Snake.

This module contains the Game class which manages the core game loop,
collision detection, number collection, and win/lose conditions.
"""

import pygame
from config import *
from menu import get_difficulty
from question import QuestionWindow
from snake import Snake
from game_numbers import create_numbers
from grid import draw_lines, drawStats
from screens import you_win_screen, you_lose_screen, death_animation, victory_animation
from sounds import SoundManager

class Game:
    """
    Main game class that manages the Math Snake game loop and state.
    
    Handles initialization, game state management, collision detection,
    and coordinates between different game components.
    """
    
    def __init__(self):
        """Initialize the game with clock, running state, and sound manager."""
        self.clock = pygame.time.Clock()
        self.running = True
        self.sound_manager = SoundManager()
        
    def initialize_game(self, difficulty):
        """
        Initialize a new game session with the specified difficulty.
        
        Creates a math question, initializes the snake, generates number tiles,
        and ensures no overlapping positions between game elements.
        
        Args:
            difficulty (str): The difficulty level ('Easy', 'Medium', 'Hard', 'Insane')
            
        Returns:
            dict: Game state containing:
                - answer: The correct answer to the math expression
                - snake: The Snake object
                - nums: List of Number objects (0-9)
                - arr: List tracking collected digits
                - idx: Current index in the answer string
                - isNegative: Whether the answer is negative
                - ansLen: Length of the answer (excluding negative sign)
                - currentNumToFind: The Number object the player needs to find next
                - time: Game timer
        """
        question_window = QuestionWindow(difficulty)
        answer = question_window.display_expression()
        
        snake = Snake(SPOT_WIDTH, SPOT_HEIGHT)
        SCREEN.fill(WHITE)
        
        nums = create_numbers()
        
        # ensure no numbers overlap with each other or the snake
        occupied_positions = set()
        occupied_positions.add((snake.row, snake.col))
        
        for num in nums:
            # keep generating new positions until we find an unoccupied one
            while (num.row, num.col) in occupied_positions:
                num.createNewPos(occupied_positions)
            occupied_positions.add((num.row, num.col))
        
        arr = []
        idx = 0
        
        isNegative = False
        answerStr = str(answer)
        ansLen = len(answerStr)
        if answerStr[idx] == "-":
            idx += 1
            ansLen -= 1
            isNegative = True
        
        currentNumToFind = nums[int(answerStr[idx])]
        
        print(f"Answer: {answer}")
        
        return {
            'answer': answer,
            'snake': snake,
            'nums': nums,
            'arr': arr,
            'idx': idx,
            'isNegative': isNegative,
            'ansLen': ansLen,
            'currentNumToFind': currentNumToFind,
            'time': 0
        }
    
    def run(self):
        """
        Main game loop that handles rendering, input, collision detection, and game logic.
        
        The loop continues until the player quits. It manages:
        - Snake movement and collision detection
        - Number collection and validation
        - Win/lose conditions
        - Screen updates and animations
        - Sound effects
        """
        difficulty = get_difficulty()
        game_state = self.initialize_game(difficulty)
        foundDifficulty = True
        
        while self.running:
            if not foundDifficulty:
                difficulty = get_difficulty()
                game_state = self.initialize_game(difficulty)
                foundDifficulty = True
            
            self.clock.tick(FPS)
            game_state['time'] += 1
            
            drawStats(SCREEN, BLACK, game_state['arr'], game_state['time'])
            
            print(f"Number to find: {game_state['currentNumToFind'].number}, "
                  f"idx: {game_state['idx']}, ansLen: {game_state['ansLen']}")
            
            # snake movement
            game_state['snake'].move(
                BLUE, 
                SCREEN, 
                game_state['currentNumToFind'].row, 
                game_state['currentNumToFind'].col
            )
            
            # check collisions after movement
            if game_state['snake'].collisionWithSelf():
                print("SELF COLLISION DETECTED!")  # Debug
                self.sound_manager.play('collision')
                death_animation(SCREEN)
                you_lose_screen()
                foundDifficulty = False
                continue
            
            if game_state['snake'].collideWall:
                print("WALL COLLISION DETECTED!")  # Debug
                self.sound_manager.play('collision')
                death_animation(SCREEN)
                you_lose_screen()
                foundDifficulty = False
                continue
            
            for num in game_state['nums']:
                num.draw_Number(BLACK, SCREEN)
                
                if num.collision(game_state['snake'].row, game_state['snake'].col):
                    # play eat sound
                    self.sound_manager.play('eat')
                    
                    # build occupied set once
                    occupied = set(game_state['snake'].visited)
                    for other_num in game_state['nums']:
                        if other_num != num:
                            occupied.add((other_num.row, other_num.col))
                    
                    num.createNewNumber(WHITE, SCREEN, occupied)
                    
                    game_state['arr'].append(str(num.number))
                
                    if game_state['idx'] < game_state['ansLen']:
                        if num.number == str(game_state['answer'])[game_state['idx']]:
                            # correct number - play success sound
                            self.sound_manager.play('correct')
                            game_state['idx'] += 1
                            if game_state['idx'] <= game_state['ansLen']:
                                if game_state['idx'] < len(str(game_state['answer'])):
                                    game_state['currentNumToFind'] = game_state['nums'][
                                        int(str(game_state['answer'])[game_state['idx']])
                                    ]
                        else:
                            # wrong number eaten - trigger death animation
                            self.sound_manager.play('wrong')
                            death_animation(SCREEN)
                            you_lose_screen()
                            foundDifficulty = False
                            break  # skip rest of loop
                    
                    if len(game_state['arr']) == game_state['ansLen']:
                        print(f"Answer complete! arr: {''.join(game_state['arr'])}, answer: {game_state['answer']}")  # Debug
                        final_ans = (int("-" + "".join(game_state['arr'])) if game_state['isNegative'] else int("".join(game_state['arr'])))
                        
                        print(f"Final answer: {final_ans}, Expected: {int(game_state['answer'])}")  # Debug
                        if final_ans == int(game_state['answer']):
                            print("WIN CONDITION MET - Starting victory animation")  # Debug
                            self.sound_manager.play('victory')
                            victory_animation(SCREEN)
                            you_win_screen()
                            foundDifficulty = False
                            break
                        else:
                            self.sound_manager.play('wrong')
                            death_animation(SCREEN)
                            you_lose_screen()
                            foundDifficulty = False
                            break
            
            # draw grid lines with animation
            draw_lines(SQUARE_PER_ROW, SQUARE_PER_COL)
            
            # draw snake
            game_state['snake'].draw_head(BLUE, SCREEN)
            
            # snake speed
            pygame.time.delay(SNAKE_SPEED)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        self.running = False