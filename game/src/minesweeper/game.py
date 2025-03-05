import pygame
import random
from typing import List, Tuple, Set
from src.common.colors import *
from src.common.utils import draw_block

class MinesweeperGame:
    def __init__(self, width: int = 16, height: int = 16, block_size: int = 30):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen_width = width * block_size
        self.screen_height = height * block_size + 50  # 额外空间显示地雷数
        self.mines_count = 40
        self.remaining_mines = self.mines_count
        self.score = 0
        self.game_over = False
        self.win = False
        
        # 初始化游戏网格
        self.grid = [[0] * width for _ in range(height)]
        self.revealed = [[False] * width for _ in range(height)]
        self.flagged = [[False] * width for _ in range(height)]
        self.first_click = True
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("扫雷")
        self.clock = pygame.time.Clock()
    
    def _place_mines(self, first_x: int, first_y: int) -> None:
        """放置地雷，确保第一次点击的位置不是地雷"""
        positions = [(x, y) for x in range(self.width) for y in range(self.height)
                    if (x, y) != (first_x, first_y)]
        mine_positions = random.sample(positions, self.mines_count)
        
        for x, y in mine_positions:
            self.grid[y][x] = -1
            # 更新周围数字
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < self.width and 0 <= new_y < self.height and self.grid[new_y][new_x] != -1:
                        self.grid[new_y][new_x] += 1
    
    def _reveal_cell(self, x: int, y: int) -> None:
        """揭示一个格子，如果是空格则递归揭示周围的格子"""
        if not (0 <= x < self.width and 0 <= y < self.height) or self.revealed[y][x] or self.flagged[y][x]:
            return
        
        self.revealed[y][x] = True
        if self.grid[y][x] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    self._reveal_cell(x + dx, y + dy)
    
    def _check_win(self) -> bool:
        """检查是否获胜"""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True
    
    def handle_click(self, pos: Tuple[int, int], right_click: bool = False) -> None:
        """处理鼠标点击事件"""
        if self.game_over or self.win:
            return
        
        x = pos[0] // self.block_size
        y = pos[1] // self.block_size
        
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        
        if right_click:
            if not self.revealed[y][x]:
                self.flagged[y][x] = not self.flagged[y][x]
                self.remaining_mines += -1 if self.flagged[y][x] else 1
        else:
            if self.flagged[y][x]:
                return
            
            if self.first_click:
                self._place_mines(x, y)
                self.first_click = False
            
            if self.grid[y][x] == -1:
                self.game_over = True
            else:
                self._reveal_cell(x, y)
                if self._check_win():
                    self.win = True
                    self.score = 1000 - (self.mines_count - self.remaining_mines) * 10
    
    def run(self):
        while not (self.game_over or self.win):
            self.screen.fill(BACKGROUND)
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] < self.screen_height - 50:  # 确保点击在游戏区域内
                        self.handle_click(event.pos, event.button == 3)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
            
            # 绘制网格
            for y in range(self.height):
                for x in range(self.width):
                    color = GRAY
                    if self.revealed[y][x]:
                        color = WHITE if self.grid[y][x] != -1 else RED
                    draw_block(self.screen, color, (x, y), self.block_size)
                    
                    if self.revealed[y][x] and self.grid[y][x] > 0:
                        font = pygame.font.Font(None, 36)
                        text = font.render(str(self.grid[y][x]), True, BLACK)
                        text_rect = text.get_rect(center=(
                            x * self.block_size + self.block_size // 2,
                            y * self.block_size + self.block_size // 2
                        ))
                        self.screen.blit(text, text_rect)
                    elif self.flagged[y][x]:
                        font = pygame.font.Font(None, 36)
                        text = font.render("F", True, RED)
                        text_rect = text.get_rect(center=(
                            x * self.block_size + self.block_size // 2,
                            y * self.block_size + self.block_size // 2
                        ))
                        self.screen.blit(text, text_rect)
            
            # 显示剩余地雷数
            font = pygame.font.Font(None, 36)
            mines_text = font.render(f'剩余地雷: {self.remaining_mines}', True, WHITE)
            self.screen.blit(mines_text, (10, self.screen_height - 40))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # 游戏结束处理
        while True:
            self.screen.fill(BACKGROUND)
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
            
            if self.win:
                text = font.render(f'恭喜获胜！得分: {self.score}', True, WHITE)
            else:
                text = font.render('游戏结束', True, WHITE)
            
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