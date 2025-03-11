import pygame
import sys
from .pieces import Piece
from .constants import *

class JungleGame:
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.win = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.selected_piece = None
        self.turn = 'red'
        self.game_over = False
        self.winner = None
        self.history = []
        self.status_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 32)
        self.hint_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 20)
        self.game_started = False  # 是否已经选择游戏模式
        self.vs_ai = False  # 是否是人机对战模式
        self.ai_difficulty = 'normal'  # AI难度
        self.menu_index = 0  # 当前选中的菜单项
        self.difficulties = [('简单', 'easy'), ('中等', 'normal'), ('困难', 'hard')]
        self.diff_index = 1  # 当前选中的难度（默认中等）
        self.initialize_board()

    def initialize_board(self):
        """初始化棋盘和棋子"""
        # 清空棋盘
        self.board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        
        # 初始化红方棋子
        red_pieces = [
            (12, 0, 3),  # 军旗
            (11, 6, 0),  # 司令
            (10, 2, 2), (10, 2, 4),  # 地雷
            (9, 6, 6),   # 军长
            (8, 0, 0),   # 师长
            (7, 1, 1), (7, 1, 5),  # 旅长
            (6, 2, 0), (6, 2, 6),  # 团长
            (5, 3, 1), (5, 3, 5),  # 营长
            (4, 4, 2), (4, 4, 4),  # 连长
            (3, 5, 1), (3, 5, 5),  # 排长
            (2, 0, 6), (2, 3, 3)   # 工兵
        ]
        
        # 初始化蓝方棋子
        blue_pieces = [
            (12, 8, 3),  # 军旗
            (11, 2, 6),  # 司令
            (10, 6, 2), (10, 6, 4),  # 地雷
            (9, 2, 0),   # 军长
            (8, 8, 6),   # 师长
            (7, 7, 1), (7, 7, 5),  # 旅长
            (6, 6, 0), (6, 6, 6),  # 团长
            (5, 5, 1), (5, 5, 5),  # 营长
            (4, 4, 2), (4, 4, 4),  # 连长
            (3, 3, 1), (3, 3, 5),  # 排长
            (2, 8, 0), (2, 5, 3)   # 工兵
        ]

        # 放置红方棋子
        for rank, row, col in red_pieces:
            self.board[row][col] = Piece(rank, 'red', row, col)
            
        # 放置蓝方棋子
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

    def draw_mode_selection(self):
        """绘制游戏模式选择界面"""
        self.win.fill(COLORS['background'])
        
        # 绘制标题
        title_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
        title = title_font.render("军旗", True, COLORS['text'])
        title_rect = title.get_rect(center=(self.screen_width//2, 100))
        self.win.blit(title, title_rect)
        
        # 绘制模式选择按钮
        button_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
        
        # 双人对战按钮
        pvp_text = button_font.render("双人对战", True, COLORS['text'])
        pvp_rect = pvp_text.get_rect(center=(self.screen_width//2, 200))
        button_color = COLORS['selected'] if self.menu_index == 0 and not self.vs_ai else COLORS['button']
        pygame.draw.rect(self.win, button_color, pvp_rect.inflate(40, 20))
        self.win.blit(pvp_text, pvp_rect)
        
        # 人机对战按钮
        pve_text = button_font.render("人机对战", True, COLORS['text'])
        pve_rect = pve_text.get_rect(center=(self.screen_width//2, 300))
        button_color = COLORS['selected'] if self.menu_index == 1 or self.vs_ai else COLORS['button']
        pygame.draw.rect(self.win, button_color, pve_rect.inflate(40, 20))
        self.win.blit(pve_text, pve_rect)
        
        # 如果选择了人机对战，显示难度选择
        if self.vs_ai:
            for i, (text, _) in enumerate(self.difficulties):
                diff_text = button_font.render(text, True, COLORS['text'])
                diff_rect = diff_text.get_rect(center=(self.screen_width//2, 400 + i*60))
                button_color = COLORS['selected'] if i == self.diff_index else COLORS['button']
                pygame.draw.rect(self.win, button_color, diff_rect.inflate(40, 20))
                self.win.blit(diff_text, diff_rect)
        
        # 绘制操作提示
        hint_text = "↑↓: 选择  Enter: 确认  ESC: 返回"
        hint = self.hint_font.render(hint_text, True, COLORS['text'])
        hint_rect = hint.get_rect(center=(self.screen_width//2, SCREEN_HEIGHT - 30))
        self.win.blit(hint, hint_rect)
        
        pygame.display.update()

    def handle_mode_selection(self, event):
        """处理游戏模式选择的事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # 检查双人对战按钮
            pvp_rect = pygame.Rect(self.screen_width//2 - 70, 185, 140, 40)
            if pvp_rect.collidepoint(mouse_pos):
                self.vs_ai = False
                self.game_started = True
                return
            
            # 检查人机对战按钮
            pve_rect = pygame.Rect(self.screen_width//2 - 70, 285, 140, 40)
            if pve_rect.collidepoint(mouse_pos):
                self.vs_ai = True
                return
            
            # 如果显示难度选择，检查难度按钮
            if self.vs_ai:
                for i, (_, diff) in enumerate(self.difficulties):
                    diff_rect = pygame.Rect(self.screen_width//2 - 70, 385 + i*60, 140, 40)
                    if diff_rect.collidepoint(mouse_pos):
                        self.ai_difficulty = diff
                        self.game_started = True
                        return
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.vs_ai and not self.game_started:
                    self.vs_ai = False  # 返回到主菜单
                else:
                    pygame.display.set_mode((600, 500))
                    pygame.display.set_caption("游戏合集")
                    return True
            
            elif event.key == pygame.K_UP:
                if self.vs_ai:
                    self.diff_index = (self.diff_index - 1) % len(self.difficulties)
                else:
                    self.menu_index = (self.menu_index - 1) % 2
            
            elif event.key == pygame.K_DOWN:
                if self.vs_ai:
                    self.diff_index = (self.diff_index + 1) % len(self.difficulties)
                else:
                    self.menu_index = (self.menu_index + 1) % 2
            
            elif event.key == pygame.K_RETURN:
                if not self.vs_ai:
                    if self.menu_index == 0:
                        self.game_started = True
                    else:
                        self.vs_ai = True
                else:
                    self.ai_difficulty = self.difficulties[self.diff_index][1]
                    self.game_started = True

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
                
                # 处理游戏模式选择
                if not self.game_started:
                    self.draw_mode_selection()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif self.handle_mode_selection(event):
                            running = False
                    continue
                
                # 主游戏循环
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
                
                # AI移动
                if self.vs_ai and not self.game_over and self.turn == 'blue':
                    ai_move = self.get_ai_move()
                    if ai_move:
                        piece, to_row, to_col = ai_move
                        self.move_piece(piece, to_row, to_col)
                        self.turn = 'red'

                if self.win:  # 确保窗口还存在
                    self.draw_board()
                    pygame.display.update()
                
        finally:
            self.cleanup()  # 确保资源被清理

    def get_ai_move(self):
        # 获取所有合法移动
        valid_moves = []
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                piece = self.board[row][col]
                if piece and piece.team == self.turn:
                    moves = self.get_valid_moves(piece)
                    for move in moves:
                        valid_moves.append((piece, move[0], move[1]))
        
        if not valid_moves:
            return None
        
        # 改进的评估函数
        def evaluate_move(piece, to_row, to_col):
            score = 0
            target = self.board[to_row][to_col]
            
            # 基本价值
            if target:
                score += target.rank * 2  # 提高吃子权重
            else:
                score += 1
                
            # 位置价值
            if piece.rank == 12:  # 军旗
                # 鼓励军旗向对方大本营移动
                hq_row, hq_col = HEADQUARTER_POSITIONS['red' if piece.team == 'blue' else 'blue']
                distance = abs(to_row - hq_row) + abs(to_col - hq_col)
                score += 100 / (distance + 1)
                
            # 控制中心区域
            center_row, center_col = BOARD_ROWS // 2, BOARD_COLS // 2
            distance_to_center = abs(to_row - center_row) + abs(to_col - center_col)
            score += 50 / (distance_to_center + 1)
            
            # 根据难度调整评估
            if self.ai_difficulty == 'easy':
                score *= 0.5  # 降低评估准确度
            elif self.ai_difficulty == 'hard':
                score *= 1.5  # 提高评估准确度
            
            return score
        
        # 选择最佳移动
        best_score = -float('inf')
        best_move = None
        
        for piece, to_row, to_col in valid_moves:
            score = evaluate_move(piece, to_row, to_col)
            if score > best_score:
                best_score = score
                best_move = (piece, to_row, to_col)
        
        return best_move
