import pygame
import math
import sys

# Constants
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
FRICTION = 0.99
BALL_RADIUS = 15
HEX_RADIUS = 250
ROTATION_SPEED = 1

class Hexagon:
    def __init__(self):
        self.angle = 0
        self.points = self.calculate_points()

    def calculate_points(self):
        return [(HEX_RADIUS * math.cos(math.radians(60 * i + self.angle)) + WIDTH//2,
                 HEX_RADIUS * math.sin(math.radians(60 * i + self.angle)) + HEIGHT//2)
                for i in range(6)]

    def rotate(self):
        self.angle = (self.angle + ROTATION_SPEED) % 360
        self.points = self.calculate_points()

    def draw(self, surface):
        pygame.draw.polygon(surface, (255, 255, 255), self.points, 2)

class Ball:
    def __init__(self):
        self.x, self.y = WIDTH//2, HEIGHT//2 - HEX_RADIUS + BALL_RADIUS + 50
        self.vx, self.vy = 5, 0

    def update(self, hex_points):
        # Apply gravity
        self.vy += GRAVITY
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Check collision with hexagon walls
        for i in range(6):
            x1, y1 = hex_points[i]
            x2, y2 = hex_points[(i+1)%6]
            
            # Line equation: (y2 - y1)x - (x2 - x1)y + (x2y1 - x1y2) = 0
            A = y2 - y1
            B = x1 - x2
            C = x2*y1 - x1*y2
            
            # Distance from ball to line
            dist = abs(A*self.x + B*self.y + C) / math.sqrt(A*A + B*B)
            
            if dist <= BALL_RADIUS:
                # Calculate normal vector
                normal = math.atan2(y2 - y1, x2 - x1) + math.pi/2
                
                # Reflect velocity vector
                speed = math.hypot(self.vx, self.vy)
                angle = math.atan2(self.vy, self.vx)
                new_angle = 2*normal - angle
                
                self.vx = speed * math.cos(new_angle) * FRICTION
                self.vy = speed * math.sin(new_angle) * FRICTION
                
                # Move ball outside the wall
                self.x += self.vx
                self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), BALL_RADIUS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    hexagon = Hexagon()
    ball = Ball()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((0, 0, 0))
        
        hexagon.rotate()
        hexagon.draw(screen)
        
        ball.update(hexagon.points)
        ball.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()