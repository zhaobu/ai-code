import pygame
import random
from typing import List
from src.tetris.shapes import Shape
from src.common.colors import *
from src.common.utils import draw_grid, draw_block

class TetrisGame:
    def __init__(self, width: int = 10, height: int = 20, block_size: int = 30):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen_width = width * block_size
        self.screen_height = height * block_size
        self.grid = [[0] * width for _ in range(height)]
        self.current_shape: Optional[Shape] = None
        self.next_shape: Optional[Shape] = None
        self.score = 0
        self.game_over = False
        self.fall_time = 0
        self.last_time = pygame.time.get_ticks()
        self.fall_speed = 0.3
        self.speed_up_factor = 2
        self.speed_up_duration = 0
        self.speed_up = False  # 加速状态标志
        self.moving_left = False
        self.moving_right = False
        self.last_move_time = 0
        self.move_interval = 150  # 延长移动间隔到150毫秒
        self.initial_delay = 250  # 增加初始延迟到250毫秒
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("俄罗斯方块")
        self.clock = pygame.time.Clock()
        self.new_shape()  # 初始化时生成第一个方块

    def new_shape(self) -> None:
        """生成新的方块"""
        shapes = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        if self.next_shape:
            self.current_shape = self.next_shape
        else:
            self.current_shape = Shape(random.choice(shapes))
        self.next_shape = Shape(random.choice(shapes))
        # 根据当前形状宽度计算居中位置
        shape_width = len(self.current_shape.get_shape()[0])
        self.current_pos = [self.width // 2 - shape_width // 2, 0]

    def valid_move(self, shape: List[List[int]], pos: List[int]) -> bool:
        """检查方块是否可以移动到指定位置"""
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = pos[0] + x
                    grid_y = pos[1] + y
                    # 严格检查横向边界和纵向位置
                    if grid_x < 0 or grid_x >= self.width or \
                       grid_y >= self.height or \
                       (grid_y >= 0 and self.grid[grid_y][grid_x]):
                        return False
        return True

    def clear_lines(self) -> None:
        """消除完整行并更新分数"""
        lines_cleared = 0
        for y in range(self.height - 1, -1, -1):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * self.width)
                lines_cleared += 1
        
        # 更新分数
        if lines_cleared > 0:
            self.score += lines_cleared * 100

    def update(self) -> None:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.last_time
        self.fall_time += delta_time  # 保持毫秒单位
        self.last_time = current_time
        
        if not self.current_shape:
            self.new_shape()
        
        # 根据加速状态调整下落间隔
        speed = self.fall_speed * 1000 / (3 if self.speed_up else 1)
        if self.fall_time >= speed:
            self.fall_time = 0
            new_pos = [self.current_pos[0], self.current_pos[1] + 1]
            if self.valid_move(self.current_shape.get_shape(), new_pos):
                self.current_pos = new_pos
            else:
                self.lock_shape()

    def _check_game_over(self, shape) -> None:
        """检查游戏是否结束"""
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = self.current_pos[1] + y
                    if grid_y <= 1:
                        self.game_over = True
                        return

    def lock_shape(self) -> None:
        """锁定当前方块到网格"""
        shape = self.current_shape.get_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_pos[0] + x
                    grid_y = self.current_pos[1] + y
                    if grid_y >= 0:
                        # 确保写入颜色到网格时使用正确的坐标
                        try:
                            self.grid[grid_y][grid_x] = self.current_shape.color
                        except IndexError:
                            self.game_over = True
                            return
        
        self.clear_lines()
        self.new_shape()
        
        # 立即检查新方块是否合法
        if not self.valid_move(self.current_shape.get_shape(), self.current_pos):
            self._check_game_over(self.current_shape.get_shape())
            if self.game_over:
                self.current_shape = None
    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            
            # 显示游戏结束提示
            while self.game_over:
                self.screen.fill(BLACK)
                if not hasattr(self, 'game_over_time'):
                    self.game_over_time = pygame.time.get_ticks()
                # 渲染得分和按钮
                font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
                text = font.render(f'最终得分: {self.score}', True, WHITE)
                restart_text = font.render('按 R 重新开始', True, WHITE)
                menu_text = font.render('按 ESC 返回菜单', True, WHITE)
                
                # 居中显示所有元素
                self.screen.blit(text, (self.screen_width//2 - text.get_width()//2, self.screen_height//2 - 80))
                self.screen.blit(restart_text, (self.screen_width//2 - restart_text.get_width()//2, self.screen_height//2))
                self.screen.blit(menu_text, (self.screen_width//2 - menu_text.get_width()//2, self.screen_height//2 + 60))
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
                            return
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game_over = False
                            return
                        elif event.key == pygame.K_r:  # 重新开始游戏
                            self.__init__(self.width, self.height, self.block_size)
                            self.game_over = False
                            self.run()
                            return
                continue
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = True
                    elif event.key == pygame.K_UP:
                        # 旋转前保存原始状态
                        original_rotation = self.current_shape.rotation_index
                        self.current_shape.rotate()
                        if not self.valid_move(self.current_shape.get_shape(), self.current_pos):
                            self.current_shape.rotation_index = original_rotation
                    elif event.key == pygame.K_DOWN:
                        self.speed_up = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.speed_up = False
                    elif event.key == pygame.K_LEFT:
                        self.moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = False
            # 游戏更新逻辑
            current_time = pygame.time.get_ticks()
            if (self.moving_left or self.moving_right) and \
               (current_time - self.last_move_time > (self.initial_delay if self.last_move_time == 0 else self.move_interval)):
                new_pos = self.current_pos.copy()
                if self.moving_left:
                    new_pos[0] -= 1
                elif self.moving_right:
                    new_pos[0] += 1
                
                if self.valid_move(self.current_shape.get_shape(), new_pos):
                    self.current_pos = new_pos
                self.last_move_time = current_time
            
            self.update()
            
            # 渲染游戏界面
            draw_grid(self.screen, self.block_size, GRAY)
            
            # 显示积分
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (self.screen_width - 200, 10))
            
            # 绘制所有已锁定的方块
            for y, row in enumerate(self.grid):
                for x, color in enumerate(row):
                    if color:
                        draw_block(
                            self.screen,
                            color,
                            (x, y),
                            self.block_size
                        )
            
            # 绘制当前下落中的方块
            if self.current_shape and not self.game_over:
                for y, row in enumerate(self.current_shape.get_shape()):
                    for x, cell in enumerate(row):
                        if cell:
                            draw_block(
                                self.screen,
                                self.current_shape.color,
                                (self.current_pos[0] + x, self.current_pos[1] + y),
                                self.block_size
                            )
            
            pygame.display.flip()
            self.clock.tick(60)