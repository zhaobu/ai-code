import pygame
import random
import logging
from typing import List, Tuple
from src.common.colors import *
from src.common.utils import draw_grid, draw_block

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SnakeGame:
    def __init__(self, width: int = 20, height: int = 15, block_size: int = 30):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen_width = width * block_size
        self.screen_height = height * block_size
        self.score = 0
        self.game_over = False
        self.speed = 10
        self.speed_up_factor = 2
        self.speed_up_duration = 0

        # 初始化蛇
        self.snake = [(width // 2, height // 2)]
        self.direction = (1, 0)
        self.food = self._generate_food()

        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("贪吃蛇")
        self.clock = pygame.time.Clock()

    def _generate_food(self) -> Tuple[int, int]:
        """生成食物"""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def _check_collision(self) -> bool:
        """检查碰撞"""
        head = self.snake[0]
        # 撞墙检测
        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            return True
        # 撞自身检测
        if head in self.snake[1:]:
            return True
        return False

    def update(self) -> None:
        """更新游戏状态"""
        if self.game_over:
            return

        # 计算新蛇头位置
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        # 插入新蛇头
        self.snake.insert(0, new_head)

        # 检查是否吃到食物
        if new_head == self.food:
            self.score += 10
            self.food = self._generate_food()
        else:
            # 移除蛇尾
            self.snake.pop()

        # 检查碰撞
        if self._check_collision():
            self.game_over = True

    def draw(self) -> None:
        """绘制游戏界面"""
        self.screen.fill(BACKGROUND)

        # 绘制网格
        draw_grid(self.screen, self.block_size, GRID_COLOR)

        # 绘制蛇
        for segment in self.snake:
            draw_block(self.screen, GREEN, segment, self.block_size)

        # 显示积分
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # 绘制食物
        draw_block(self.screen, RED, self.food, self.block_size)

        pygame.display.flip()
        self.clock.tick(self.speed)

    def run(self) -> None:
        """运行游戏主循环"""
        while not self.game_over:
            self.update()
            self.draw()

            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logging.debug('Game window closed by user')
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != (0, 1):
                        self.direction = (0, -1)
                        self.speed_up_duration = 10
                    elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                        self.direction = (0, 1)
                        self.speed_up_duration = 10
                    elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.direction = (-1, 0)
                        self.speed_up_duration = 10
                    elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                        self.direction = (1, 0)
                        self.speed_up_duration = 10

            self.speed = self.speed * self.speed_up_factor if self.speed_up_duration > 0 else 10
            self.speed_up_duration = max(0, self.speed_up_duration - 1)
