import pygame
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Hexagon parameters
hex_radius = 150
hex_center = (WIDTH//2, HEIGHT//2)
hex_angle = 0
rotation_speed = 1  # Degrees per frame

# Ball parameters
ball_radius = 10
ball_pos = [hex_center[0], hex_center[1] - 100]
ball_vel = [3.5, 0]
gravity = 0.4
friction = 0.99

def get_rotated_hexagon(center, radius, angle):
    """Generate hexagon vertices rotated by given angle"""
    vertices = []
    for i in range(6):
        theta = math.radians(60 * i + angle)
        x = center[0] + radius * math.sin(theta)
        y = center[1] + radius * math.cos(theta)
        vertices.append((x, y))
    return vertices

def reflect_velocity(vel, normal):
    """Reflect velocity vector over surface normal"""
    dot = vel[0] * normal[0] + vel[1] * normal[1]
    return [
        vel[0] - 2 * dot * normal[0],
        vel[1] - 2 * dot * normal[1]
    ]

def closest_point_on_line(point, line_start, line_end):
    """手动实现线段最近点计算"""
    line_vec = (line_end[0] - line_start[0], line_end[1] - line_start[1])
    point_vec = (point[0] - line_start[0], point[1] - line_start[1])
    line_len_sq = line_vec[0]**2 + line_vec[1]**2
    
    if line_len_sq == 0:
        return line_start
    
    t = max(0, min(1, (point_vec[0]*line_vec[0] + point_vec[1]*line_vec[1]) / line_len_sq))
    return (
        line_start[0] + t*line_vec[0],
        line_start[1] + t*line_vec[1]
    )

running = True
while running:
    screen.fill((0, 0, 0))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update hexagon rotation
    hex_angle = (hex_angle + rotation_speed) % 360
    hex_vertices = get_rotated_hexagon(hex_center, hex_radius, hex_angle)
    
    # Apply physics to ball
    ball_vel[1] += gravity
    ball_vel[0] *= friction
    ball_vel[1] *= friction
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Collision detection with hexagon walls
    for i in range(6):
        a = hex_vertices[i]
        b = hex_vertices[(i+1)%6]
        
        # Calculate wall direction and normal
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        length = math.hypot(dx, dy)
        if length == 0:
            continue
            
        # Calculate inward normal (perpendicular to wall direction)
        normal = (-dy/length, dx/length)
        
        # Find closest point on wall segment to ball
        closest = closest_point_on_line(ball_pos, a, b)
        distance = math.hypot(closest[0]-ball_pos[0], closest[1]-ball_pos[1])
        
        if distance < ball_radius:
            # Reflect velocity and adjust position
            ball_vel = reflect_velocity(ball_vel, normal)
            overlap = ball_radius - distance
            ball_pos[0] += normal[0] * overlap
            ball_pos[1] += normal[1] * overlap
    
    # Draw hexagon
    pygame.draw.polygon(screen, (0, 255, 0), hex_vertices, 2)
    
    # Draw ball
    pygame.draw.circle(screen, (255, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()