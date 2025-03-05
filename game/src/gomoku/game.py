import pygame
import random
from typing import List, Tuple, Optional
from src.common.colors import *

class GomokuGame:
    def __init__(self, board_size: int = 15, block_size: int = 40):
        self.board_size = board_size
        self.block_size = block_size
        self.margin = 40  # 棋盘边距
        self.screen_width = board_size * block_size + 2 * self.margin
        self.screen_height = board_size * block_size + 2 * self.margin
        self.game_over = False
        self.is_black_turn = True  # True表示黑棋回合
        self.winner = None
        self.ai_enabled = True  # 启用AI对战
        
        # 初始化棋盘
        self.board = [[None] * board_size for _ in range(board_size)]
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("五子棋")
        self.clock = pygame.time.Clock()
    
    def _get_board_pos(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """将鼠标坐标转换为棋盘坐标"""
        x, y = mouse_pos
        board_x = round((x - self.margin) / self.block_size)
        board_y = round((y - self.margin) / self.block_size)
        if 0 <= board_x < self.board_size and 0 <= board_y < self.board_size:
            return board_x, board_y
        return None
    
    def _check_win(self, x: int, y: int, is_black: bool) -> bool:
        """检查是否获胜"""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平、垂直、对角线
        for dx, dy in directions:
            count = 1
            # 正向检查
            for i in range(1, 5):
                new_x, new_y = x + dx * i, y + dy * i
                if not (0 <= new_x < self.board_size and 0 <= new_y < self.board_size):
                    break
                if self.board[new_y][new_x] != is_black:
                    break
                count += 1
            # 反向检查
            for i in range(1, 5):
                new_x, new_y = x - dx * i, y - dy * i
                if not (0 <= new_x < self.board_size and 0 <= new_y < self.board_size):
                    break
                if self.board[new_y][new_x] != is_black:
                    break
                count += 1
            if count >= 5:
                return True
        return False
    
    def _ai_move(self) -> None:
        """AI下棋"""
        # 简单的AI策略：随机选择一个空位
        empty_positions = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] is None:
                    empty_positions.append((x, y))
        
        if empty_positions:
            x, y = random.choice(empty_positions)
            self.board[y][x] = False  # AI使用白棋
            if self._check_win(x, y, False):
                self.game_over = True
                self.winner = False
            self.is_black_turn = True
    
    def run(self):
        while True:
            self.screen.fill((240, 240, 240))  # 使用浅灰色作为背景色
            
            # 绘制棋盘背景
            board_rect = pygame.Rect(self.margin - 5, self.margin - 5,
                                   self.board_size * self.block_size + 10,
                                   self.board_size * self.block_size + 10)
            pygame.draw.rect(self.screen, (210, 180, 140), board_rect)  # 使用实木色调
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    if self.is_black_turn:  # 玩家回合
                        pos = self._get_board_pos(event.pos)
                        if pos and self.board[pos[1]][pos[0]] is None:
                            x, y = pos
                            self.board[y][x] = True  # 黑棋
                            if self._check_win(x, y, True):
                                self.game_over = True
                                self.winner = True
                            else:
                                self.is_black_turn = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.board_size, self.block_size)
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
            
            # AI回合
            if not self.game_over and not self.is_black_turn and self.ai_enabled:
                self._ai_move()
            
            # 绘制棋盘
            for i in range(self.board_size):
                # 绘制横线
                line_width = 2 if i == 0 or i == self.board_size - 1 else 1
                pygame.draw.line(self.screen, (0, 0, 0),
                               (self.margin, self.margin + i * self.block_size),
                               (self.screen_width - self.margin, self.margin + i * self.block_size), line_width)
                # 绘制竖线
                pygame.draw.line(self.screen, (0, 0, 0),
                               (self.margin + i * self.block_size, self.margin),
                               (self.margin + i * self.block_size, self.screen_height - self.margin), line_width)
            
            # 绘制棋子
            for y in range(self.board_size):
                for x in range(self.board_size):
                    if self.board[y][x] is not None:
                        color = BLACK if self.board[y][x] else WHITE
                        pos = (self.margin + x * self.block_size,
                              self.margin + y * self.block_size)
                        # 绘制棋子阴影
                        shadow_pos = (pos[0] + 2, pos[1] + 2)
                        pygame.draw.circle(self.screen, (128, 128, 128), shadow_pos, self.block_size // 2 - 2)
                        # 绘制棋子
                        pygame.draw.circle(self.screen, color, pos, self.block_size // 2 - 2)
                        # 添加高光效果
                        highlight_pos = (pos[0] - 2, pos[1] - 2)
                        highlight_color = (255, 255, 255) if color == BLACK else (220, 220, 220)
                        pygame.draw.circle(self.screen, highlight_color, highlight_pos, self.block_size // 4, 2)
            
            # 游戏结束显示
            if self.game_over:
                # 创建半透明背景
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(128)
                self.screen.blit(overlay, (0, 0))
                
                font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 56)
                if self.winner is True:
                    text = font.render("黑棋胜利！", True, (255, 215, 0))  # 金色
                else:
                    text = font.render("白棋胜利！", True, (255, 215, 0))  # 金色
                
                font_small = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
                restart_text = font_small.render("按R重新开始", True, (255, 255, 255))
                menu_text = font_small.render("按ESC返回菜单", True, (255, 255, 255))
                
                text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 60))
                restart_rect = restart_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
                menu_rect = menu_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 60))
                
                self.screen.blit(text, text_rect)
                self.screen.blit(restart_text, restart_rect)
                self.screen.blit(menu_text, menu_rect)
            
            pygame.display.flip()
            self.clock.tick(60)