import pygame
import random
import math
import time
from config import *

galaxy_stars = []
for i in range(STAR_COUNT):
    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(50, 0.9 * SCREEN_WIDTH // 2)
    speed = random.uniform(0.001, 0.003)
    size = random.randint(2, 5)
    alpha = random.randint(100, 180) # transparency
    galaxy_stars.append({
        'angle': angle,
        'radius': radius,
        'speed': speed,
        'size': size,
        'alpha': alpha
    })

def draw_galaxy():
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    
    for star in galaxy_stars:
        # update angle to make it orbit
        star['angle'] += star['speed']
        
        # calculate position based on angle and radius
        x = center_x + star['radius'] * math.cos(star['angle'])
        y = center_y + star['radius'] * math.sin(star['angle'])
        
        # draw the star
        star_surface = pygame.Surface((star['size'] * 2, star['size'] * 2), pygame.SRCALPHA)
        pygame.draw.circle(star_surface, WHITE + (star['alpha'],), (star['size'], star['size']), star['size'])
        SCREEN.blit(star_surface, (x - star['size'], y - star['size']))

def draw_menu():
    PADDING = int(SCREEN_WIDTH * 0.05)
    SPACING = int(SCREEN_HEIGHT * 0.1)

    easy_button = FONT_BIG.render("Easy", True, BLACK)
    medium_button = FONT_BIG.render("Medium", True, BLACK)
    hard_button = FONT_BIG.render("Hard", True, BLACK)
    insane_button = FONT_BIG.render("Insane", True, BLACK)

    easy_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - easy_button.get_width() // 2 - PADDING,
        SCREEN_HEIGHT // 2 - SPACING * 2, # 30% of height
        easy_button.get_width() + PADDING * 2,
        easy_button.get_height() + PADDING
    )

    medium_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - medium_button.get_width() // 2 - PADDING,
        easy_rect.bottom + SPACING,
        medium_button.get_width() + PADDING * 2,
        medium_button.get_height() + PADDING
    )

    hard_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - hard_button.get_width() // 2 - PADDING,
        medium_rect.bottom + SPACING,
        hard_button.get_width() + PADDING * 2,
        hard_button.get_height() + PADDING
    )

    insane_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - insane_button.get_width() // 2 - PADDING,
        hard_rect.bottom + SPACING,
        insane_button.get_width() + PADDING * 2,
        insane_button.get_height() + PADDING
    )

    time_elapsed = time.time() % 100
    r = max(0, min(255, int(100 + 50 * math.sin(time_elapsed))))
    g = max(0, min(255, int(100 + 50 * math.cos(time_elapsed))))
    b = max(0, min(255, int(150 + 50 * math.sin(time_elapsed / 2))))
    SCREEN.fill((r,g,b))

    draw_galaxy()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if easy_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(SCREEN, EASY_COLOR, easy_rect, 5)
        pygame.draw.rect(SCREEN, WHITE, easy_rect, 3)
    else:
        pygame.draw.rect(SCREEN, EASY_COLOR, easy_rect)

    if medium_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(SCREEN, MEDIUM_COLOR, medium_rect, 5)
        pygame.draw.rect(SCREEN, WHITE, medium_rect, 3)
    else:
        pygame.draw.rect(SCREEN, MEDIUM_COLOR, medium_rect)

    if hard_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(SCREEN, HARD_COLOR, hard_rect, 5)
        pygame.draw.rect(SCREEN, WHITE, hard_rect, 3)
    else:
        pygame.draw.rect(SCREEN, HARD_COLOR, hard_rect)

    if insane_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(SCREEN, INSANE_COLOR, insane_rect, 5)
        pygame.draw.rect(SCREEN, WHITE, insane_rect, 3)
    else:
        pygame.draw.rect(SCREEN, INSANE_COLOR, insane_rect)

    title = HEADER_1.render("Welcome to Math Snake", True, BLACK)
    selectLevel = HEADER_2.render("Select Difficulty Level", True, BLACK)

    SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT * 0.1))
    SCREEN.blit(selectLevel, (SCREEN_WIDTH // 2 - selectLevel.get_width() // 2, SCREEN_HEIGHT * 0.2))

    SCREEN.blit(easy_button, (easy_rect.x + PADDING, easy_rect.y + PADDING // 2))
    SCREEN.blit(medium_button, (medium_rect.x + PADDING, medium_rect.y + PADDING // 2))
    SCREEN.blit(hard_button, (hard_rect.x + PADDING, hard_rect.y + PADDING // 2))
    SCREEN.blit(insane_button, (insane_rect.x + PADDING, insane_rect.y + PADDING // 2))

    if easy_rect.collidepoint(mouse_x, mouse_y) or medium_rect.collidepoint(mouse_x, mouse_y) or \
            hard_rect.collidepoint(mouse_x, mouse_y) or insane_rect.collidepoint(mouse_x, mouse_y):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    pygame.display.update()

    return easy_rect, medium_rect, hard_rect, insane_rect

def get_difficulty():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                easy_rect, medium_rect, hard_rect, insane_rect = draw_menu()
                if easy_rect.collidepoint(mouse_pos):
                    return "Easy"
                elif medium_rect.collidepoint(mouse_pos):
                    return "Medium"
                elif hard_rect.collidepoint(mouse_pos):
                    return "Hard"
                elif insane_rect.collidepoint(mouse_pos):
                    return "Insane"

        draw_menu()
        pygame.display.update()