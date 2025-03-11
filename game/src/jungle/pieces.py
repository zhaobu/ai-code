import pygame
from .constants import COLORS, CELL_SIZE, RANK_NAMES

class Piece:
    def __init__(self, rank, team, row, col):
        self.rank = rank
        self.team = team
        self.row = row
        self.col = col
        self.selected = False
        self.font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 16)

    def draw(self, win, x, y):
        # 绘制棋子背景
        radius = CELL_SIZE // 2 - 4
        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        
        # 绘制选中状态
        if self.selected:
            pygame.draw.circle(win, COLORS['selected'], center, radius + 2)
        
        # 绘制棋子
        color = (255, 0, 0) if self.team == 'red' else (0, 0, 255)
        pygame.draw.circle(win, color, center, radius)
        
        # 绘制棋子等级名称
        text = RANK_NAMES.get(self.rank, str(self.rank))
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=center)
        win.blit(text_surface, text_rect)

    def move(self, row, col):
        """移动棋子到新位置"""
        self.row = row
        self.col = col

    def can_capture(self, target):
        """判断是否可以吃掉目标棋子"""
        # 工兵可以炸掉地雷
        if self.rank == 2 and target.rank == 10:
            return True
            
        # 地雷不能移动，所以不能吃子
        if self.rank == 10:
            return False
            
        # 军旗不能吃子
        if self.rank == 12:
            return False
            
        # 一般规则：大子可以吃小子
        if target.rank == 12:  # 可以吃军旗
            return True
            
        return self.rank >= target.rank
