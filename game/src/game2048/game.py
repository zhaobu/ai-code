import pygame
import random
from typing import List, Optional
from src.common.colors import *

class Game2048:
    def __init__(self, width: int = 4, height: int = 4, block_size: int = 120):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen_width = width * block_size
        self.screen_height = height * block_size
        self.score = 0
        self.game_over = False
        self.grid = [[0] * width for _ in range(height)]
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("2048")
        self.clock = pygame.time.Clock()
        
        # 初始化游戏
        self._add_new_tile()
        self._add_new_tile()
    
    def _add_new_tile(self) -> None:
        """在空位置添加新的数字方块"""
        empty_cells = [(x, y) for x in range(self.width)
                      for y in range(self.height) if self.grid[y][x] == 0]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.grid[y][x] = 2 if random.random() < 0.9 else 4
    
    def _get_tile_color(self, value: int) -> tuple:
        """根据数字获取对应的颜色"""
        colors = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }
        return colors.get(value, (0, 0, 0))
    
    def _can_move(self) -> bool:
        """检查是否还可以移动"""
        # 检查是否有空格
        for row in self.grid:
            if 0 in row:
                return True
        
        # 检查相邻数字是否相同
        for y in range(self.height):
            for x in range(self.width):
                current = self.grid[y][x]
                if x < self.width - 1 and current == self.grid[y][x + 1]:
                    return True
                if y < self.height - 1 and current == self.grid[y + 1][x]:
                    return True
        return False
    
    def _merge_line(self, line: List[int], reverse: bool = False) -> List[int]:
        """合并一行数字"""
        if reverse:
            line = line[::-1]
        
        # 移除零
        non_zero = [x for x in line if x != 0]
        
        # 合并相同数字
        result = []
        i = 0
        while i < len(non_zero):
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                result.append(non_zero[i] * 2)
                self.score += non_zero[i] * 2
                i += 2
            else:
                result.append(non_zero[i])
                i += 1
        
        # 补零
        result.extend([0] * (len(line) - len(result)))
        
        if reverse:
            result = result[::-1]
        return result
    
    def move(self, direction: str) -> bool:
        """移动数字方块"""
        original_grid = [row[:] for row in self.grid]
        moved = False
        
        if direction in ['left', 'right']:
            for y in range(self.height):
                self.grid[y] = self._merge_line(self.grid[y], direction == 'right')
        else:  # up or down
            for x in range(self.width):
                column = [self.grid[y][x] for y in range(self.height)]
                merged = self._merge_line(column, direction == 'down')
                for y in range(self.height):
                    self.grid[y][x] = merged[y]
        
        # 检查是否有变化
        if self.grid != original_grid:
            moved = True
            self._add_new_tile()
            
            # 检查游戏是否结束
            if not self._can_move():
                self.game_over = True
        
        return moved
    
    def run(self):
        while not self.game_over:
            self.screen.fill((187, 173, 160))
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move('left')
                    elif event.key == pygame.K_RIGHT:
                        self.move('right')
                    elif event.key == pygame.K_UP:
                        self.move('up')
                    elif event.key == pygame.K_DOWN:
                        self.move('down')
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
            
            # 绘制方块
            for y in range(self.height):
                for x in range(self.width):
                    value = self.grid[y][x]
                    color = self._get_tile_color(value)
                    rect = pygame.Rect(x * self.block_size + 5,
                                     y * self.block_size + 5,
                                     self.block_size - 10,
                                     self.block_size - 10)
                    pygame.draw.rect(self.screen, color, rect, border_radius=8)
                    
                    if value != 0:
                        font_size = 48 if value < 100 else 36 if value < 1000 else 24
                        font = pygame.font.Font(None, font_size)
                        text = font.render(str(value), True, (0, 0, 0) if value <= 4 else WHITE)
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)
            
            # 显示得分
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'得分: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # 游戏结束处理
        while True:
            self.screen.fill((187, 173, 160))
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