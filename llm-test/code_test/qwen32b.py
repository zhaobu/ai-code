import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
CX, CY = WIDTH // 2, HEIGHT // 2
HEX_RADIUS = 200  # Radius of the hexagon
BALL_RADIUS = 10

# Ball properties
ball_x, ball_y = CX, CY - 150  # Starting position above center
ball_vx, ball_vy = 5.0, 0.0    # Initial velocity

# Physics parameters
GRAVITY = 0.5  # Acceleration per second (downward)
FRICTION = 0.1  # Damping factor per second
COEFF_RESTITUTION = 0.8  # Bounce factor

# Hexagon rotation
ANGULAR_SPEED = 0.5  # Radians per second (adjust speed)
rotation_angle = 0.0  # Current rotation angle

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def main():
    global ball_x, ball_y, ball_vx, ball_vy, rotation_angle  # Add this line
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update rotation angle
        rotation_angle += ANGULAR_SPEED * dt

        # Calculate hexagon vertices
        vertices = []
        for i in range(6):
            angle = math.radians(i * 60) + rotation_angle
            x = CX + HEX_RADIUS * math.cos(angle)
            y = CY + HEX_RADIUS * math.sin(angle)
            vertices.append((x, y))

        # Update ball's velocity and position
        # Apply gravity
        ball_vy += GRAVITY * dt

        # Apply friction (damping on horizontal velocity)
        ball_vx *= (1 - FRICTION * dt)

        # Update position
        ball_x += ball_vx * dt
        ball_y += ball_vy * dt

        # Collision detection and response
        collision = False
        for i in range(6):
            A = vertices[i]
            B = vertices[(i+1) % 6]

            Ax, Ay = A
            Bx, By = B

            # Edge vector AB
            ABx = Bx - Ax
            ABy = By - Ay

            # Vector from A to ball
            ACx = ball_x - Ax
            ACy = ball_y - Ay

            dot_AC_AB = ACx * ABx + ACy * ABy
            if dot_AC_AB <= 0:
                # Closest point is A
                closest_x, closest_y = Ax, Ay
            else:
                length_sq = ABx**2 + ABy**2
                if dot_AC_AB >= length_sq:
                    # Closest point is B
                    closest_x, closest_y = Bx, By
                else:
                    # Closest point on the segment
                    t = dot_AC_AB / length_sq
                    closest_x = Ax + t * ABx
                    closest_y = Ay + t * ABy

            # Compute distance squared to the closest point
            dx = ball_x - closest_x
            dy = ball_y - closest_y
            distance_sq = dx**2 + dy**2
            if distance_sq < BALL_RADIUS**2 + 1e-6:  # Collision detected
                # Compute outward normal vector
                normal_x = -ABy  # -ABy
                normal_y = ABx   # ABx
                normal_length = math.hypot(normal_x, normal_y)
                nx = normal_x / normal_length
                ny = normal_y / normal_length

                # Compute wall's velocity at closest point
                dx_p = closest_x - CX
                dy_p = closest_y - CY
                omega = ANGULAR_SPEED
                v_wall_x = dy_p * omega
                v_wall_y = -dx_p * omega

                # Relative velocity of the ball to the wall
                v_ball = (ball_vx, ball_vy)
                v_wall = (v_wall_x, v_wall_y)
                v_rel_x = v_ball[0] - v_wall[0]
                v_rel_y = v_ball[1] - v_wall[1]

                # Normal component of relative velocity
                vn = v_rel_x * nx + v_rel_y * ny

                # New velocity after collision
                e = COEFF_RESTITUTION
                new_vx = ball_vx - (1 + e) * vn * nx
                new_vy = ball_vy - (1 + e) * vn * ny

                # Update ball's velocity and position
                ball_vx, ball_vy = new_vx, new_vy

                # Move ball to outside the edge
                distance = math.sqrt(distance_sq)
                ball_x = closest_x + nx * BALL_RADIUS * (BALL_RADIUS / distance)
                ball_y = closest_y + ny * BALL_RADIUS * (BALL_RADIUS / distance)

                collision = True
                break  # Handle first collision only

        # Draw everything
        screen.fill((0, 0, 0))
        # Draw hexagon
        pygame.draw.polygon(screen, (255, 255, 255), vertices, 2)
        # Draw ball
        pygame.draw.circle(screen, (255, 0, 0), (int(ball_x), int(ball_y)), BALL_RADIUS)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()