import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Hexagon parameters
hexagon_center = (width // 2, height // 2)
hexagon_radius = 200
hexagon_rotation_speed = 0.01  # Radians per frame
hexagon_angle = 0

def get_hexagon_vertices(center, radius, angle):
    vertices = []
    for i in range(6):
        x = center[0] + radius * math.cos(angle + 2 * math.pi * i / 6)
        y = center[1] + radius * math.sin(angle + 2 * math.pi * i / 6)
        vertices.append((int(x), int(y)))
    return vertices

def draw_hexagon(surface, color, vertices):
    pygame.draw.polygon(surface, color, vertices, 2)

# Ball parameters
ball_radius = 20
ball_color = red
ball_pos = [width // 2, height // 2]  # Start at center
ball_velocity = [2, 2]  # Initial velocity (x, y)
gravity = 0.1
friction = 0.01
bounce_factor = 0.7  # Energy loss on bounce

clock = pygame.time.Clock()

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def normalize_vector(vector):
    magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
    if magnitude != 0:
        return [vector[0] / magnitude, vector[1] / magnitude]
    return [0, 0]

def reflect_vector(incident_vector, normal_vector):
    """Reflects an incident vector off a surface with a given normal vector."""
    dot_product = incident_vector[0] * normal_vector[0] + incident_vector[1] * normal_vector[1]
    reflected_x = incident_vector[0] - 2 * dot_product * normal_vector[0]
    reflected_y = incident_vector[1] - 2 * dot_product * normal_vector[1]
    return [reflected_x, reflected_y]


def is_ball_colliding_with_hexagon(ball_pos, ball_radius, hexagon_vertices):
    for i in range(6):
        p1 = hexagon_vertices[i]
        p2 = hexagon_vertices[(i + 1) % 6]

        # Vector representing the hexagon edge
        edge_vector = [p2[0] - p1[0], p2[1] - p1[1]]
        edge_length_sq = edge_vector[0]**2 + edge_vector[1]**2

        # Vector from p1 to ball center
        p1_to_ball = [ball_pos[0] - p1[0], ball_pos[1] - p1[1]]

        # Projection parameter (how far along the edge the closest point is)
        t = max(0, min(1, (p1_to_ball[0] * edge_vector[0] + p1_to_ball[1] * edge_vector[1]) / edge_length_sq))

        # Closest point on the edge to the ball center
        closest_point = [p1[0] + t * edge_vector[0], p1[1] + t * edge_vector[1]]

        # Distance from ball center to the closest point on the edge
        dist = distance(ball_pos, closest_point)

        if dist <= ball_radius:
            # Collision detected, return the normal vector of the edge

            # Normal vector is perpendicular to the edge.
            # For counter-clockwise vertices order, swap x and y and negate x to get outward normal.
            normal_vector = [-edge_vector[1], edge_vector[0]]
            return normalize_vector(normal_vector)  # Return normalized normal vector

    return None # No collision


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(black)

    # Update hexagon angle for rotation
    hexagon_angle += hexagon_rotation_speed

    # Get hexagon vertices
    hexagon_vertices = get_hexagon_vertices(hexagon_center, hexagon_radius, hexagon_angle)

    # Draw the spinning hexagon
    draw_hexagon(screen, white, hexagon_vertices)

    # Apply gravity
    ball_velocity[1] += gravity

    # Apply friction (simple air friction)
    ball_velocity[0] *= (1 - friction)
    ball_velocity[1] *= (1 - friction)


    # Predict next ball position
    next_ball_pos = [ball_pos[0] + ball_velocity[0], ball_pos[1] + ball_velocity[1]]

    # Check for collision with hexagon
    collision_normal = is_ball_colliding_with_hexagon(next_ball_pos, ball_radius, hexagon_vertices)

    if collision_normal:
        # Reflect the velocity based on the collision normal
        ball_velocity = reflect_vector(ball_velocity, collision_normal)
        # Apply bounce factor (energy loss)
        ball_velocity[0] *= bounce_factor
        ball_velocity[1] *= bounce_factor

        # To prevent sticking, move ball slightly along normal after collision
        ball_pos[0] += collision_normal[0] * (ball_radius + 1) * 0.1 # nudge out a bit
        ball_pos[1] += collision_normal[1] * (ball_radius + 1) * 0.1


    # Update ball position
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]


    # Simple screen boundaries (optional, if you want the ball to stay within screen - can remove for hexagon only containment)
    if ball_pos[0] - ball_radius < 0 or ball_pos[0] + ball_radius > width:
        ball_velocity[0] = -ball_velocity[0] * bounce_factor
        ball_pos[0] = max(ball_radius, min(ball_pos[0], width - ball_radius)) # Keep ball inside bounds

    if ball_pos[1] - ball_radius < 0 or ball_pos[1] + ball_radius > height:
        ball_velocity[1] = -ball_velocity[1] * bounce_factor
        ball_pos[1] = max(ball_radius, min(ball_pos[1], height - ball_radius)) # Keep ball inside bounds


    # Draw the ball
    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()