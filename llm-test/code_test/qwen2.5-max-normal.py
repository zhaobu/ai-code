import pygame
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Hexagon parameters
HEXAGON_CENTER = (WIDTH // 2, HEIGHT // 2)
HEXAGON_RADIUS = 200
NUM_SIDES = 6

# Ball parameters
BALL_RADIUS = 10
ball_pos = [WIDTH // 2 + 50, HEIGHT // 2]  # Initial position
ball_velocity = [3, -5]  # Initial velocity
gravity = 0.2  # Gravity effect
friction = 0.99  # Friction coefficient

# Function to calculate hexagon vertices
def get_hexagon_vertices(center, radius, angle):
    vertices = []
    for i in range(NUM_SIDES):
        theta = (math.pi / 3) * i + angle  # Angle for each vertex
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        vertices.append((x, y))
    return vertices

# Function to check collision between ball and hexagon edge
def check_collision(ball_pos, ball_radius, p1, p2):
    # Vector from p1 to p2
    edge = (p2[0] - p1[0], p2[1] - p1[1])
    # Vector from p1 to ball
    ball_to_p1 = (ball_pos[0] - p1[0], ball_pos[1] - p1[1])

    # Project ball_to_p1 onto edge
    edge_length_sq = edge[0] ** 2 + edge[1] ** 2
    t = max(0, min((ball_to_p1[0] * edge[0] + ball_to_p1[1] * edge[1]) / edge_length_sq, 1))
    closest_point = (p1[0] + t * edge[0], p1[1] + t * edge[1])

    # Distance between ball and closest point
    distance_sq = (ball_pos[0] - closest_point[0]) ** 2 + (ball_pos[1] - closest_point[1]) ** 2
    if distance_sq <= ball_radius ** 2:
        return closest_point
    return None

# Main game loop
angle = 0  # Initial rotation angle of the hexagon
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball velocity with gravity
    ball_velocity[1] += gravity

    # Apply friction
    ball_velocity[0] *= friction
    ball_velocity[1] *= friction

    # Update ball position
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Get hexagon vertices
    vertices = get_hexagon_vertices(HEXAGON_CENTER, HEXAGON_RADIUS, angle)

    # Check for collisions with hexagon edges
    collided = False
    for i in range(NUM_SIDES):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % NUM_SIDES]
        closest_point = check_collision(ball_pos, BALL_RADIUS, p1, p2)
        if closest_point:
            # Calculate normal vector of the edge
            edge = (p2[0] - p1[0], p2[1] - p1[1])
            edge_length = math.hypot(edge[0], edge[1])
            normal = (-edge[1] / edge_length, edge[0] / edge_length)

            # Reflect velocity vector
            dot_product = ball_velocity[0] * normal[0] + ball_velocity[1] * normal[1]
            ball_velocity[0] -= 2 * dot_product * normal[0]
            ball_velocity[1] -= 2 * dot_product * normal[1]

            # Move ball out of the wall
            overlap = BALL_RADIUS - math.hypot(ball_pos[0] - closest_point[0], ball_pos[1] - closest_point[1])
            ball_pos[0] += overlap * normal[0]
            ball_pos[1] += overlap * normal[1]

            collided = True

    # Rotate the hexagon
    angle += 0.02

    # Draw the hexagon
    pygame.draw.polygon(screen, BLUE, vertices, 2)

    # Draw the ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()