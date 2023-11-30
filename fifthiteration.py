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
grass_height = int(height * 0.35)

obstacle_width = 50
obstacle_min_height = 100
obstacle_max_height = 300
obstacle_color = (255, 0, 0)

# Set the ball color to dark purple
bird_color = (128, 0, 128)

obstacles = []

obstacle_speed = 10  # Speed of obstacles
next_obstacle_distance = width // 4  # Distance at which to generate next obstacle
last_obstacle_time = time.time()
obstacle_generation_interval = 0.5  # Time between generating new obstacles

first_obstacle_after_restart = True

def add_new_obstacle():
    obstacle_height = random.randint(obstacle_min_height, obstacle_max_height)
    if random.choice([True, False]):
        obstacle_y = height - obstacle_height - grass_height
    else:
        obstacle_y = 0
    obstacles.append([width, obstacle_y, obstacle_width, obstacle_height])

def move_obstacles():
    for obstacle in obstacles:
        obstacle[0] -= obstacle_speed

def remove_off_screen_obstacles():
    global obstacles
    obstacles = [obstacle for obstacle in obstacles if obstacle[0] > -obstacle_width]

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
                    return True
                elif event.key == pygame.K_q:
                    return False

        screen.fill((135, 206, 250))
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(60)

add_new_obstacle()

while True:
    current_time = time.time()
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

    move_obstacles()

    if first_obstacle_after_restart and current_time - last_obstacle_time > 3:
        add_new_obstacle()
        last_obstacle_time = current_time
        first_obstacle_after_restart = False
    elif not first_obstacle_after_restart and current_time - last_obstacle_time > obstacle_generation_interval:
        add_new_obstacle()
        last_obstacle_time = current_time

    remove_off_screen_obstacles()

    collision = False
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3])
        if bird.colliderect(obstacle_rect):
            collision = True
            break

    if collision:
        if not pause_game():
            pygame.quit()
            sys.exit()

    screen.fill((135, 206, 250))
    pygame.draw.rect(screen, floor_color, (0, height - grass_height, width, grass_height))
    
    # Draw the ball with dark purple color
    pygame.draw.circle(screen, bird_color, bird.center, bird_radius)
    
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle_color, obstacle)

    pygame.display.flip()
    clock.tick(60)
