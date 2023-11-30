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

bird_color = (128, 0, 128)

# Star properties
star_radius = 10
star_color_options = [(255, 255, 0), (255, 182, 193), (0, 0, 0)]  # Yellow, Pink, Black
star_color = random.choice(star_color_options)
star_x = width
star_y = random.randint(grass_height + star_radius, height - grass_height - star_radius)

obstacles = []

obstacle_speed = 10
next_obstacle_distance = width // 4
last_obstacle_time = time.time()
obstacle_generation_interval = 0.5

first_obstacle_after_restart = True

star_generation_interval = 10
last_star_time = time.time()

# Variable to handle ball color change
ball_color_change_start_time = 0

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

def handle_star_collision():
    global ball_color_change_start_time, bird_color

    if bird.colliderect(star_rect):
        ball_color_change_start_time = time.time()
        bird_color = star_color

def reset_ball_color():
    global bird_color, ball_color_change_start_time
    bird_color = (128, 0, 128)
    ball_color_change_start_time = 0

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

    # Star generation and movement
    if current_time - last_star_time > star_generation_interval:
        star_color = random.choice(star_color_options)
        star_x = width
        star_y = random.randint(grass_height + star_radius, height - grass_height - star_radius)
        last_star_time = current_time

    star_x -= obstacle_speed

    star_rect = pygame.Rect(star_x - star_radius, star_y - star_radius, star_radius * 2, star_radius * 2)

    handle_star_collision()

    if ball_color_change_start_time > 0 and current_time - ball_color_change_start_time > star_generation_interval:
        reset_ball_color()

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

    pygame.draw.circle(screen, bird_color, bird.center, bird_radius)
    
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle_color, obstacle)

    pygame.draw.circle(screen, star_color, (star_x, star_y), star_radius)

    pygame.display.flip()
    clock.tick(60)
