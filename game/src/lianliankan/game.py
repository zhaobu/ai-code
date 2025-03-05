import pygame
import random
from typing import List, Tuple, Optional
from src.common.colors import *

class LianLianKanGame:
    def __init__(self, width: int = 8, height: int = 8, block_size: int = 60):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.margin = 40  # 边距
        self.screen_width = width * block_size + 2 * self.margin
        self.screen_height = height * block_size + 2 * self.margin + 100  # 额外空间显示得分和时间
        self.score = 0
        self.game_over = False
        self.time_left = 300  # 5分钟时间限制
        self.last_time = 0
        
        # 初始化游戏板
        self.board = []
        self.selected = None
        self._init_board()
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("连连看")
        self.clock = pygame.time.Clock()
    
    def _init_board(self) -> None:
        """初始化游戏板"""
        # 生成配对的图案
        pairs = (self.width * self.height) // 2
        numbers = list(range(1, pairs + 1)) * 2
        random.shuffle(numbers)
        
        # 填充游戏板
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(numbers[i * self.width + j])
            self.board.append(row)
    
    def _get_board_pos(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """将鼠标坐标转换为游戏板坐标"""
        x, y = mouse_pos
        board_x = (x - self.margin) // self.block_size
        board_y = (y - self.margin) // self.block_size
        if 0 <= board_x < self.width and 0 <= board_y < self.height:
            return board_x, board_y
        return None
    
    def _can_connect(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """检查两个位置是否可以连通"""
        # 简单版本：只检查相邻的相同数字
        x1, y1 = pos1
        x2, y2 = pos2
        if self.board[y1][x1] != self.board[y2][x2]:
            return False
        
        # 检查是否相邻
        if abs(x1 - x2) + abs(y1 - y2) == 1:
            return True
        return False
    
    def run(self):
        start_time = pygame.time.get_ticks()
        
        while not self.game_over:
            current_time = pygame.time.get_ticks()
            self.time_left = max(0, 300 - (current_time - start_time) // 1000)
            if self.time_left == 0:
                self.game_over = True
            
            self.screen.fill(BACKGROUND)
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    pos = self._get_board_pos(event.pos)
                    if pos:
                        if self.selected is None:
                            if self.board[pos[1]][pos[0]] != 0:  # 确保选中的不是空格
                                self.selected = pos
                        else:
                            if pos != self.selected:  # 确保不是点击同一个位置
                                if self._can_connect(self.selected, pos):
                                    # 消除配对
                                    x1, y1 = self.selected
                                    x2, y2 = pos
                                    self.board[y1][x1] = 0
                                    self.board[y2][x2] = 0
                                    self.score += 10
                                    # 检查游戏是否结束
                                    if all(all(cell == 0 for cell in row) for row in self.board):
                                        self.game_over = True
                            self.selected = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.width, self.height, self.block_size)
                        start_time = pygame.time.get_ticks()
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
            
            # 绘制游戏板
            for y in range(self.height):
                for x in range(self.width):
                    if self.board[y][x] != 0:
                        rect = pygame.Rect(self.margin + x * self.block_size,
                                         self.margin + y * self.block_size,
                                         self.block_size - 2,
                                         self.block_size - 2)
                        color = BLUE
                        if self.selected and (x, y) == self.selected:
                            color = RED
                        pygame.draw.rect(self.screen, color, rect)
                        # 显示数字
                        font = pygame.font.Font(None, 48)
                        text = font.render(str(self.board[y][x]), True, WHITE)
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)
            
            # 显示得分和时间
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
            score_text = font.render(f'得分: {self.score}', True, WHITE)
            time_text = font.render(f'剩余时间: {self.time_left}秒', True, WHITE)
            self.screen.blit(score_text, (10, self.screen_height - 80))
            self.screen.blit(time_text, (self.screen_width - 250, self.screen_height - 80))
            
            # 游戏结束显示
            if self.game_over:
                font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
                if self.time_left == 0:
                    text = font.render("时间到！", True, WHITE)
                else:
                    text = font.render("恭喜完成！", True, WHITE)
                score_text = font.render(f'最终得分: {self.score}', True, WHITE)
                restart_text = font.render("按R重新开始", True, WHITE)
                menu_text = font.render("按ESC返回菜单", True, WHITE)
                
                text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 90))
                score_rect = score_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 30))
                restart_rect = restart_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 30))
                menu_rect = menu_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 90))
                
                self.screen.blit(text, text_rect)
                self.screen.blit(score_text, score_rect)
                self.screen.blit(restart_text, restart_rect)
                self.screen.blit(menu_text, menu_rect)
            
            pygame.display.flip()
            self.clock.tick(60)