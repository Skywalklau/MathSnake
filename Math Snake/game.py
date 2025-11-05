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
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.sound_manager = SoundManager()
        
    def initialize_game(self, difficulty):
        """Initialize or reset game state"""
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
            'game_over': False,
            'time': 0
        }
    
    def run(self):
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
            
            if not game_state['game_over']:
                for num in game_state['nums']:
                    num.draw_Number(BLACK, SCREEN)
                    
                    if num.collision(game_state['snake'].row, game_state['snake'].col):
                        # play eat sound
                        self.sound_manager.play('eat')
                        
                        num.createNewNumber(WHITE, SCREEN, game_state['snake'].visited)
                        
                        # check if new position conflicts with other numbers
                        other_nums_positions = set()
                        for other_num in game_state['nums']:
                            if other_num != num:
                                other_nums_positions.add((other_num.row, other_num.col))
                        
                        # keep repositioning if it overlaps with another number or snake
                        while (num.row, num.col) in other_nums_positions or (num.row, num.col) in game_state['snake'].visited:
                            num.createNewPos(game_state['snake'].visited)
                        
                        game_state['arr'].append(str(num.number))
                    
                        if game_state['idx'] < game_state['ansLen']:
                            if num.number == str(game_state['answer'])[game_state['idx']]:
                                # correct number - play success sound
                                self.sound_manager.play('correct')
                                game_state['idx'] += 1
                                if game_state['idx'] < game_state['ansLen']:
                                    game_state['currentNumToFind'] = game_state['nums'][
                                        int(str(game_state['answer'])[game_state['idx']])
                                    ]
                            else:
                                # wrong number eaten - trigger death animation
                                self.sound_manager.play('wrong')
                                death_animation(SCREEN)
                                you_lose_screen()
                                foundDifficulty = False
                                continue  # skip rest of loop
                        
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
                                continue
                            else:
                                self.sound_manager.play('wrong')
                                death_animation(SCREEN)
                                you_lose_screen()
                                foundDifficulty = False
                                continue
            
            # draw grid lines with animation
            draw_lines(SQUARE_PER_ROW, SQUARE_PER_COL)
            
            # check collisions
            if game_state['snake'].collisionWithSelf() or game_state['snake'].collideWall:
                death_animation(SCREEN)
                you_lose_screen()
                foundDifficulty = False
                continue
            
            if game_state['game_over']:
                you_lose_screen()
                foundDifficulty = False
                continue
            
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