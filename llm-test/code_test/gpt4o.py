import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Ball properties
ball_radius = 10
ball_pos = [WIDTH // 2, HEIGHT // 4]
ball_velocity = [2, 0]
gravity = 0.5
friction = 0.9

# Hexagon properties
hexagon_radius = 200
hexagon_center = (WIDTH // 2, HEIGHT // 2)
hexagon_angle = 0
hexagon_rotation_speed = 2  # degrees per frame

def rotate_point(point, angle, center):
    """Rotate a point around a center by a given angle."""
    angle_rad = math.radians(angle)
    x, y = point
    cx, cy = center
    x -= cx
    y -= cy
    new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    return new_x + cx, new_y + cy

def get_hexagon_vertices(center, radius, angle):
    """Get the vertices of a rotated hexagon."""
    vertices = []
    for i in range(6):
        theta = math.radians(i * 60)  # 60 degrees for each side
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        vertices.append(rotate_point((x, y), angle, center))
    return vertices

def reflect_velocity(velocity, normal):
    """Reflect the velocity vector based on the collision normal."""
    dot_product = velocity[0] * normal[0] + velocity[1] * normal[1]
    return [
        velocity[0] - 2 * dot_product * normal[0],
        velocity[1] - 2 * dot_product * normal[1],
    ]

def normalize(vector):
    """Normalize a vector."""
    length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if length == 0:
        return [0, 0]
    return [vector[0] / length, vector[1] / length]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(BLACK)

    # Update hexagon rotation
    hexagon_angle += hexagon_rotation_speed
    hexagon_vertices = get_hexagon_vertices(hexagon_center, hexagon_radius, hexagon_angle)

    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hexagon_vertices, 2)

    # Update ball position
    ball_velocity[1] += gravity  # Apply gravity
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Check for collisions with hexagon walls
    for i in range(6):
        p1 = hexagon_vertices[i]
        p2 = hexagon_vertices[(i + 1) % 6]
        edge = [p2[0] - p1[0], p2[1] - p1[1]]
        edge_normal = normalize([-edge[1], edge[0]])

        # Vector from edge point to ball
        ball_to_edge = [ball_pos[0] - p1[0], ball_pos[1] - p1[1]]
        distance = abs(ball_to_edge[0] * edge_normal[0] + ball_to_edge[1] * edge_normal[1])

        if distance <= ball_radius:
            # Reflect ball velocity
            ball_velocity = reflect_velocity(ball_velocity, edge_normal)
            ball_velocity[0] *= friction
            ball_velocity[1] *= friction

            # Move ball out of collision
            overlap = ball_radius - distance
            ball_pos[0] += edge_normal[0] * overlap
            ball_pos[1] += edge_normal[1] * overlap

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()