import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Inside Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Ball properties
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_radius = 10
ball_vel = [0, 0]
gravity = 0.5
friction = 0.99

# Hexagon properties
hexagon_radius = 200
num_sides = 6
hexagon_center = (WIDTH // 2, HEIGHT // 2)
rotation_angle = 0
rotation_speed = 0.01

def draw_hexagon(screen, center, radius, num_sides, color, angle=0):
    vertices = []
    for i in range(num_sides):
        theta = 2 * math.pi * i / num_sides + angle
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        vertices.append((x, y))
    pygame.draw.polygon(screen, color, vertices)

def points_to_edges(points):
    edges = []
    num_points = len(points)
    for i in range(num_points):
        j = (i + 1) % num_points
        edges.append((points[i], points[j]))
    return edges

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def point_line_distance(point, start, end):
    line_vec = (end[0] - start[0], end[1] - start[1])
    point_vec = (point[0] - start[0], point[1] - start[1])
    line_len = distance(start, end)
    line_unitvec = (line_vec[0] / line_len, line_vec[1] / line_len)
    point_vec_scaled = (point_vec[0] * line_len, point_vec[1] * line_len)
    t = point_vec_scaled[0] * line_unitvec[0] + point_vec_scaled[1] * line_unitvec[1]
    if t < 0:
        t = 0
    elif t > line_len:
        t = line_len
    nearest = (start[0] + line_unitvec[0] * t, start[1] + line_unitvec[1] * t)
    return distance(point, nearest), nearest

def reflect_velocity(vel, normal):
    dot_product = vel[0] * normal[0] + vel[1] * normal[1]
    reflect_x = vel[0] - 2 * dot_product * normal[0]
    reflect_y = vel[1] - 2 * dot_product * normal[1]
    return [reflect_x, reflect_y]

def normalize(vector):
    length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    return [vector[0] / length, vector[1] / length]

def main():
    clock = pygame.time.Clock()
    global ball_pos, ball_vel, gravity, friction, hexagon_radius, num_sides, hexagon_center, rotation_angle, rotation_speed

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update physics
        ball_vel[1] += gravity  # Apply gravity
        ball_vel[0] *= friction  # Apply friction
        ball_vel[1] *= friction
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        # Compute hexagon vertices
        hexagon_vertices = []
        for i in range(num_sides):
            theta = 2 * math.pi * i / num_sides + rotation_angle
            x = hexagon_center[0] + hexagon_radius * math.cos(theta)
            y = hexagon_center[1] + hexagon_radius * math.sin(theta)
            hexagon_vertices.append((x, y))

        # Check for collisions
        edges = points_to_edges(hexagon_vertices)
        for edge in edges:
            dist, nearest = point_line_distance(ball_pos, edge[0], edge[1])
            if dist <= ball_radius:
                normal = normalize((edge[1][0] - edge[0][0], edge[1][1] - edge[0][1]))
                ball_vel = reflect_velocity(ball_vel, normal)
                ball_pos[0] = nearest[0] + normal[0] * ball_radius
                ball_pos[1] = nearest[1] + normal[1] * ball_radius

        # Update rotation angle
        rotation_angle += rotation_speed

        # Clear screen
        screen.fill(WHITE)

        # Draw hexagon
        draw_hexagon(screen, hexagon_center, hexagon_radius, num_sides, BLACK, rotation_angle)

        # Draw ball
        pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
