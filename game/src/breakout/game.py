import pygame
from typing import List, Tuple
from src.common.colors import *
from src.common.utils import draw_block

class BreakoutGame:
    def __init__(self, width: int = 20, height: int = 25, block_size: int = 30):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen_width = width * block_size
        self.screen_height = height * block_size
        self.score = 0
        self.game_over = False
        self.lives = 3
        
        # 初始化挡板
        self.paddle_width = 4
        self.paddle_height = 1
        self.paddle_pos = [width // 2 - self.paddle_width // 2, height - 2]
        self.paddle_speed = 8
        self.moving_left = False
        self.moving_right = False
        
        # 初始化球
        self.ball_pos = [width // 2, height - 3]
        self.ball_speed = [0.3, -0.3]
        
        # 初始化砖块
        self.bricks: List[List[Tuple[int, int, int]]] = []
        self._init_bricks()
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("打砖块")
        self.clock = pygame.time.Clock()
    
    def _init_bricks(self) -> None:
        """初始化砖块布局"""
        colors = [RED, ORANGE, YELLOW, GREEN, CYAN]
        for i in range(5):
            row = []
            for j in range(self.width - 4):
                row.append(colors[i])
            self.bricks.append(row)
    
    def _check_collision(self, pos: List[float], size: List[int]) -> bool:
        """检查球与矩形的碰撞"""
        ball_rect = pygame.Rect(int(self.ball_pos[0] * self.block_size),
                              int(self.ball_pos[1] * self.block_size),
                              self.block_size, self.block_size)
        block_rect = pygame.Rect(int(pos[0] * self.block_size),
                                int(pos[1] * self.block_size),
                                size[0] * self.block_size,
                                size[1] * self.block_size)
        return ball_rect.colliderect(block_rect)
    
    def update(self) -> None:
        """更新游戏状态"""
        if self.game_over:
            return
            
        # 更新挡板位置
        if self.moving_left and self.paddle_pos[0] > 0:
            self.paddle_pos[0] -= self.paddle_speed * 0.016
        if self.moving_right and self.paddle_pos[0] < self.width - self.paddle_width:
            self.paddle_pos[0] += self.paddle_speed * 0.016
        
        # 更新球的位置
        new_ball_pos = [self.ball_pos[0] + self.ball_speed[0],
                       self.ball_pos[1] + self.ball_speed[1]]
        
        # 检查球与墙壁的碰撞
        if new_ball_pos[0] <= 0 or new_ball_pos[0] >= self.width - 1:
            self.ball_speed[0] *= -1
        if new_ball_pos[1] <= 0:
            self.ball_speed[1] *= -1
        
        # 检查球是否掉落
        if new_ball_pos[1] >= self.height:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                new_ball_pos = [self.width // 2, self.height - 3]
                self.ball_speed = [0.3, -0.3]
        
        # 检查球与挡板的碰撞
        if self._check_collision(self.paddle_pos, [self.paddle_width, self.paddle_height]):
            self.ball_speed[1] *= -1
            # 根据击中挡板的位置调整反弹角度
            relative_intersect = (self.ball_pos[0] - self.paddle_pos[0]) / self.paddle_width
            self.ball_speed[0] = relative_intersect * 2
        
        # 检查球与砖块的碰撞
        for i, row in enumerate(self.bricks):
            for j, brick in enumerate(row):
                if brick and self._check_collision([j + 2, i + 2], [1, 1]):
                    self.bricks[i][j] = 0
                    self.ball_speed[1] *= -1
                    self.score += 10
                    break
        
        self.ball_pos = new_ball_pos
    
    def run(self):
        while not self.game_over:
            self.screen.fill(BACKGROUND)
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = True
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = False
            
            self.update()
            
            # 绘制砖块
            for i, row in enumerate(self.bricks):
                for j, color in enumerate(row):
                    if color:
                        draw_block(self.screen, color, (j + 2, i + 2), self.block_size)
            
            # 绘制挡板
            for x in range(self.paddle_width):
                draw_block(self.screen, WHITE,
                          (self.paddle_pos[0] + x, self.paddle_pos[1]),
                          self.block_size)
            
            # 绘制球
            draw_block(self.screen, WHITE,
                      (int(self.ball_pos[0]), int(self.ball_pos[1])),
                      self.block_size)
            
            # 显示得分和生命值
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'得分: {self.score}', True, WHITE)
            lives_text = font.render(f'生命: {self.lives}', True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (self.screen_width - 120, 10))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # 游戏结束处理
        while True:
            self.screen.fill(BACKGROUND)
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
            text = font.render(f'最终得分: {self.score}', True, WHITE)
            restart_text = font.render('按 R 重新开始', True, WHITE)
            menu_text = font.render('按 ESC 返回菜单', True, WHITE)
            
            text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 60))
            restart_rect = restart_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            menu_rect = menu_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 60))
            
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_text, restart_rect)
            self.screen.blit(menu_text, menu_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.width, self.height, self.block_size)
                        self.run()
                        return
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return