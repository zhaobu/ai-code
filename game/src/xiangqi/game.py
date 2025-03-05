import pygame
import random
from typing import List, Tuple, Optional, Dict
from src.common.colors import *

class XiangqiGame:
    def __init__(self, block_size: int = 60):
        # 中国象棋棋盘是9x10的
        self.board_width = 9
        self.board_height = 10
        self.block_size = block_size
        self.margin = 50  # 棋盘边距
        self.screen_width = self.board_width * block_size + 2 * self.margin
        self.screen_height = self.board_height * block_size + 2 * self.margin
        self.game_over = False
        self.is_red_turn = True  # True表示红方回合
        self.winner = None
        self.selected_piece = None
        
        # 初始化棋盘和棋子
        self.board = [[None for _ in range(self.board_width)] for _ in range(self.board_height)]
        self._init_pieces()
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("中国象棋")
        self.clock = pygame.time.Clock()
        
        # 加载棋子图片
        self.piece_images = {}
        self._load_piece_images()
    
    def _load_piece_images(self):
        """加载棋子图片，如果没有图片，使用文字代替"""
        # 这里使用文字代替图片，实际应用中可以加载真实图片
        self.piece_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
        
        # 红方棋子文字
        self.piece_texts = {
            'r_general': '帅',
            'r_advisor': '仕',
            'r_elephant': '相',
            'r_horse': '马',
            'r_chariot': '车',
            'r_cannon': '炮',
            'r_soldier': '兵',
            # 黑方棋子文字
            'b_general': '将',
            'b_advisor': '士',
            'b_elephant': '象',
            'b_horse': '马',
            'b_chariot': '车',
            'b_cannon': '炮',
            'b_soldier': '卒'
        }
    
    def _init_pieces(self):
        """初始化棋子位置"""
        # 初始化红方棋子（下方）
        self.board[9][4] = {'type': 'general', 'color': 'red'}
        self.board[9][3] = {'type': 'advisor', 'color': 'red'}
        self.board[9][5] = {'type': 'advisor', 'color': 'red'}
        self.board[9][2] = {'type': 'elephant', 'color': 'red'}
        self.board[9][6] = {'type': 'elephant', 'color': 'red'}
        self.board[9][1] = {'type': 'horse', 'color': 'red'}
        self.board[9][7] = {'type': 'horse', 'color': 'red'}
        self.board[9][0] = {'type': 'chariot', 'color': 'red'}
        self.board[9][8] = {'type': 'chariot', 'color': 'red'}
        self.board[7][1] = {'type': 'cannon', 'color': 'red'}
        self.board[7][7] = {'type': 'cannon', 'color': 'red'}
        self.board[6][0] = {'type': 'soldier', 'color': 'red'}
        self.board[6][2] = {'type': 'soldier', 'color': 'red'}
        self.board[6][4] = {'type': 'soldier', 'color': 'red'}
        self.board[6][6] = {'type': 'soldier', 'color': 'red'}
        self.board[6][8] = {'type': 'soldier', 'color': 'red'}
        
        # 初始化黑方棋子（上方）
        self.board[0][4] = {'type': 'general', 'color': 'black'}
        self.board[0][3] = {'type': 'advisor', 'color': 'black'}
        self.board[0][5] = {'type': 'advisor', 'color': 'black'}
        self.board[0][2] = {'type': 'elephant', 'color': 'black'}
        self.board[0][6] = {'type': 'elephant', 'color': 'black'}
        self.board[0][1] = {'type': 'horse', 'color': 'black'}
        self.board[0][7] = {'type': 'horse', 'color': 'black'}
        self.board[0][0] = {'type': 'chariot', 'color': 'black'}
        self.board[0][8] = {'type': 'chariot', 'color': 'black'}
        self.board[2][1] = {'type': 'cannon', 'color': 'black'}
        self.board[2][7] = {'type': 'cannon', 'color': 'black'}
        self.board[3][0] = {'type': 'soldier', 'color': 'black'}
        self.board[3][2] = {'type': 'soldier', 'color': 'black'}
        self.board[3][4] = {'type': 'soldier', 'color': 'black'}
        self.board[3][6] = {'type': 'soldier', 'color': 'black'}
        self.board[3][8] = {'type': 'soldier', 'color': 'black'}
    
    def _get_board_pos(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """将鼠标坐标转换为棋盘坐标"""
        x, y = mouse_pos
        board_x = round((x - self.margin) / self.block_size)
        board_y = round((y - self.margin) / self.block_size)
        if 0 <= board_x < self.board_width and 0 <= board_y < self.board_height:
            return board_x, board_y
        return None
    
    def _is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """检查移动是否合法"""
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        # 确保起始位置有棋子
        if self.board[from_y][from_x] is None:
            return False
        
        # 确保目标位置没有同色棋子
        if self.board[to_y][to_x] is not None and self.board[to_y][to_x]['color'] == self.board[from_y][from_x]['color']:
            return False
        
        piece = self.board[from_y][from_x]
        piece_type = piece['type']
        piece_color = piece['color']
        
        # 根据不同棋子类型检查移动规则
        if piece_type == 'general':
            # 将/帅只能在九宫格内移动，每次只能移动一格
            if piece_color == 'red':
                # 红方九宫格
                if not (7 <= to_y <= 9 and 3 <= to_x <= 5):
                    return False
            else:
                # 黑方九宫格
                if not (0 <= to_y <= 2 and 3 <= to_x <= 5):
                    return False
            
            # 只能横向或纵向移动一格
            if abs(to_x - from_x) + abs(to_y - from_y) != 1:
                return False
        
        elif piece_type == 'advisor':
            # 仕/士只能在九宫格内斜线移动
            if piece_color == 'red':
                if not (7 <= to_y <= 9 and 3 <= to_x <= 5):
                    return False
            else:
                if not (0 <= to_y <= 2 and 3 <= to_x <= 5):
                    return False
            
            # 只能斜线移动一格
            if abs(to_x - from_x) != 1 or abs(to_y - from_y) != 1:
                return False
        
        elif piece_type == 'elephant':
            # 相/象不能过河
            if piece_color == 'red' and to_y < 5:
                return False
            if piece_color == 'black' and to_y > 4:
                return False
            
            # 相/象走田字格
            if abs(to_x - from_x) != 2 or abs(to_y - from_y) != 2:
                return False
            
            # 检查象眼是否被堵
            elephant_eye_x = (from_x + to_x) // 2
            elephant_eye_y = (from_y + to_y) // 2
            if self.board[elephant_eye_y][elephant_eye_x] is not None:
                return False
        
        elif piece_type == 'horse':
            # 马走日字
            if not ((abs(to_x - from_x) == 1 and abs(to_y - from_y) == 2) or 
                    (abs(to_x - from_x) == 2 and abs(to_y - from_y) == 1)):
                return False
            
            # 检查马腿是否被堵
            if abs(to_x - from_x) == 1:
                # 竖向移动，检查横向马腿
                horse_leg_y = from_y + (1 if to_y > from_y else -1)
                if self.board[horse_leg_y][from_x] is not None:
                    return False
            else:
                # 横向移动，检查纵向马腿
                horse_leg_x = from_x + (1 if to_x > from_x else -1)
                if self.board[from_y][horse_leg_x] is not None:
                    return False
        
        elif piece_type == 'chariot':
            # 车走直线
            if from_x != to_x and from_y != to_y:
                return False
            
            # 检查路径上是否有其他棋子
            if from_x == to_x:
                # 纵向移动
                start, end = min(from_y, to_y), max(from_y, to_y)
                for y in range(start + 1, end):
                    if self.board[y][from_x] is not None:
                        return False
            else:
                # 横向移动
                start, end = min(from_x, to_x), max(from_x, to_x)
                for x in range(start + 1, end):
                    if self.board[from_y][x] is not None:
                        return False
        
        elif piece_type == 'cannon':
            # 炮走直线
            if from_x != to_x and from_y != to_y:
                return False
            
            # 计算路径上的棋子数量
            piece_count = 0
            if from_x == to_x:
                # 纵向移动
                start, end = min(from_y, to_y), max(from_y, to_y)
                for y in range(start + 1, end):
                    if self.board[y][from_x] is not None:
                        piece_count += 1
            else:
                # 横向移动
                start, end = min(from_x, to_x), max(from_x, to_x)
                for x in range(start + 1, end):
                    if self.board[from_y][x] is not None:
                        piece_count += 1
            
            # 炮的移动规则：移动时不能有棋子，吃子时必须有且仅有一个棋子作为炮架
            if self.board[to_y][to_x] is None:
                # 移动，路径上不能有棋子
                return piece_count == 0
            else:
                # 吃子，路径上必须有且仅有一个棋子
                return piece_count == 1
        
        elif piece_type == 'soldier':
            # 兵/卒只能向前或横向移动一格，且过河后才能横向移动
            if piece_color == 'red':
                # 红方兵向上移动
                if to_y > from_y:
                    return False
                if from_y > 4:  # 未过河
                    if to_x != from_x or to_y != from_y - 1:
                        return False
                else:  # 已过河
                    if not ((to_x == from_x and to_y == from_y - 1) or 
                            (to_y == from_y and abs(to_x - from_x) == 1)):
                        return False
            else:
                # 黑方卒向下移动
                if to_y < from_y:
                    return False
                if from_y < 5:  # 未过河
                    if to_x != from_x or to_y != from_y + 1:
                        return False
                else:  # 已过河
                    if not ((to_x == from_x and to_y == from_y + 1) or 
                            (to_y == from_y and abs(to_x - from_x) == 1)):
                        return False
        
        return True
    
    def _check_win(self) -> bool:
        """检查是否将军或胜利"""
        # 检查将帅是否被吃掉
        red_general_exists = False
        black_general_exists = False
        
        for y in range(self.board_height):
            for x in range(self.board_width):
                piece = self.board[y][x]
                if piece is not None and piece['type'] == 'general':
                    if piece['color'] == 'red':
                        red_general_exists = True
                    else:
                        black_general_exists = True
        
        if not red_general_exists:
            self.winner = 'black'
            return True
        if not black_general_exists:
            self.winner = 'red'
            return True
        
        return False
    
    def _draw_board(self):
        """绘制棋盘"""
        # 绘制棋盘背景
        self.screen.fill((240, 240, 240))
        board_rect = pygame.Rect(self.margin - 5, self.margin - 5,
                               self.board_width * self.block_size + 10,
                               self.board_height * self.block_size + 10)
        pygame.draw.rect(self.screen, (210, 180, 140), board_rect)  # 实木色调
        
        # 绘制棋盘网格
        for x in range(self.board_width):
            pygame.draw.line(self.screen, BLACK,
                           (self.margin + x * self.block_size, self.margin),
                           (self.margin + x * self.block_size, self.margin + (self.board_height - 1) * self.block_size))
        
        for y in range(self.board_height):
            pygame.draw.line(self.screen, BLACK,
                           (self.margin, self.margin + y * self.block_size),
                           (self.margin + (self.board_width - 1) * self.block_size, self.margin + y * self.block_size))
        
        # 绘制九宫格
        # 上方九宫格
        pygame.draw.line(self.screen, BLACK,
                       (self.margin + 3 * self.block_size, self.margin),
                       (self.margin + 5 * self.block_size, self.margin + 2 * self.block_size))
        pygame.draw.line(self.screen, BLACK,
                       (self.margin + 5 * self.block_size, self.margin),
                       (self.margin + 3 * self.block_size, self.margin + 2 * self.block_size))
        
        # 下方九宫格
        pygame.draw.line(self.screen, BLACK,
                       (self.margin + 3 * self.block_size, self.margin + 7 * self.block_size),
                       (self.margin + 5 * self.block_size, self.margin + 9 * self.block_size))
        pygame.draw.line(self.screen, BLACK,
                       (self.margin + 5 * self.block_size, self.margin + 7 * self.block_size),
                       (self.margin + 3 * self.block_size, self.margin + 9 * self.block_size))
        
        # 绘制河界
        font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
        text = font.render("楚河          汉界", True, BLACK)
        text_rect = text.get_rect(center=(self.screen_width // 2, self.margin + 4.5 * self.block_size))
        self.screen.blit(text, text_rect)
    
    def _draw_pieces(self):
        """绘制棋子"""
        for y in range(self.board_height):
            for x in range(self.board_width):
                piece = self.board[y][x]
                if piece is not None:
                    # 计算棋子位置
                    pos = (self.margin + x * self.block_size, self.margin + y * self.block_size)
                    
                    # 绘制棋子背景
                    radius = self.block_size // 2 - 2
                    color = RED if piece['color'] == 'red' else BLACK
                    bg_color = (255, 220, 180) if piece['color'] == 'red' else (200, 200, 200)
                    
                    # 绘制棋子阴影
                    shadow_pos = (pos[0] + 2, pos[1] + 2)
                    pygame.draw.circle(self.screen, (100, 100, 100), shadow_pos, radius)
                    
                    # 绘制棋子
                    pygame.draw.circle(self.screen, bg_color, pos, radius)
                    pygame.draw.circle(self.screen, color, pos, radius, 2)
                    
                    # 绘制棋子文字
                    piece_key = ('r_' if piece['color'] == 'red' else 'b_') + piece['type']
                    text = self.piece_font.render(self.piece_texts[piece_key], True, color)
                    text_rect = text.get_rect(center=pos)
                    self.screen.blit(text, text_rect)
                    
                    # 高亮选中的棋子
                    if self.selected_piece == (x, y):
                        pygame.draw.circle(self.screen, YELLOW, pos, radius, 3)
    
    def run(self):
        while True:
            self._draw_board()
            self._draw_pieces()
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    pos = self._get_board_pos(event.pos)
                    if pos:
                        x, y = pos
                        # 如果已经选中了一个棋子
                        if self.selected_piece is not None:
                            from_x, from_y = self.selected_piece
                            # 如果点击的是同一个位置，取消选择
                            if (x, y) == self.selected_piece:
                                self.selected_piece = None
                            # 如果点击的是另一个己方棋子，更新选择
                            elif self.board[y][x] is not None and self.board[y][x]['color'] == ('red' if self.is_red_turn else 'black'):
                                self.selected_piece = (x, y)
                            # 如果是有效移动
                            elif self._is_valid_move(self.selected_piece, (x, y)):
                                # 移动棋子
                                self.board[y][x] = self.board[from_y][from_x]
                                self.board[from_y][from_x] = None
                                self.selected_piece = None
                                
                                # 检查胜利条件
                                if self._check_win():
                                    self.game_over = True
                                
                                # 切换回合
                                self.is_red_turn = not self.is_red_turn
                        # 如果没有选中棋子，且点击的是己方棋子
                        elif self.board[y][x] is not None and self.board[y][x]['color'] == ('red' if self.is_red_turn else 'black'):
                            self.selected_piece = (x, y)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.block_size)
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
            
            # 游戏结束显示
            if self.game_over:
                # 创建半透明背景
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(128)
                self.screen.blit(overlay, (0, 0))
                
                font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 56)
                if self.winner == 'red':
                    text = font.render("红方胜利！", True, (255, 215, 0))  # 金色
                else:
                    text = font.render("黑方胜利！", True, (255, 215, 0))  # 金色
                
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