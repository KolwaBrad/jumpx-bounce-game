import pygame
import sys

pygame.init()

width, height = 400, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

bird_radius = 25
bird = pygame.Rect(width // 2 - bird_radius, height // 2 - bird_radius, bird_radius * 2, bird_radius * 2)
gravity = 0.5
jump = -10
velocity = 0

floor_color = (34, 177, 76)
grass_height = 50

obstacle_width = 50
obstacle_height = 30
obstacle_color = (255, 0, 0)
obstacle_x = width // 2 - obstacle_width // 2
obstacle_y = height - grass_height - obstacle_height

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bird.y == height - bird.height:
                velocity += jump
            elif event.key == pygame.K_RIGHT:
                bird.x += 15  # Move bird forward
            elif event.key == pygame.K_LEFT:
                bird.x -= 15     # Move bird backward

    velocity += gravity
    bird.y += velocity

    # Bounce off the top wall
    if bird.y < 0:
        bird.y = 0
        velocity = abs(velocity)  # Bounce back with positive velocity

    # Bounce off the bottom wall and jump over the obstacle
    if bird.y > height - bird.height:
        bird.y = height - bird.height
        velocity = 0  # Stop vertical movement

    # Wrap around left and right edges
    if bird.x < -bird_radius:
        bird.x = width
    elif bird.x > width:
        bird.x = -bird_radius

    # Move obstacle to the left
    obstacle_x -= 5

    # Reset obstacle position when it goes off the screen
    if obstacle_x + obstacle_width < 0:
        obstacle_x = width
        obstacle_y = height - grass_height - obstacle_height

    screen.fill((135, 206, 250))  # Sky blue background

    # Draw grass features
    pygame.draw.rect(screen, floor_color, (0, height - grass_height, width, grass_height))

    # Draw bouncing circular bird
    pygame.draw.circle(screen, (255, 0, 0), bird.center, bird_radius)

    # Draw obstacle
    pygame.draw.rect(screen, obstacle_color, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

    pygame.display.flip()
    clock.tick(60)