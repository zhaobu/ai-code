import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Ball properties
ball_radius = 10
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_velocity = [0, 0]
gravity = 0.5
friction = 0.9

# Hexagon properties
hex_side_length = 150
hex_center = [WIDTH // 2, HEIGHT // 2]
rotation_speed = 0.01
angle = 0

# Function to draw a hexagon
def draw_hexagon(center, side_length, angle):
    points = []
    for i in range(6):
        x = center[0] + side_length * math.cos(math.radians(60 * i + angle))
        y = center[1] + side_length * math.sin(math.radians(60 * i + angle))
        points.append((x, y))
    pygame.draw.polygon(screen, WHITE, points, 3)

# Function to check collision between ball and hexagon
def check_collision(ball_pos, ball_radius, hex_points):
    for i in range(len(hex_points)):
        p1 = hex_points[i]
        p2 = hex_points[(i + 1) % len(hex_points)]
        
        # Calculate normal vector of the edge
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        norm = math.sqrt(dx**2 + dy**2)
        nx = -dy / norm
        ny = dx / norm
        
        # Project ball position onto the normal vector
        px = ball_pos[0] - p1[0]
        py = ball_pos[1] - p1[1]
        dot_product = px * nx + py * ny
        
        if dot_product > 0 and dot_product < norm:
            distance = abs(px * nx + py * ny)
            if distance < ball_radius:
                return True, (nx, ny)
    return False, (0, 0)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_velocity[1] += gravity
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Rotate hexagon
    angle += rotation_speed

    # Get hexagon points
    hex_points = []
    for i in range(6):
        x = hex_center[0] + hex_side_length * math.cos(math.radians(60 * i + angle))
        y = hex_center[1] + hex_side_length * math.sin(math.radians(60 * i + angle))
        hex_points.append((x, y))

    # Check for collision
    collision, normal = check_collision(ball_pos, ball_radius, hex_points)
    if collision:
        # Reflect velocity based on normal vector
        dot_product = ball_velocity[0] * normal[0] + ball_velocity[1] * normal[1]
        ball_velocity[0] -= 2 * dot_product * normal[0]
        ball_velocity[1] -= 2 * dot_product * normal[1]
        ball_velocity[0] *= friction
        ball_velocity[1] *= friction

    # Clear screen
    screen.fill(BLACK)

    # Draw hexagon
    draw_hexagon(hex_center, hex_side_length, angle)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()