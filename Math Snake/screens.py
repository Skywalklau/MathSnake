import pygame
import random
import math
from config import *

def death_animation(screen):
    """Cool death animation with particle explosion and screen shake"""
    # create explosion particles
    particles = []
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    
    for _ in range(100):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 15)
        particles.append({
            'x': center_x,
            'y': center_y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'color': random.choice([RED, YELLOW, (255, 165, 0), WHITE, (255, 100, 100)]),
            'size': random.randint(3, 8),
            'life': 60,
            'fade': random.uniform(0.8, 1.2)
        })
    
    clock = pygame.time.Clock()
    
    # animate explosion (2s)
    for frame in range(120):
        # screen shake effect
        shake_x = random.randint(-int(SCREEN_WIDTH * 0.05), int(SCREEN_WIDTH * 0.05)) if frame < 20 else 0
        shake_y = random.randint(-int(SCREEN_HEIGHT * 0.05), int(SCREEN_HEIGHT * 0.05)) if frame < 20 else 0
        
        # fade to red overlay
        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill(RED)
        fade_alpha = min(255, frame * 8)
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (shake_x, shake_y))
        
        # update and draw particles
        for particle in particles[:]:
            if particle['life'] <= 0:
                particles.remove(particle)
                continue
            
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3  # Gravity
            particle['life'] -= particle['fade']
            
            # draw particle with fading
            # life starts at 60, do / 60 gives proportion of life left
            # then multiply by 255 (max opacity) to simulate the fading effect by making
            # the particle more transparent with less life 
            alpha = max(0, min(255, int((particle['life'] / 60) * 255)))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            color_with_alpha = particle['color'] + (alpha,)
            pygame.draw.circle(particle_surface, color_with_alpha, (particle['size'], particle['size']), particle['size'])
            screen.blit(particle_surface, (int(particle['x']) + shake_x, int(particle['y']) + shake_y))
        
        # "WRONG!" text appears
        if frame > 40:
            wrong_text = HEADER_1.render("WRONG!", True, WHITE)
            text_alpha = min(255, (frame - 40) * 10)
            wrong_surface = wrong_text.copy()
            wrong_surface.set_alpha(text_alpha)
            screen.blit(wrong_surface, (SCREEN_WIDTH // 2 - wrong_text.get_width() // 2, SCREEN_HEIGHT // 3))
        
        pygame.display.update()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

def victory_animation(screen):
    """Epic victory animation with fireworks and celebration effects"""
    print("Victory animation started!")  # Debug
    # create fireworks
    fireworks = []
    confetti = []
    clock = pygame.time.Clock()
    
    # victory text with scaling effect (2s)
    for frame in range(120):
        if frame % 30 == 0:
            print(f"Victory animation frame: {frame}")  # Debug
        # gradient background that shifts colors
        time_factor = frame / 120
        r = max(0, min(255, int(50 + 100 * math.sin(time_factor * math.pi))))
        g = max(0, min(255, int(50 + 100 * math.cos(time_factor * math.pi))))
        b = max(0, min(255, int(100 + 100 * math.sin(time_factor * math.pi * 2))))
        screen.fill((r, g, b))
        
        # spawn fireworks randomly
        if frame % 8 == 0:
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT // 2)
            color = random.choice([GOLD, YELLOW, CYAN, PINK, PURPLE, GREEN, ORANGE])
            fireworks.append({
                'x': x,
                'y': y,
                'particles': [],
                'exploded': False,
                'color': color,
                'timer': 0
            })
        
        # update fireworks (need to shallow copy cuz if we delete we won't loop all fireworks)
        for firework in fireworks[:]:
            if not firework['exploded']:
                firework['timer'] += 1
                if firework['timer'] > 15:
                    firework['exploded'] = True
                    # create explosion particles
                    for _ in range(40):
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(2, 8)
                        firework['particles'].append({
                            'x': firework['x'],
                            'y': firework['y'],
                            'vx': math.cos(angle) * speed,
                            'vy': math.sin(angle) * speed,
                            'life': 60,
                            'size': random.randint(2, 5)
                        })
                else:
                    # rising firework
                    pygame.draw.circle(screen, firework['color'], 
                                     (int(firework['x']), int(firework['y'])), 4)
                    firework['y'] -= 3
            else:
                # update and draw explosion particles
                for particle in firework['particles'][:]:
                    if particle['life'] <= 0:
                        firework['particles'].remove(particle)
                        continue
                    
                    particle['x'] += particle['vx']
                    particle['y'] += particle['vy']
                    particle['vy'] += 0.15  # Gravity
                    particle['life'] -= 1
                    
                    alpha = max(0, min(255, int((particle['life'] / 60) * 255)))
                    if alpha > 0:
                        particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                        color_with_alpha = firework['color'] + (alpha,)
                        pygame.draw.circle(particle_surface, color_with_alpha, 
                                         (particle['size'], particle['size']), particle['size'])
                        screen.blit(particle_surface, (int(particle['x']), int(particle['y'])))
                
                # remove firework if all particles are gone
                if not firework['particles']:
                    fireworks.remove(firework)
        
        # random confetti
        for i in range(5):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, 3*SCREEN_HEIGHT//4)
            confetti_color = random.choice([GOLD, RED, GREEN, BLUE, PINK, YELLOW])
            size = random.randint(3, 6)
            pygame.draw.rect(screen, confetti_color, (x, y, size, size * 2))
        
        # victory text with pulsing effect
        scale = 1.0 + 0.2 * math.sin(frame * 0.1)
        victory_text = HEADER_1.render("VICTORY!", True, GOLD)
        
        # create scaled surface
        text_width = int(victory_text.get_width() * scale)
        text_height = int(victory_text.get_height() * scale)
        scaled_surface = pygame.transform.scale(victory_text, (text_width, text_height))
        
        # shadow effect
        shadow = HEADER_1.render("VICTORY!", True, BLACK)
        shadow_scaled = pygame.transform.scale(shadow, (text_width, text_height))
        screen.blit(shadow_scaled, 
                   (SCREEN_WIDTH // 2 - text_width // 2 + 5, SCREEN_HEIGHT // 3 + 5))
        
        # main text
        screen.blit(scaled_surface, 
                   (SCREEN_WIDTH // 2 - text_width // 2, SCREEN_HEIGHT // 3))
        
        pygame.display.update()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

def you_win_screen():
    win_message = HEADER_1.render("You Win!", True, RED)
    restart_message = HEADER_1.render("Press R to Restart", True, BLACK)
    quit_message = HEADER_1.render("Press Q to Quit", True, BLACK)

    while True:
        SCREEN.fill(WHITE)
        SCREEN.blit(win_message, (SCREEN_WIDTH // 2 - win_message.get_width() // 2, SCREEN_HEIGHT // 4))
        SCREEN.blit(restart_message, (SCREEN_WIDTH // 2 - restart_message.get_width() // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(quit_message, (SCREEN_WIDTH // 2 - quit_message.get_width() // 2, 3 * SCREEN_HEIGHT // 4))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_r:
                    return

def you_lose_screen():
    lose_message = HEADER_1.render("You Lost!", True, RED)
    restart_message = HEADER_1.render("Press R to Restart", True, BLACK)
    quit_message = HEADER_1.render("Press Q to Quit", True, BLACK)

    while True:
        SCREEN.fill(WHITE)
        SCREEN.blit(lose_message, (SCREEN_WIDTH // 2 - lose_message.get_width() // 2, SCREEN_HEIGHT // 4))
        SCREEN.blit(restart_message, (SCREEN_WIDTH // 2 - restart_message.get_width() // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(quit_message, (SCREEN_WIDTH // 2 - quit_message.get_width() // 2, 3 * SCREEN_HEIGHT // 4))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_r:
                    return