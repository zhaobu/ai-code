import pygame
import sys
import math
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Physics parameters
GRAVITY = 0.5
FRICTION = 0.99
RESTITUTION = 0.8  # Bounciness

# Ball properties
ball_radius = 15
ball_pos = [WIDTH // 2, HEIGHT // 3]
ball_vel = [0, 0]

# Hexagon properties
hex_radius = 200
hex_center = [WIDTH // 2, HEIGHT // 2]
hex_angle = 0
hex_rotation_speed = 0.005

# Clock for controlling frame rate
clock = pygame.time.Clock()

def get_hexagon_vertices(center, radius, angle):
    """Calculate the vertices of the hexagon based on center, radius, and rotation angle."""
    vertices = []
    for i in range(6):
        theta = angle + i * (2 * math.pi / 6)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        vertices.append((x, y))
    return vertices

def get_hexagon_edges(vertices):
    """Get the edges of the hexagon as line segments."""
    edges = []
    for i in range(len(vertices)):
        edges.append((vertices[i], vertices[(i + 1) % len(vertices)]))
    return edges

def distance_point_to_line(point, line):
    """Calculate the distance from a point to a line segment and the closest point on the line."""
    x0, y0 = point
    x1, y1 = line[0]
    x2, y2 = line[1]
    
    # Vector from line start to end
    line_vec = (x2 - x1, y2 - y1)
    # Vector from line start to point
    point_vec = (x0 - x1, y0 - y1)
    
    # Length of line squared
    line_len_sq = line_vec[0]**2 + line_vec[1]**2
    
    # Calculate projection of point_vec onto line_vec
    if line_len_sq == 0:  # Line is actually a point
        return math.sqrt((x0 - x1)**2 + (y0 - y1)**2), (x1, y1)
    
    t = max(0, min(1, (point_vec[0] * line_vec[0] + point_vec[1] * line_vec[1]) / line_len_sq))
    
    # Calculate closest point on line
    closest_x = x1 + t * line_vec[0]
    closest_y = y1 + t * line_vec[1]
    
    # Calculate distance
    distance = math.sqrt((x0 - closest_x)**2 + (y0 - closest_y)**2)
    
    return distance, (closest_x, closest_y)

def check_collision(ball_pos, ball_radius, edges):
    """Check if the ball collides with any edge of the hexagon."""
    for edge in edges:
        distance, closest_point = distance_point_to_line(ball_pos, edge)
        if distance <= ball_radius:
            return True, closest_point, edge
    return False, None, None

def handle_collision(ball_pos, ball_vel, closest_point, edge):
    """Handle the collision between the ball and an edge."""
    # Calculate normal vector to the edge
    edge_vec = (edge[1][0] - edge[0][0], edge[1][1] - edge[0][1])
    edge_len = math.sqrt(edge_vec[0]**2 + edge_vec[1]**2)
    
    if edge_len == 0:
        return ball_vel
    
    # Normalize edge vector
    edge_vec = (edge_vec[0] / edge_len, edge_vec[1] / edge_len)
    
    # Calculate normal vector (perpendicular to edge)
    normal = (-edge_vec[1], edge_vec[0])
    
    # Calculate reflection direction
    dot_product = ball_vel[0] * normal[0] + ball_vel[1] * normal[1]
    
    # Calculate new velocity after reflection
    new_vel_x = ball_vel[0] - 2 * dot_product * normal[0]
    new_vel_y = ball_vel[1] - 2 * dot_product * normal[1]
    
    # Apply restitution (bounciness)
    new_vel_x *= RESTITUTION
    new_vel_y *= RESTITUTION
    
    # Move ball away from the edge to prevent sticking
    overlap = ball_radius - distance_point_to_line(ball_pos, edge)[0]
    ball_pos[0] += normal[0] * overlap * 1.1
    ball_pos[1] += normal[1] * overlap * 1.1
    
    return [new_vel_x, new_vel_y]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Update hexagon rotation
    hex_angle += hex_rotation_speed
    
    # Get hexagon vertices and edges
    vertices = get_hexagon_vertices(hex_center, hex_radius, hex_angle)
    edges = get_hexagon_edges(vertices)
    
    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, vertices, 2)
    
    # Update ball position with gravity
    ball_vel[1] += GRAVITY
    
    # Apply friction
    ball_vel[0] *= FRICTION
    ball_vel[1] *= FRICTION
    
    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Check for collision with hexagon edges
    collision, closest_point, edge = check_collision(ball_pos, ball_radius, edges)
    if collision:
        ball_vel = handle_collision(ball_pos, ball_vel, closest_point, edge)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    # Update display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(60)

pygame.quit()
sys.exit()