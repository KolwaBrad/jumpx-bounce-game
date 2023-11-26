import pygame
import sys
import random
import time

pygame.init()

width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

bird_radius = 25
bird_y_start = height // 2
bird = pygame.Rect(width // 2 - bird_radius, bird_y_start - bird_radius, bird_radius * 2, bird_radius * 2)
gravity = 0.5
jump = -10
velocity = 0

floor_color = (34, 177, 76)
grass_height = int(height * 0.5)  # Raise the floor position by 50%

obstacle_width = 50
obstacle_height = int(150 * 0.25)  # Reduce the height by 75%
obstacle_color = (255, 0, 0)
obstacle_x = width
obstacle_y = height - obstacle_height - grass_height
obstacle_min_height = int(100 * 0.25)  # Adjusted minimum height
obstacle_max_height = int(300 * 0.25)  # Adjusted maximum height

start_time = time.time()

def reset_obstacle():
    global obstacle_x, obstacle_y, obstacle_height
    obstacle_x = width
    obstacle_height = random.randint(obstacle_min_height, obstacle_max_height)
    obstacle_y = height - obstacle_height - grass_height

def pause_game():
    pause = True
    font = pygame.font.SysFont(None, 55)
    text = font.render('Game Paused: R to Restart, Q to Quit', True, (0, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_obstacle()
                    return True
                elif event.key == pygame.K_q:
                    return False

        screen.fill((135, 206, 250))
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(60)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = jump

    velocity += gravity
    bird.y += velocity
    bird.y = max(0, min(bird.y, height - bird.height - grass_height))

    if time.time() - start_time > 3:
        obstacle_x -= 5
        if obstacle_x + obstacle_width < 0:
            reset_obstacle()

    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    if bird.colliderect(obstacle_rect):
        if not pause_game():
            pygame.quit()
            sys.exit()

    screen.fill((135, 206, 250))
    pygame.draw.rect(screen, floor_color, (0, height - grass_height, width, grass_height))
    pygame.draw.circle(screen, (255, 0, 0), bird.center, bird_radius)
    pygame.draw.rect(screen, obstacle_color, obstacle_rect)

    pygame.display.flip()
    clock.tick(60)
