import pygame
import random
from typing import List, Tuple, Optional
from src.common.colors import *

class MemoryGame:
    def __init__(self, width: int = 6, height: int = 6, block_size: int = 80):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen_width = width * block_size
        self.screen_height = height * block_size + 100  # 额外空间显示得分
        self.score = 0
        self.game_over = False
        self.moves = 0
        
        # 初始化卡片
        self.cards = []
        self.revealed = [[False] * width for _ in range(height)]
        self.matched = [[False] * width for _ in range(height)]
        self.selected: Optional[Tuple[int, int]] = None
        self.last_selected: Optional[Tuple[int, int]] = None
        self.hide_timer = 0
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("记忆翻牌")
        self.clock = pygame.time.Clock()
        
        # 生成卡片
        self._generate_cards()
    
    def _generate_cards(self) -> None:
        """生成配对卡片"""
        pairs = (self.width * self.height) // 2
        numbers = list(range(1, pairs + 1)) * 2
        random.shuffle(numbers)
        
        self.cards = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(numbers[i * self.width + j])
            self.cards.append(row)
    
    def _check_win(self) -> bool:
        """检查是否完成所有配对"""
        return all(all(matched for matched in row) for row in self.matched)
    
    def run(self):
        while not self.game_over:
            self.screen.fill(BACKGROUND)
            current_time = pygame.time.get_ticks()
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y < self.height * self.block_size:  # 在卡片区域内
                        col = x // self.block_size
                        row = y // self.block_size
                        if 0 <= row < self.height and 0 <= col < self.width:
                            if not self.matched[row][col] and not self.revealed[row][col]:
                                self.revealed[row][col] = True
                                if self.selected is None:
                                    self.selected = (row, col)
                                else:
                                    self.last_selected = (row, col)
                                    self.moves += 1
                                    # 检查是否配对
                                    if self.cards[self.selected[0]][self.selected[1]] == \
                                       self.cards[row][col]:
                                        self.matched[self.selected[0]][self.selected[1]] = True
                                        self.matched[row][col] = True
                                        self.score += 100
                                        self.selected = None
                                        self.last_selected = None
                                        if self._check_win():
                                            self.game_over = True
                                    else:
                                        self.hide_timer = current_time + 1000  # 1秒后隐藏
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
            
            # 检查是否需要隐藏未配对的卡片
            if self.hide_timer and current_time >= self.hide_timer:
                if self.selected and self.last_selected:
                    self.revealed[self.selected[0]][self.selected[1]] = False
                    self.revealed[self.last_selected[0]][self.last_selected[1]] = False
                self.selected = None
                self.last_selected = None
                self.hide_timer = 0
            
            # 绘制卡片
            for i in range(self.height):
                for j in range(self.width):
                    rect = pygame.Rect(j * self.block_size + 5,
                                     i * self.block_size + 5,
                                     self.block_size - 10,
                                     self.block_size - 10)
                    
                    if self.matched[i][j]:
                        pygame.draw.rect(self.screen, GREEN, rect)
                        font = pygame.font.Font(None, 48)
                        text = font.render(str(self.cards[i][j]), True, WHITE)
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)
                    elif self.revealed[i][j]:
                        pygame.draw.rect(self.screen, BLUE, rect)
                        font = pygame.font.Font(None, 48)
                        text = font.render(str(self.cards[i][j]), True, WHITE)
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)
                    else:
                        pygame.draw.rect(self.screen, GRAY, rect)
            
            # 显示得分和移动次数
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
            score_text = font.render(f'得分: {self.score}', True, WHITE)
            moves_text = font.render(f'移动次数: {self.moves}', True, WHITE)
            self.screen.blit(score_text, (10, self.height * self.block_size + 10))
            self.screen.blit(moves_text, (self.screen_width - 200, self.height * self.block_size + 10))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # 游戏结束处理
        while True:
            self.screen.fill(BACKGROUND)
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
            text = font.render(f'游戏完成！得分: {self.score}', True, WHITE)
            moves_text = font.render(f'总移动次数: {self.moves}', True, WHITE)
            restart_text = font.render('按 R 重新开始', True, WHITE)
            menu_text = font.render('按 ESC 返回菜单', True, WHITE)
            
            text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 90))
            moves_rect = moves_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 30))
            restart_rect = restart_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 30))
            menu_rect = menu_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 90))
            
            self.screen.blit(text, text_rect)
            self.screen.blit(moves_text, moves_rect)
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