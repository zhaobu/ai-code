import pygame
import sys
from .pieces import Piece
from .constants import *

class JungleGame:
    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.selected_piece = None
        self.turn = 'red'
        self.game_over = False
        self.history = []
        self._init_pieces()

    def _init_pieces(self):
        # 初始化棋子（保持原有初始化代码）
        red_pieces = [
            (12, 0, 3), (9, 0, 0), (8, 0, 6),
            (7, 1, 1), (7, 1, 5),
            (6, 2, 2), (6, 2, 4),
            (5, 3, 3),
            (4, 2, 0), (4, 2, 6),
            (3, 3, 1), (3, 3, 5),
            (2, 4, 2), (2, 4, 4),
            (10, 5, 1), (10, 5, 5),
            (11, 6, 0), (11, 6, 6)
        ]
        
        blue_pieces = [
            (12, 8, 3), (9, 8, 6), (8, 8, 0),
            (7, 7, 1), (7, 7, 5),
            (6, 6, 2), (6, 6, 4),
            (5, 5, 3),
            (4, 6, 0), (4, 6, 6),
            (3, 7, 1), (3, 7, 5),
            (2, 8, 2), (2, 8, 4),
            (10, 3, 1), (10, 3, 5),
            (11, 2, 0), (11, 2, 6)
        ]

        for rank, row, col in red_pieces:
            self.board[row][col] = Piece(rank, 'red', row, col)
            
        for rank, row, col in blue_pieces:
            self.board[row][col] = Piece(rank, 'blue', row, col)

    def draw_board(self):
        self.win.fill(COLORS['background'])
        
        # 绘制棋盘
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                pygame.draw.rect(self.win, COLORS['board'], 
                               (x, y, CELL_SIZE, CELL_SIZE), 2)
        
        # 绘制棋子
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw(self.win)
        
        pygame.display.update()

    def handle_click(self, row, col):
        # Add bounds checking
        if row < 0 or row >= BOARD_ROWS or col < 0 or col >= BOARD_COLS:
            return

        piece = self.board[row][col]
        if piece:
            if piece.team == self.turn:
                self.selected_piece = piece
                piece.selected = True
        elif self.selected_piece:
            if self.is_valid_move(self.selected_piece, row, col):
                self.move_piece(self.selected_piece, row, col)
                self.turn = 'blue' if self.turn == 'red' else 'red'
                self.selected_piece = None

    def is_valid_move(self, piece, new_row, new_col):
        # 简单移动验证（需扩展完整规则）
        return abs(new_row - piece.row) <= 1 and abs(new_col - piece.col) <= 1

    def move_piece(self, piece, new_row, new_col):
        self.board[piece.row][piece.col] = None
        piece.move(new_row, new_col)
        self.board[new_row][new_col] = piece

    def check_win_condition(self):
        # 胜利条件判断（需扩展完整逻辑）
        return False

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    self.handle_click(row, col)

            self.draw_board()
            if self.check_win_condition():
                running = False

            pygame.display.update()

        pygame.quit()
