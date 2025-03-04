import pygame
import random
from typing import List, Tuple, Optional
from .shapes import Shape
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
        self.fall_speed = 0.3
        self.speed_up_factor = 2
        self.speed_up_duration = 0
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("俄罗斯方块")
        self.clock = pygame.time.Clock()

    def new_shape(self) -> None:
        """生成新的方块"""
        shapes = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        if self.next_shape:
            self.current_shape = self.next_shape
        else:
            self.current_shape = Shape(random.choice(shapes))
        self.next_shape = Shape(random.choice(shapes))
        self.current_pos = [self.width // 2 - 1, 0]

    def valid_move(self, shape: List[List[int]], pos: List[int]) -> bool:
        """检查方块是否可以移动到指定位置"""
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = pos[0] + x
                    grid_y = pos[1] + y
                    if (grid_x < 0 or grid_x >= self.width or
                        grid_y >= self.height or
                        (grid_y >= 0 and self.grid[grid_y][grid_x])):
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
        """更新游戏状态"""
        if not self.current_shape:
            self.new_shape()
        
        # 处理自动下落
        self.fall_time += self.clock.get_rawtime()
        if self.fall_time / 1000 >= self.fall_speed:
            self.fall_time = 0
            new_pos = [self.current_pos[0], self.current_pos[1] + 1]
            if self.valid_move(self.current_shape.get_shape(), new_pos):
                self.current_pos = new_pos
            else:
                self.lock_shape()

    def lock_shape(self) -> None:
        """锁定当前方块到网格"""
        shape = self.current_shape.get_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_pos[0] + x
                    grid_y = self.current_pos[1] + y
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = self.current_shape.color
        
        self.clear_lines()
        self.new_shape()
        
        # 检查游戏结束
        if not self.valid_move(self.current_shape.get_shape(), self.current_pos):
            self.game_over = True

    def draw(self) -> None:
        """绘制游戏界面"""
        self.screen.fill(BACKGROUND)
        
        # 绘制网格
        draw_grid(self.screen, self.block_size, GRID_COLOR)
        
        # 绘制当前方块
        if self.current_shape:
            shape = self.current_shape.get_shape()
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        draw_block(
                            self.screen,
                            self.current_shape.color,
                            (self.current_pos[0] + x, self.current_pos[1] + y),
                            self.block_size
                        )
        
        # 绘制已锁定方块
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    draw_block(self.screen, cell, (x, y), self.block_size)
        
        # 显示积分
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

    def run(self) -> None:
        """运行游戏主循环"""
        while not self.game_over:
            self.clock.tick(60)
            self.update()
            self.draw()
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.speed_up_duration = 10
                        new_pos = [self.current_pos[0], self.current_pos[1] + 1]
                        if self.valid_move(self.current_shape.get_shape(), new_pos):
                            self.current_pos = new_pos
                    elif event.key == pygame.K_LEFT:
                        new_pos = [self.current_pos[0] - 1, self.current_pos[1]]
                        if self.valid_move(self.current_shape.get_shape(), new_pos):
                            self.current_pos = new_pos
                    elif event.key == pygame.K_RIGHT:
                        new_pos = [self.current_pos[0] + 1, self.current_pos[1]]
                        if self.valid_move(self.current_shape.get_shape(), new_pos):
                            self.current_pos = new_pos
                    elif event.key == pygame.K_UP:
                        self.current_shape.rotate()
                        if not self.valid_move(self.current_shape.get_shape(), self.current_pos):
                            self.current_shape.rotate()  # 撤销旋转
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.speed_up_duration = 0
            
            self.fall_speed = self.speed_up_factor * 0.3 if self.speed_up_duration > 0 else 0.3
            self.fall_time = 0

        # 显示游戏结束菜单
        self.show_game_over_menu()

    def show_game_over_menu(self) -> None:
        """显示游戏结束菜单"""
        self.screen.fill(BACKGROUND)
        font = pygame.font.Font(None, 72)
        game_over_text = font.render('Game Over', True, WHITE)
        self.screen.blit(game_over_text, (self.screen_width // 2 - game_over_text.get_width() // 2, self.screen_height // 2 - game_over_text.get_height() // 2 - 50))
        
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, self.screen_height // 2 - score_text.get_height() // 2 + 20))
        
        restart_text = font.render('Press R to Restart', True, WHITE)
        self.screen.blit(restart_text, (self.screen_width // 2 - restart_text.get_width() // 2, self.screen_height // 2 - restart_text.get_height() // 2 + 80))
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        self.reset_game()

    def reset_game(self) -> None:
        """重置游戏"""
        self.grid = [[0] * self.width for _ in range(self.height)]
        self.score = 0
        self.game_over = False
        self.new_shape()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()