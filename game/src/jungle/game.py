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
        self.winner = None
        self.history = []
        self.status_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 32)
        self.hint_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 20)
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
        
        # 绘制游戏状态
        status_text = f"当前回合: {'红方' if self.turn == 'red' else '蓝方'}"
        if self.game_over:
            status_text = f"游戏结束 - {'红方' if self.winner == 'red' else '蓝方'}胜利!"
        text = self.status_font.render(status_text, True, COLORS['text'])
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 30))
        self.win.blit(text, text_rect)
        
        # 绘制操作提示
        hint_text = "操作提示: Z-悔棋 | R-重新开始 | ESC-退出游戏"
        hint = self.hint_font.render(hint_text, True, COLORS['text'])
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 20))
        self.win.blit(hint, hint_rect)
        
        # 绘制基础棋盘
        board_offset_x = (SCREEN_WIDTH - BOARD_COLS * CELL_SIZE) // 2
        board_offset_y = (SCREEN_HEIGHT - BOARD_ROWS * CELL_SIZE) // 2
        
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                x = board_offset_x + col * CELL_SIZE
                y = board_offset_y + row * CELL_SIZE
                pygame.draw.rect(self.win, COLORS['board'], 
                               (x, y, CELL_SIZE, CELL_SIZE), 2)
        
        # 绘制铁路线
        for pos in RAILWAY_POSITIONS['horizontal']:
            row, col = pos
            x = board_offset_x + col * CELL_SIZE
            y = board_offset_y + row * CELL_SIZE
            pygame.draw.line(self.win, COLORS['railway'],
                           (x, y + CELL_SIZE//2),
                           (x + CELL_SIZE, y + CELL_SIZE//2), 3)
            
        for pos in RAILWAY_POSITIONS['vertical']:
            row, col = pos
            x = board_offset_x + col * CELL_SIZE
            y = board_offset_y + row * CELL_SIZE
            pygame.draw.line(self.win, COLORS['railway'],
                           (x + CELL_SIZE//2, y),
                           (x + CELL_SIZE//2, y + CELL_SIZE), 3)
        
        # 绘制行营
        for row, col in CAMP_POSITIONS:
            x = board_offset_x + col * CELL_SIZE
            y = board_offset_y + row * CELL_SIZE
            points = [
                (x + CELL_SIZE//2, y),
                (x + CELL_SIZE, y + CELL_SIZE//2),
                (x + CELL_SIZE//2, y + CELL_SIZE),
                (x, y + CELL_SIZE//2)
            ]
            pygame.draw.polygon(self.win, COLORS['camp'], points)
            
        # 绘制大本营
        for team, (row, col) in HEADQUARTER_POSITIONS.items():
            x = board_offset_x + col * CELL_SIZE
            y = board_offset_y + row * CELL_SIZE
            pygame.draw.rect(self.win, COLORS['headquarter'],
                           (x, y, CELL_SIZE, CELL_SIZE))
            
        # 绘制棋子
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                piece = self.board[row][col]
                if piece:
                    x = board_offset_x + col * CELL_SIZE
                    y = board_offset_y + row * CELL_SIZE
                    piece.draw(self.win, x, y)
                    
        # 绘制可移动位置提示
        if self.selected_piece:
            valid_moves = self.get_valid_moves(self.selected_piece)
            for row, col in valid_moves:
                x = board_offset_x + col * CELL_SIZE + CELL_SIZE//2
                y = board_offset_y + row * CELL_SIZE + CELL_SIZE//2
                pygame.draw.circle(self.win, COLORS['highlight'],
                                 (x, y), 10)
        
        pygame.display.update()

    def handle_click(self, px, py):
        # 转换屏幕坐标到棋盘坐标
        board_offset_x = (SCREEN_WIDTH - BOARD_COLS * CELL_SIZE) // 2
        board_offset_y = (SCREEN_HEIGHT - BOARD_ROWS * CELL_SIZE) // 2
        
        col = (px - board_offset_x) // CELL_SIZE
        row = (py - board_offset_y) // CELL_SIZE
        
        # Add bounds checking
        if row < 0 or row >= BOARD_ROWS or col < 0 or col >= BOARD_COLS:
            return

        # 清除之前选中的棋子
        if self.selected_piece:
            self.selected_piece.selected = False

        piece = self.board[row][col]
        if piece:
            if piece.team == self.turn:
                self.selected_piece = piece
                piece.selected = True
            elif self.selected_piece and self.is_valid_move(self.selected_piece, row, col):
                self.move_piece(self.selected_piece, row, col)
                self.selected_piece = None
                self.turn = 'blue' if self.turn == 'red' else 'red'
        elif self.selected_piece:
            if self.is_valid_move(self.selected_piece, row, col):
                self.move_piece(self.selected_piece, row, col)
                self.turn = 'blue' if self.turn == 'red' else 'red'
                self.selected_piece = None

    def get_valid_moves(self, piece):
        valid_moves = []
        if piece.rank == 10:  # 地雷不能移动
            return valid_moves
            
        # 检查常规移动（上下左右）
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        for dr, dc in directions:
            new_row = piece.row + dr
            new_col = piece.col + dc
            if self.is_valid_position(new_row, new_col):
                if self.is_valid_destination(piece, new_row, new_col):
                    valid_moves.append((new_row, new_col))
        
        # 检查铁路移动
        if self.is_on_railway(piece.row, piece.col):
            railway_moves = self.get_railway_moves(piece)
            valid_moves.extend(railway_moves)
            
        return valid_moves

    def is_valid_move(self, piece, new_row, new_col):
        if not self.is_valid_position(new_row, new_col):
            return False
            
        if piece.rank == 10:  # 地雷不能移动
            return False
            
        # 如果是在铁路上的移动
        if self.is_on_railway(piece.row, piece.col) and self.is_on_railway(new_row, new_col):
            railway_moves = self.get_railway_moves(piece)
            return (new_row, new_col) in railway_moves
            
        # 常规移动（上下左右一格）
        return (abs(new_row - piece.row) + abs(new_col - piece.col) == 1 and
                self.is_valid_destination(piece, new_row, new_col))
                
    def is_valid_position(self, row, col):
        """检查位置是否在棋盘范围内"""
        return 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS
        
    def is_on_railway(self, row, col):
        """检查位置是否在铁路上"""
        pos = (row, col)
        return pos in RAILWAY_POSITIONS['horizontal'] or pos in RAILWAY_POSITIONS['vertical']
        
    def get_railway_moves(self, piece):
        """获取铁路上可能的移动位置"""
        moves = []
        if not self.is_on_railway(piece.row, piece.col):
            return moves
            
        # 检查水平铁路移动
        if (piece.row, piece.col) in RAILWAY_POSITIONS['horizontal']:
            row = piece.row
            # 向左移动
            for col in range(piece.col - 1, -1, -1):
                if not self.is_on_railway(row, col):
                    break
                if self.is_valid_destination(piece, row, col):
                    moves.append((row, col))
                if self.board[row][col]:
                    break
            # 向右移动
            for col in range(piece.col + 1, BOARD_COLS):
                if not self.is_on_railway(row, col):
                    break
                if self.is_valid_destination(piece, row, col):
                    moves.append((row, col))
                if self.board[row][col]:
                    break
                    
        # 检查垂直铁路移动
        if (piece.row, piece.col) in RAILWAY_POSITIONS['vertical']:
            col = piece.col
            # 向上移动
            for row in range(piece.row - 1, -1, -1):
                if not self.is_on_railway(row, col):
                    break
                if self.is_valid_destination(piece, row, col):
                    moves.append((row, col))
                if self.board[row][col]:
                    break
            # 向下移动
            for row in range(piece.row + 1, BOARD_ROWS):
                if not self.is_on_railway(row, col):
                    break
                if self.is_valid_destination(piece, row, col):
                    moves.append((row, col))
                if self.board[row][col]:
                    break
                    
        return moves
        
    def is_valid_destination(self, piece, row, col):
        """检查目标位置是否可以移动到或吃子"""
        # 检查是否是行营
        if (row, col) in CAMP_POSITIONS:
            return True
            
        # 检查是否是对方大本营
        red_hq = HEADQUARTER_POSITIONS['red']
        blue_hq = HEADQUARTER_POSITIONS['blue']
        if (piece.team == 'red' and (row, col) == blue_hq) or \
           (piece.team == 'blue' and (row, col) == red_hq):
            if piece.rank == 12:  # 只有军旗可以进入对方大本营
                return True
            return False
            
        # 检查是否是己方大本营
        if (piece.team == 'red' and (row, col) == red_hq) or \
           (piece.team == 'blue' and (row, col) == blue_hq):
            return False
            
        # 检查是否可以吃子
        target = self.board[row][col]
        if not target:
            return True
        if target.team == piece.team:
            return False
        return piece.can_capture(target)

    def move_piece(self, piece, new_row, new_col):
        # 记录移动历史
        captured_piece = self.board[new_row][new_col]
        move_record = {
            'piece': piece,
            'from_pos': (piece.row, piece.col),
            'to_pos': (new_row, new_col),
            'captured': captured_piece
        }
        self.history.append(move_record)
        
        # 执行移动
        self.board[piece.row][piece.col] = None
        piece.move(new_row, new_col)
        self.board[new_row][new_col] = piece
        
        # 检查胜利条件
        self.check_win_condition()

    def check_win_condition(self):
        red_flag = blue_flag = False
        red_alive = blue_alive = False
        
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                piece = self.board[row][col]
                if piece:
                    if piece.rank == 12:  # 军旗
                        if piece.team == 'red':
                            red_flag = True
                        else:
                            blue_flag = True
                    # 检查是否还有可移动的棋子
                    elif piece.rank not in [10]:  # 不是地雷
                        if piece.team == 'red':
                            red_alive = True
                        else:
                            blue_alive = True
        
        # 检查军旗是否到达对方大本营
        red_hq = HEADQUARTER_POSITIONS['red']
        blue_hq = HEADQUARTER_POSITIONS['blue']
        
        if self.board[blue_hq[0]][blue_hq[1]]:
            piece = self.board[blue_hq[0]][blue_hq[1]]
            if piece.team == 'red' and piece.rank == 12:
                self.game_over = True
                self.winner = 'red'
                return True
                
        if self.board[red_hq[0]][red_hq[1]]:
            piece = self.board[red_hq[0]][red_hq[1]]
            if piece.team == 'blue' and piece.rank == 12:
                self.game_over = True
                self.winner = 'blue'
                return True
                
        # 检查军旗被吃或无可移动棋子
        if not red_flag or not red_alive:
            self.game_over = True
            self.winner = 'blue'
            return True
        if not blue_flag or not blue_alive:
            self.game_over = True
            self.winner = 'red'
            return True
            
        return False

    def undo_move(self):
        """撤销上一步移动"""
        if not self.history:
            return
            
        move = self.history.pop()
        piece = move['piece']
        old_row, old_col = move['from_pos']
        cur_row, cur_col = move['to_pos']
        captured = move['captured']
        
        # 恢复棋子位置
        self.board[cur_row][cur_col] = captured
        self.board[old_row][old_col] = piece
        piece.move(old_row, old_col)
        
        # 切换回合
        self.turn = 'blue' if self.turn == 'red' else 'red'
        self.game_over = False
        self.winner = None

    def cleanup(self):
        """清理游戏资源"""
        # 释放窗口但不退出pygame
        if self.win:
            pygame.display.quit()
            self.win = None

    def run(self):
        clock = pygame.time.Clock()
        running = True
        try:
            pygame.display.init()  # 重新初始化显示
            self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            
            while running:
                clock.tick(30)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                        x, y = pygame.mouse.get_pos()
                        self.handle_click(x, y)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z:  # 按Z撤销移动
                            self.undo_move()
                        elif event.key == pygame.K_r:  # 按R重新开始
                            self.__init__()
                        elif event.key == pygame.K_ESCAPE:  # 按ESC退出
                            running = False

                if self.win:  # 确保窗口还存在
                    self.draw_board()
                    pygame.display.update()
                
        finally:
            self.cleanup()  # 确保资源被清理
