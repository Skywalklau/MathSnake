import pygame
from game import Game

def main():
    pygame.display.set_caption("Math Snake")
    
    game = Game()
    game.run()
    
    
if __name__ == "__main__":
    main()