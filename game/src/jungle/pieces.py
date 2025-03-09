import pygame
from .constants import COLORS, CELL_SIZE, RANK_NAMES

class Piece:
    def __init__(self, rank, team, row, col):
        self.rank = rank
        self.team = team
        self.row = row
        self.col = col
        self.selected = False

    def draw(self, win, x, y):
        center_x = x + CELL_SIZE//2
        center_y = y + CELL_SIZE//2
        
        # Draw piece base
        color = COLORS['red_team'] if self.team == 'red' else COLORS['blue_team']
        pygame.draw.circle(win, color, (center_x, center_y), CELL_SIZE//3)
        
        # Draw rank text with Chinese font
        font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)
        text = font.render(RANK_NAMES[self.rank], True, COLORS['text'])
        text_rect = text.get_rect(center=(center_x, center_y))
        win.blit(text, text_rect)
        
        # Draw selection highlight
        if self.selected:
            pygame.draw.circle(win, COLORS['highlight'], (center_x, center_y), CELL_SIZE//3 + 2, 3)

    def move(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"{self.team} {RANK_NAMES[self.rank]} ({self.row},{self.col})"

    def can_capture(self, other):
        if self.rank == 11:  # 炸弹可以炸任何棋子
            return True
        if other.rank == 11:  # 炸弹可以被任何棋子引爆
            return True
        if other.rank == 10:  # 地雷只能被工兵排除
            return self.rank == 1
        if other.rank == 12:  # 军旗可以被任何移动的棋子夺取
            return True
        return self.rank > other.rank
