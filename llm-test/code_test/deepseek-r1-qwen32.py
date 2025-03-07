import pygame
import math
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.02

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
 
# Ball properties
BALL_RADIUS = 10
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [0, 0]
ball_acc = [0, GRAVITY]

# Hexagon properties
HEX_SIZE = 100
hex_pos = [WIDTH // 2, HEIGHT // 2]
hex_rotation = 0
hex_spin = 1  # Rotation speed

def create_hexagon(center, size):
    points = []
    for i in range(6):
        angle = (i * 60 + hex_rotation) * math.pi / 180
        x = center[0] + size * math.cos(angle)
        y = center[1] + size * math.sin(angle)
        points.append((x, y))
    return points

def point_on_segment(px, py, x1, y1, x2, y2):
    cross = (x2 - x1)*(py - y1) - (y2 - y1)*(px - x1)
    if abs(cross) > 1e-10:
        return False
    dot = (x2 - x1)*(px - x1) + (y2 - y1)*(py - y1)
    if dot < 0:
        return False
    squared_length = (x2 - x1)**2 + (y2 - y1)**2
    if dot > squared_length:
        return False
    return True

def distance_point_segment(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx**2 + dy**2)
    t = max(0, min(1, t))
    nearest_x = x1 + t * dx
    nearest_y = y1 + t * dy
    return math.hypot(nearest_x - px, nearest_y - py)

def check_collision():
    hex_points = create_hexagon(hex_pos, HEX_SIZE)
    for i in range(len(hex_points)):
        x1, y1 = hex_points[i]
        x2, y2 = hex_points[(i+1)%len(hex_points)]
        dist = distance_point_segment(ball_pos[0], ball_pos[1], x1, y1, x2, y2)
        if dist < BALL_RADIUS:
            nx = (y2 - y1)
            ny = (x1 - x2)
            mag = math.hypot(nx, ny)
            if mag == 0:
                continue
            nx /= mag
            ny /= mag
            dp = ball_vel[0]*nx + ball_vel[1]*ny
            if dp < 0:
                ball_vel[0] -= 2 * dp * nx
                ball_vel[1] -= 2 * dp * ny
            if point_on_segment(ball_pos[0], ball_pos[1], x1, y1, x2, y2):
                if ball_vel[0] * (x2 - x1) + ball_vel[1] * (y2 - y1) > 0:
                    ball_vel[0] *= -FRICTION
                    ball_vel[1] *= FRICTION

def apply_gravity():
    ball_vel[1] += ball_acc[1]

def update_ball():
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    if ball_pos[0] < BALL_RADIUS or ball_pos[0] > WIDTH - BALL_RADIUS:
        ball_pos[0] = max(BALL_RADIUS, min(ball_pos[0], WIDTH - BALL_RADIUS))
        ball_vel[0] *= -FRICTION
        if abs(ball_vel[0]) < 0.1:
            ball_vel[0] = 0

    if ball_pos[1] < BALL_RADIUS or ball_pos[1] > HEIGHT - BALL_RADIUS:
        ball_pos[1] = max(BALL_RADIUS, min(ball_pos[1], HEIGHT - BALL_RADIUS))
        ball_vel[1] *= -FRICTION
        if abs(ball_vel[1]) < 0.1:
            ball_vel[1] = 0

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        # Update hexagon rotation
        global hex_rotation
        hex_rotation += hex_spin
        hex_rotation %= 360

        # Update ball physics
        apply_gravity()
        update_ball()
        check_collision()

        # Draw hexagon
        hex_points = create_hexagon(hex_pos, HEX_SIZE)
        pygame.draw.polygon(screen, GREEN, hex_points, 2)

        # Draw ball
        pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
