from typing import List, Tuple

# 方块类型定义
SHAPES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]
    ],
    'O': [
        [[1, 1],
         [1, 1]]
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1]],
        [[0, 1],
         [1, 1],
         [0, 1]],
        [[1, 1, 1],
         [0, 1, 0]],
        [[1, 0],
         [1, 1],
         [1, 0]]
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]]
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1]],
        [[1, 1],
         [1, 0],
         [1, 0]],
        [[1, 1, 1],
         [0, 0, 1]],
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1]],
        [[1, 0],
         [1, 0],
         [1, 1]],
        [[1, 1, 1],
         [1, 0, 0]],
        [[1, 1],
         [0, 1],
         [0, 1]]
    ]
}

class Shape:
    def __init__(self, shape_type: str):
        self.shape_type = shape_type
        self.rotations = SHAPES[shape_type]
        self.rotation_index = 0
        self.color = self._get_color()

    def _get_color(self) -> Tuple[int, int, int]:
        """根据方块类型返回颜色"""
        colors = {
            'I': (0, 255, 255),  # Cyan
            'O': (255, 255, 0),  # Yellow
            'T': (128, 0, 128),  # Purple
            'S': (0, 255, 0),    # Green
            'Z': (255, 0, 0),    # Red
            'J': (0, 0, 255),    # Blue
            'L': (255, 165, 0)   # Orange
        }
        return colors[self.shape_type]

    def rotate(self) -> None:
        """旋转方块"""
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)

    def get_shape(self) -> List[List[int]]:
        """获取当前旋转状态的方块形状"""
        return self.rotations[self.rotation_index]