import random
from typing import List, Tuple, Dict, Optional

class XiangqiAI:
    def __init__(self, difficulty: str = 'normal'):
        """初始化象棋AI
        
        Args:
            difficulty: AI难度，可选值为'easy', 'normal', 'hard'
        """
        self.difficulty = difficulty
        # 棋子价值表
        self.piece_values = {
            'general': 10000,  # 将/帅
            'advisor': 200,    # 士/仕
            'elephant': 200,   # 象/相
            'horse': 400,      # 马
            'chariot': 900,    # 车
            'cannon': 450,     # 炮
            'soldier': 100     # 兵/卒
        }
        
        # 位置价值表（简化版）
        # 这里只是一个简单的示例，实际的位置价值会更复杂
        self.position_values = {
            'soldier': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [5, 10, 10, 15, 15, 15, 10, 10, 5],
                [10, 15, 20, 30, 30, 30, 20, 15, 10],
                [15, 20, 30, 40, 40, 40, 30, 20, 15],
                [20, 30, 40, 50, 50, 50, 40, 30, 20],
                [25, 35, 45, 55, 55, 55, 45, 35, 25]
            ]
        }
    
    def evaluate_board(self, board: List[List[Dict]]) -> int:
        """评估当前棋盘状态的分数
        
        Args:
            board: 棋盘状态
            
        Returns:
            分数，正数表示红方有利，负数表示黑方有利
        """
        score = 0
        
        # 计算棋子价值
        for y in range(len(board)):
            for x in range(len(board[0])):
                piece = board[y][x]
                if piece is not None:
                    piece_type = piece['type']
                    piece_color = piece['color']
                    piece_value = self.piece_values.get(piece_type, 0)
                    
                    # 红方为正，黑方为负
                    if piece_color == 'red':
                        score += piece_value
                        # 加上位置价值（如果有）
                        if piece_type == 'soldier':
                            score += self.position_values['soldier'][y][x]
                    else:  # 黑方
                        score -= piece_value
                        # 加上位置价值（如果有）
                        if piece_type == 'soldier':
                            # 黑方的位置价值需要翻转棋盘
                            score -= self.position_values['soldier'][9-y][x]
        
        # 根据难度调整随机性
        if self.difficulty == 'easy':
            score += random.randint(-300, 300)
        elif self.difficulty == 'normal':
            score += random.randint(-100, 100)
        
        return score
    
    def get_all_valid_moves(self, board: List[List[Dict]], is_red_turn: bool) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """获取所有合法移动
        
        Args:
            board: 棋盘状态
            is_red_turn: 是否是红方回合
            
        Returns:
            所有合法移动的列表，每个移动是一个元组 ((from_x, from_y), (to_x, to_y))
        """
        valid_moves = []
        board_height = len(board)
        board_width = len(board[0])
        
        # 遍历棋盘找出所有己方棋子
        for from_y in range(board_height):
            for from_x in range(board_width):
                piece = board[from_y][from_x]
                if piece is not None and piece['color'] == ('red' if is_red_turn else 'black'):
                    # 对每个可能的目标位置检查移动是否合法
                    for to_y in range(board_height):
                        for to_x in range(board_width):
                            if self._is_valid_move(board, (from_x, from_y), (to_x, to_y)):
                                valid_moves.append(((from_x, from_y), (to_x, to_y)))
        
        return valid_moves
    
    def _is_valid_move(self, board: List[List[Dict]], from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """检查移动是否合法（与游戏类中的逻辑相同）"""
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        # 如果起始位置和目标位置相同，则不合法
        if from_x == to_x and from_y == to_y:
            return False
        
        # 确保起始位置有棋子
        if board[from_y][from_x] is None:
            return False
        
        # 确保目标位置没有同色棋子
        if board[to_y][to_x] is not None and board[to_y][to_x]['color'] == board[from_y][from_x]['color']:
            return False
        
        piece = board[from_y][from_x]
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
            if board[elephant_eye_y][elephant_eye_x] is not None:
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
                if board[horse_leg_y][from_x] is not None:
                    return False
            else:
                # 横向移动，检查纵向马腿
                horse_leg_x = from_x + (1 if to_x > from_x else -1)
                if board[from_y][horse_leg_x] is not None:
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
                    if board[y][from_x] is not None:
                        return False
            else:
                # 横向移动
                start, end = min(from_x, to_x), max(from_x, to_x)
                for x in range(start + 1, end):
                    if board[from_y][x] is not None:
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
                    if board[y][from_x] is not None:
                        piece_count += 1
            else:
                # 横向移动
                start, end = min(from_x, to_x), max(from_x, to_x)
                for x in range(start + 1, end):
                    if board[from_y][x] is not None:
                        piece_count += 1
            
            # 炮的移动规则：移动时不能有棋子，吃子时必须有且仅有一个棋子作为炮架
            if board[to_y][to_x] is None:
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
    
    def make_move(self, board: List[List[Dict]], is_red_turn: bool) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """AI决策下一步移动
        
        Args:
            board: 棋盘状态
            is_red_turn: 是否是红方回合
            
        Returns:
            选择的移动，格式为 ((from_x, from_y), (to_x, to_y))，如果没有合法移动则返回None
        """
        valid_moves = self.get_all_valid_moves(board, is_red_turn)
        if not valid_moves:
            return None
        
        # 根据难度选择不同的策略
        if self.difficulty == 'easy':
            # 简单难度：随机选择一个合法移动
            return random.choice(valid_moves)
        
        # 中等和困难难度：评估每个移动后的局面
        best_move = None
        best_score = float('-inf') if is_red_turn else float('inf')
        
        for move in valid_moves:
            from_pos, to_pos = move
            from_x, from_y = from_pos
            to_x, to_y = to_pos
            
            # 模拟移动
            temp_board = [row[:] for row in board]
            temp_board[to_y][to_x] = temp_board[from_y][from_x]
            temp_board[from_y][from_x] = None
            
            # 评估移动后的局面
            score = self.evaluate_board(temp_board)
            
            # 更新最佳移动
            if is_red_turn:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        
        return best_move or random.choice(valid_moves)  # 如果没有找到最佳移动，随机选择一个