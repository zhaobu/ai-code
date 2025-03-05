import pygame
import random
from typing import List, Optional
from src.common.colors import *

class SudokuGame:
    def __init__(self, block_size: int = 60):
        self.block_size = block_size
        self.grid_size = 9
        self.screen_width = self.grid_size * block_size
        self.screen_height = self.grid_size * block_size + 100  # 额外空间显示按钮
        self.game_over = False
        self.selected_cell = None
        self.difficulty = 30  # 初始挖空数量
        
        # 初始化数独面板
        self.original_grid = [[0] * 9 for _ in range(9)]
        self.player_grid = [[0] * 9 for _ in range(9)]
        self.fixed_cells = [[False] * 9 for _ in range(9)]
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("数独")
        self.clock = pygame.time.Clock()
        
        # 生成新游戏
        self._generate_puzzle()
    
    def _is_valid(self, grid: List[List[int]], row: int, col: int, num: int) -> bool:
        """检查在指定位置放置数字是否合法"""
        # 检查行
        if num in grid[row]:
            return False
        
        # 检查列
        if num in [grid[i][col] for i in range(9)]:
            return False
        
        # 检查3x3方格
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if grid[i][j] == num:
                    return False
        
        return True
    
    def _solve(self, grid: List[List[int]], row: int = 0, col: int = 0) -> bool:
        """使用回溯法解数独"""
        if col == 9:
            row += 1
            col = 0
        
        if row == 9:
            return True
        
        if grid[row][col] != 0:
            return self._solve(grid, row, col + 1)
        
        for num in range(1, 10):
            if self._is_valid(grid, row, col, num):
                grid[row][col] = num
                if self._solve(grid, row, col + 1):
                    return True
                grid[row][col] = 0
        
        return False
    
    def _generate_puzzle(self) -> None:
        """生成新的数独谜题"""
        # 生成完整的解
        self._solve(self.original_grid)
        
        # 复制到玩家网格
        for i in range(9):
            for j in range(9):
                self.player_grid[i][j] = self.original_grid[i][j]
        
        # 随机挖空
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        for i, j in cells[:self.difficulty]:
            self.player_grid[i][j] = 0
            self.fixed_cells[i][j] = False
        
        # 标记固定的单元格
        for i in range(9):
            for j in range(9):
                if self.player_grid[i][j] != 0:
                    self.fixed_cells[i][j] = True
    
    def _check_win(self) -> bool:
        """检查是否完成数独"""
        for i in range(9):
            for j in range(9):
                if self.player_grid[i][j] != self.original_grid[i][j]:
                    return False
        return True
    
    def run(self):
        while not self.game_over:
            self.screen.fill(WHITE)
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y < self.grid_size * self.block_size:  # 在网格范围内
                        col = x // self.block_size
                        row = y // self.block_size
                        if 0 <= row < 9 and 0 <= col < 9 and not self.fixed_cells[row][col]:
                            self.selected_cell = (row, col)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
                    elif self.selected_cell and not self.fixed_cells[self.selected_cell[0]][self.selected_cell[1]]:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                        pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                            num = int(event.unicode)
                            row, col = self.selected_cell
                            self.player_grid[row][col] = num
                            if self._check_win():
                                self.game_over = True
                        elif event.key == pygame.K_BACKSPACE:
                            row, col = self.selected_cell
                            self.player_grid[row][col] = 0
            
            # 绘制网格线
            for i in range(self.grid_size + 1):
                line_width = 3 if i % 3 == 0 else 1
                pygame.draw.line(self.screen, BLACK, (i * self.block_size, 0),
                               (i * self.block_size, self.grid_size * self.block_size), line_width)
                pygame.draw.line(self.screen, BLACK, (0, i * self.block_size),
                               (self.grid_size * self.block_size, i * self.block_size), line_width)
            
            # 绘制数字
            font = pygame.font.Font(None, 48)
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if self.player_grid[i][j] != 0:
                        color = BLUE if self.fixed_cells[i][j] else BLACK
                        text = font.render(str(self.player_grid[i][j]), True, color)
                        text_rect = text.get_rect(center=(j * self.block_size + self.block_size//2,
                                                         i * self.block_size + self.block_size//2))
                        self.screen.blit(text, text_rect)
            
            # 绘制选中的单元格
            if self.selected_cell:
                row, col = self.selected_cell
                pygame.draw.rect(self.screen, RED,
                               (col * self.block_size, row * self.block_size,
                                self.block_size, self.block_size), 3)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # 游戏胜利处理
        while True:
            self.screen.fill(WHITE)
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
            text = font.render('恭喜完成数独！', True, BLACK)
            restart_text = font.render('按 R 重新开始', True, BLACK)
            menu_text = font.render('按 ESC 返回菜单', True, BLACK)
            
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
                        self.__init__(self.block_size)
                        self.run()
                        return
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return