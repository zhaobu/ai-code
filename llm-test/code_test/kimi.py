import pygame
import math
import sys

# 初始化 Pygame
pygame.init()

# 设置屏幕大小
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball Bouncing in Rotating Hexagon")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 六边形参数
hexagon_center = (screen_width // 2, screen_height // 2)
hexagon_radius = 200
hexagon_rotation_speed = 0.005  # 弧度/帧
hexagon_angle = 0

# 球参数
ball_pos = [screen_width // 2, screen_height // 2]
ball_radius = 15
ball_velocity = [2, 2]  # 初始速度
gravity = 0.1  # 重力加速度
friction = 0.99  # 摩擦系数


# 函数：绘制六边形
def draw_hexagon(surface, color, center, radius, angle):
    points = []
    for i in range(6):
        x = center[0] + radius * math.cos(angle + i * math.pi / 3)
        y = center[1] + radius * math.sin(angle + i * math.pi / 3)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)


# 函数：检测球与六边形的碰撞
def check_collision(ball_pos, ball_radius, hexagon_center, hexagon_radius, hexagon_angle):
    # 将球的位置转换到六边形的局部坐标系
    dx = ball_pos[0] - hexagon_center[0]
    dy = ball_pos[1] - hexagon_center[1]
    rotated_x = dx * math.cos(-hexagon_angle) - dy * math.sin(-hexagon_angle)
    rotated_y = dx * math.sin(-hexagon_angle) + dy * math.cos(-hexagon_angle)

    # 检测球是否超出六边形边界
    if abs(rotated_x) > hexagon_radius or abs(rotated_y) > hexagon_radius:
        return True
    return False


# 函数：处理碰撞
def handle_collision(ball_pos, ball_velocity, hexagon_center, hexagon_radius, hexagon_angle):
    # 将球的位置转换到六边形的局部坐标系
    dx = ball_pos[0] - hexagon_center[0]
    dy = ball_pos[1] - hexagon_center[1]
    rotated_x = dx * math.cos(-hexagon_angle) - dy * math.sin(-hexagon_angle)
    rotated_y = dx * math.sin(-hexagon_angle) + dy * math.cos(-hexagon_angle)

    # 碰撞处理：简单反射
    if abs(rotated_x) > hexagon_radius:
        ball_velocity[0] = -ball_velocity[0]
    if abs(rotated_y) > hexagon_radius:
        ball_velocity[1] = -ball_velocity[1]

    # 将球的位置转换回全局坐标系
    ball_pos[0] = hexagon_center[0] + rotated_x * math.cos(hexagon_angle) - rotated_y * math.sin(hexagon_angle)
    ball_pos[1] = hexagon_center[1] + rotated_x * math.sin(hexagon_angle) + rotated_y * math.cos(hexagon_angle)


# 主循环
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新六边形角度
    hexagon_angle += hexagon_rotation_speed

    # 更新球的位置
    ball_velocity[1] += gravity  # 应用重力
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # 应用摩擦力
    ball_velocity[0] *= friction
    ball_velocity[1] *= friction

    # 检测碰撞
    if check_collision(ball_pos, ball_radius, hexagon_center, hexagon_radius, hexagon_angle):
        handle_collision(ball_pos, ball_velocity, hexagon_center, hexagon_radius, hexagon_angle)

    # 绘制
    screen.fill(BLACK)
    draw_hexagon(screen, WHITE, hexagon_center, hexagon_radius, hexagon_angle)
    pygame.draw.circle(screen, RED, ball_pos, ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
