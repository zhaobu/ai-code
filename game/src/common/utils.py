import pygame

def draw_grid(surface, grid_size, color):
    """绘制网格线"""
    width, height = surface.get_size()
    for x in range(0, width, grid_size):
        pygame.draw.line(surface, color, (x, 0), (x, height))
    for y in range(0, height, grid_size):
        pygame.draw.line(surface, color, (0, y), (width, y))

def draw_block(surface, color, position, block_size):
    """绘制单个方块"""
    x, y = position
    pygame.draw.rect(
        surface,
        color,
        pygame.Rect(x * block_size + 1, y * block_size + 1, block_size - 2, block_size - 2)
    )

def to_grid(position, block_size):
    """将像素坐标转换为网格坐标"""
    x, y = position
    return (x // block_size, y // block_size)