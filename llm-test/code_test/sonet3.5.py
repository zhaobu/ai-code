import pygame
import math
import sys
from pygame import Vector2

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.8
BALL_RADIUS = 10
HEX_RADIUS = 200
ROTATION_SPEED = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
clock = pygame.time.Clock()

# Ball properties
ball_pos = Vector2(WIDTH // 2, HEIGHT // 2)
ball_vel = Vector2(0, 0)

# Hexagon properties
hex_angle = 0
hex_points = []

def get_hex_points():
    points = []
    for i in range(6):
        angle = math.radians(hex_angle + i * 60)
        x = WIDTH // 2 + HEX_RADIUS * math.cos(angle)
        y = HEIGHT // 2 + HEX_RADIUS * math.sin(angle)
        points.append((x, y))
    return points

def line_intersection(p1, p2, circle_pos, circle_radius):
    x1, y1 = p1
    x2, y2 = p2
    cx, cy = circle_pos

    # Vector from line start to circle center
    dx = cx - x1
    dy = cy - y1
    
    # Vector from line start to line end
    line_dx = x2 - x1
    line_dy = y2 - y1
    line_length = math.sqrt(line_dx**2 + line_dy**2)
    
    # Normalize line vector
    line_dx /= line_length
    line_dy /= line_length
    
    # Project circle center onto line
    proj = dx * line_dx + dy * line_dy
    
    # Find closest point on line to circle
    closest_x = x1 + proj * line_dx
    closest_y = y1 + proj * line_dy
    
    # Check if projection is within line segment
    if 0 <= proj <= line_length:
        # Distance from closest point to circle center
        dist = math.sqrt((cx - closest_x)**2 + (cy - closest_y)**2)
        return dist <= circle_radius
    return False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position and velocity
    ball_vel.y += GRAVITY
    ball_pos += ball_vel

    # Update hexagon rotation
    hex_angle += ROTATION_SPEED
    hex_points = get_hex_points()

    # Check for collisions with hexagon sides
    for i in range(6):
        p1 = hex_points[i]
        p2 = hex_points[(i + 1) % 6]
        
        if line_intersection(p1, p2, ball_pos, BALL_RADIUS):
            # Calculate normal vector of the line
            line_dx = p2[0] - p1[0]
            line_dy = p2[1] - p1[1]
            length = math.sqrt(line_dx**2 + line_dy**2)
            normal = Vector2(-line_dy/length, line_dx/length)
            
            # Reflect velocity vector
            dot_product = ball_vel.dot(normal)
            ball_vel = ball_vel - 2 * dot_product * normal
            
            # Apply friction
            ball_vel *= FRICTION

    # Draw
    screen.fill(BLACK)
    
    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hex_points, 2)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos.x), int(ball_pos.y)), BALL_RADIUS)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()