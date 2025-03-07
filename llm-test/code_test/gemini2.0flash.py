import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Ball properties
ball_radius = 15
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5
ball_dy = 0
gravity = 0.5
friction = 0.98

# Hexagon properties
hexagon_radius = 200
hexagon_x = WIDTH // 2
hexagon_y = HEIGHT // 2
hexagon_angle = 0
rotation_speed = 0.01

def draw_hexagon(angle):
    points = []
    for i in range(6):
        x = hexagon_x + hexagon_radius * math.cos(angle + i * math.pi / 3)
        y = hexagon_y + hexagon_radius * math.sin(angle + i * math.pi / 3)
        points.append((x, y))
    pygame.draw.polygon(screen, WHITE, points, 2)
    return points

def ball_collision(ball_x, ball_y, ball_dx, ball_dy, hexagon_points, hexagon_angle):
    new_ball_dx, new_ball_dy = ball_dx, ball_dy
    for i in range(6):
        x1, y1 = hexagon_points[i]
        x2, y2 = hexagon_points[(i + 1) % 6]

        # Calculate the distance from the ball to the line segment
        A = ball_x - x1
        B = ball_y - y1
        C = x2 - x1
        D = y2 - y1

        dot = A * C + B * D
        len_sq = C * C + D * D
        param = -1
        if len_sq != 0:
            param = dot / len_sq

        if param < 0:
            closest_x = x1
            closest_y = y1
        elif param > 1:
            closest_x = x2
            closest_y = y2
        else:
            closest_x = x1 + param * C
            closest_y = y1 + param * D

        dist = math.sqrt((ball_x - closest_x) ** 2 + (ball_y - closest_y) ** 2)

        if dist < ball_radius:
            # Collision detected
            normal_x = closest_x - ball_x
            normal_y = closest_y - ball_y
            normal_length = math.sqrt(normal_x ** 2 + normal_y ** 2)
            if normal_length != 0:
                normal_x /= normal_length
                normal_y /= normal_length

                # Calculate the relative velocity of the ball to the wall
                wall_velocity_x = -rotation_speed * (ball_y - hexagon_y)
                wall_velocity_y = rotation_speed * (ball_x - hexagon_x)

                relative_velocity_x = ball_dx - wall_velocity_x
                relative_velocity_y = ball_dy - wall_velocity_y

                # Calculate the dot product of the relative velocity and the normal
                dot_product = relative_velocity_x * normal_x + relative_velocity_y * normal_y

                # Calculate the new velocity components
                new_ball_dx = ball_dx - 2 * dot_product * normal_x
                new_ball_dy = ball_dy - 2 * dot_product * normal_y
                
                #add some of the wall velocity back in.
                new_ball_dx += wall_velocity_x * 0.1
                new_ball_dy += wall_velocity_y * 0.1
                
                # Move the ball out of the collision
                ball_x += normal_x * (ball_radius - dist)
                ball_y += normal_y * (ball_radius - dist)
                return new_ball_dx, new_ball_dy, ball_x, ball_y

    return new_ball_dx, new_ball_dy, ball_x, ball_y

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Apply gravity and friction
    ball_dy += gravity
    ball_dx *= friction
    ball_dy *= friction

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Rotate the hexagon
    hexagon_angle += rotation_speed

    # Draw background
    screen.fill(BLACK)

    # Draw hexagon
    hexagon_points = draw_hexagon(hexagon_angle)

    # Ball collision
    ball_dx, ball_dy, ball_x, ball_y = ball_collision(ball_x, ball_y, ball_dx, ball_dy, hexagon_points, hexagon_angle)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()