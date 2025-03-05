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
        self.history_area_width = 200  # 走子记录区域宽度
        self.screen_width = self.board_width * block_size + 2 * self.margin + self.history_area_width
        self.screen_height = self.board_height * block_size + 2 * self.margin + 100  # 增加高度以显示模式选择按钮
        self.game_over = False
        self.is_red_turn = True  # True表示红方回合
        self.winner = None
        self.selected_piece = None
        self.game_started = False  # 是否已经选择游戏模式
        self.vs_ai = False  # 是否是人机对战模式
        self.ai_difficulty = 'normal'  # AI难度
        self.ai = None  # AI实例
        self.moves_history = []  # 记录走子历史
        self.scroll_offset = 0  # 添加滚动偏移量
        self.history_surface = None  # 缓存历史记录surface
        self.history_needs_update = True  # 标记是否需要更新历史记录
        
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
        
        # 绘制走子记录区域
        history_area_x = self.margin + self.board_width * self.block_size + self.margin
        history_area_y = self.margin
        history_area = pygame.Rect(history_area_x, history_area_y,
                                 self.history_area_width, self.screen_height - 2 * self.margin)
        pygame.draw.rect(self.screen, (245, 245, 245), history_area)
        pygame.draw.rect(self.screen, (180, 180, 180), history_area, 2)
        
        # 绘制走子记录标题
        font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)
        title = font.render("走子记录", True, BLACK)
        title_rect = title.get_rect(center=(history_area_x + self.history_area_width//2, history_area_y + 20))
        self.screen.blit(title, title_rect)
        
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
    
    def _get_move_text(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], piece: Dict) -> str:
        """生成走子记录的文本"""
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        piece_type = piece['type']
        is_red = piece['color'] == 'red'
        
        # 中文数字映射
        numbers = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        
        # 棋子类型映射
        piece_names = {
            'general': '帅' if is_red else '将',
            'advisor': '仕' if is_red else '士',
            'elephant': '相' if is_red else '象',
            'horse': '马',
            'chariot': '车',
            'cannon': '炮',
            'soldier': '兵' if is_red else '卒'
        }
        
        # 获取棋子名称
        piece_name = piece_names[piece_type]
        
        # 计算列号（从右到左）
        from_col = 9 - from_x if is_red else from_x + 1
        to_col = 9 - to_x if is_red else to_x + 1
        
        # 判断移动方向
        if from_x == to_x:
            direction = '进' if (is_red and to_y < from_y) or (not is_red and to_y > from_y) else '退'
            steps = abs(from_y - to_y)
            return f'{piece_name}{numbers[from_col]}{direction}{numbers[steps]}'
        else:
            direction = '平'
            return f'{piece_name}{numbers[from_col]}{direction}{numbers[to_col]}'

    def _draw_moves_history(self):
        """绘制走子历史记录"""
        if not self.moves_history:
            return
            
        # 设置记录区域
        history_area_x = self.margin + self.board_width * self.block_size + self.margin
        history_area_y = self.margin
        line_height = 25
        max_visible_lines = (self.screen_height - 2 * self.margin - 50) // line_height
        total_height = len(self.moves_history) * line_height
        
        # 处理鼠标滚轮事件
        for event in pygame.event.get(pygame.MOUSEWHEEL):
            if event.y != 0:  # 滚轮移动
                mouse_pos = pygame.mouse.get_pos()
                # 检查鼠标是否在历史记录区域内
                if (history_area_x <= mouse_pos[0] <= history_area_x + self.history_area_width and
                    history_area_y <= mouse_pos[1] <= history_area_y + self.screen_height - 2 * self.margin):
                    self.scroll_offset = max(0, min(self.scroll_offset - event.y * 20,
                                                  max(0, total_height - max_visible_lines * line_height)))
                    self.history_needs_update = True
        
        # 如果需要更新历史记录
        if self.history_needs_update or self.history_surface is None:
            # 创建一个临时surface来绘制记录
            self.history_surface = pygame.Surface((self.history_area_width, max(total_height, self.screen_height - 2 * self.margin)))
            self.history_surface.fill((245, 245, 245))
            
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 18)
            
            # 绘制所有记录
            for i, move in enumerate(self.moves_history):
                color = RED if i % 2 == 0 else BLACK
                text = font.render(f"{i//2 + 1}. {move}", True, color)
                text_rect = text.get_rect(x=10, y=i * line_height)
                self.history_surface.blit(text, text_rect)
            
            self.history_needs_update = False
        
        # 绘制记录区域边框
        pygame.draw.rect(self.screen, (245, 245, 245), pygame.Rect(history_area_x, history_area_y,
                                                                  self.history_area_width, self.screen_height - 2 * self.margin))
        pygame.draw.rect(self.screen, (180, 180, 180), pygame.Rect(history_area_x, history_area_y,
                                                                  self.history_area_width, self.screen_height - 2 * self.margin), 2)
        
        # 绘制标题
        title_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)
        title = title_font.render("走子记录", True, BLACK)
        title_rect = title.get_rect(center=(history_area_x + self.history_area_width//2, history_area_y + 20))
        self.screen.blit(title, title_rect)
        
        # 创建一个裁剪区域
        clip_rect = pygame.Rect(history_area_x, history_area_y + 50,
                               self.history_area_width, self.screen_height - 2 * self.margin - 50)
        self.screen.set_clip(clip_rect)
        
        # 将记录surface绘制到屏幕上，考虑滚动偏移量
        start_y = history_area_y + 50 - self.scroll_offset
        self.screen.blit(self.history_surface, (history_area_x, start_y))
        
        # 重置裁剪区域
        self.screen.set_clip(None)
        
        # 如果记录超出显示区域，绘制滚动条
        if total_height > (self.screen_height - 2 * self.margin - 50):
            scroll_area_height = self.screen_height - 2 * self.margin - 50
            scroll_height = max(30, scroll_area_height * max_visible_lines * line_height / total_height)
            scroll_pos = scroll_area_height * self.scroll_offset / (total_height - max_visible_lines * line_height)
            pygame.draw.rect(self.screen, (200, 200, 200),
                           (history_area_x + self.history_area_width - 10,
                            history_area_y + 50 + scroll_pos,
                            8, scroll_height))


    def run(self):
        # 导入AI模块
        from src.xiangqi.ai import XiangqiAI
        
        # 游戏模式选择界面
        selected_mode = 0  # 0: 双人对战, 1: 人机对战
        while not self.game_started:
            self.screen.fill((240, 240, 240))
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
            title = font.render("中国象棋", True, BLACK)
            title_rect = title.get_rect(center=(self.screen_width//2, 100))
            self.screen.blit(title, title_rect)
            
            # 创建按钮
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
            pvp_text = font.render("双人对战", True, BLACK)
            pve_text = font.render("人机对战", True, BLACK)
            pvp_rect = pvp_text.get_rect(center=(self.screen_width//2, 200))
            pve_rect = pve_text.get_rect(center=(self.screen_width//2, 300))
            
            # 绘制按钮
            pvp_color = YELLOW if selected_mode == 0 else (200, 200, 200)
            pve_color = YELLOW if selected_mode == 1 else (200, 200, 200)
            pygame.draw.rect(self.screen, pvp_color, pvp_rect.inflate(40, 20))
            pygame.draw.rect(self.screen, pve_color, pve_rect.inflate(40, 20))
            self.screen.blit(pvp_text, pvp_rect)
            self.screen.blit(pve_text, pve_rect)
            
            # 如果选择了人机对战，显示难度选择
            if self.vs_ai:
                difficulties = [('简单', 'easy'), ('中等', 'normal'), ('困难', 'hard')]
                self.selected_difficulty = 0 if not hasattr(self, 'selected_difficulty') else self.selected_difficulty
                
                for i, (text, _) in enumerate(difficulties):
                    diff_text = font.render(text, True, BLACK)
                    diff_rect = diff_text.get_rect(center=(self.screen_width//2, 400 + i*60))
                    color = YELLOW if i == self.selected_difficulty else (200, 200, 200)
                    pygame.draw.rect(self.screen, color, diff_rect.inflate(40, 20))
                    self.screen.blit(diff_text, diff_rect)
            
            pygame.display.flip()
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if pvp_rect.inflate(40, 20).collidepoint(mouse_pos):
                        self.vs_ai = False
                        self.game_started = True
                    elif pve_rect.inflate(40, 20).collidepoint(mouse_pos):
                        self.vs_ai = True
                        selected_mode = 1
                        if not self.ai:
                            self.ai = XiangqiAI(self.ai_difficulty)
                    elif self.vs_ai:
                        for i, (_, diff) in enumerate(difficulties):
                            diff_rect = pygame.Rect(self.screen_width//2 - 70, 400 + i*60 - 15, 140, 40)
                            if diff_rect.collidepoint(mouse_pos):
                                self.selected_difficulty = i
                                self.ai_difficulty = difficulties[i][1]
                                self.ai = XiangqiAI(self.ai_difficulty)
                                self.game_started = True
                elif event.type == pygame.KEYDOWN:
                    if not self.vs_ai:
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            selected_mode = (selected_mode + 1) % 2
                            if selected_mode == 1:
                                self.vs_ai = True
                            else:
                                self.vs_ai = False
                        elif event.key == pygame.K_RETURN:
                            if selected_mode == 0:
                                self.game_started = True
                            else:
                                self.vs_ai = True
                    elif self.vs_ai:
                        if event.key == pygame.K_UP:
                            self.selected_difficulty = (self.selected_difficulty - 1) % 3
                            self.ai_difficulty = difficulties[self.selected_difficulty][1]
                        elif event.key == pygame.K_DOWN:
                            self.selected_difficulty = (self.selected_difficulty + 1) % 3
                            self.ai_difficulty = difficulties[self.selected_difficulty][1]
                        elif event.key == pygame.K_RETURN:
                            self.ai = XiangqiAI(self.ai_difficulty)
                            self.game_started = True
                        elif event.key == pygame.K_ESCAPE:
                            self.vs_ai = False
                            selected_mode = 0
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
        
        # 主游戏循环
        while True:
            self._draw_board()
            self._draw_pieces()
            self._draw_moves_history()
            
            # 如果是AI回合
            if self.vs_ai and not self.is_red_turn and not self.game_over:
                ai_move = self.ai.make_move(self.board, self.is_red_turn)
                if ai_move:
                    from_pos, to_pos = ai_move
                    from_x, from_y = from_pos
                    to_x, to_y = to_pos
                    
                    # 记录走子
                    piece = self.board[from_y][from_x]
                    move_text = self._get_move_text((from_x, from_y), (to_x, to_y), piece)
                    self.moves_history.append(move_text)
                    self.history_needs_update = True
                    
                    # 执行移动
                    self.board[to_y][to_x] = self.board[from_y][from_x]
                    self.board[from_y][from_x] = None
                    self.is_red_turn = not self.is_red_turn
                    
                    # 检查胜利条件
                    self._check_win()
            
            pygame.display.flip()
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    if event.button == 1:  # 左键点击
                        mouse_pos = pygame.mouse.get_pos()
                        board_pos = self._get_board_pos(mouse_pos)
                        
                        if board_pos:
                            x, y = board_pos
                            if self.selected_piece:
                                # 如果已经选择了棋子，尝试移动
                                from_x, from_y = self.selected_piece
                                if self._is_valid_move((from_x, from_y), (x, y)):
                                    # 记录走子
                                    piece = self.board[from_y][from_x]
                                    move_text = self._get_move_text((from_x, from_y), (x, y), piece)
                                    self.moves_history.append(move_text)
                                    self.history_needs_update = True
                                    
                                    # 执行移动
                                    self.board[y][x] = self.board[from_y][from_x]
                                    self.board[from_y][from_x] = None
                                    self.selected_piece = None
                                    self.is_red_turn = not self.is_red_turn
                                    
                                    # 检查胜利条件
                                    self._check_win()
                                else:
                                    # 如果移动不合法，取消选择
                                    self.selected_piece = None
                            else:
                                # 选择新棋子
                                piece = self.board[y][x]
                                if piece and ((piece['color'] == 'red' and self.is_red_turn) or 
                                            (piece['color'] == 'black' and not self.is_red_turn)):
                                    self.selected_piece = (x, y)
                    elif event.button == 3:  # 右键点击
                        self.selected_piece = None
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # 滚轮向上
                    self.scroll_offset = max(0, self.scroll_offset - 30)
                    self.history_needs_update = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # 滚轮向下
                    max_scroll = max(0, len(self.moves_history) * 30 - (self.screen_height - 2 * self.margin - 50))
                    self.scroll_offset = min(max_scroll, self.scroll_offset + 30)
                    self.history_needs_update = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
            
            self.clock.tick(60)