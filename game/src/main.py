import pygame
from src.breakout.game import BreakoutGame
from src.game2048.game import Game2048
from src.minesweeper.game import MinesweeperGame
from src.plane.game import PlaneGame
from src.sudoku.game import SudokuGame
from src.memory.game import MemoryGame
from src.snake.game import SnakeGame
from src.tetris.game import TetrisGame
from src.common.colors import *

def draw_menu(screen, selected, page=0):
    """绘制游戏选择菜单"""
    screen.fill(BACKGROUND)
    title_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
    menu_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 32)
    
    # 绘制标题
    title = title_font.render("游戏合集", True, WHITE)
    screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 30))
    
    # 游戏选项列表
    options = ["1. 打砖块", "2. 2048", "3. 扫雷", "4. 飞机大战", "5. 数独", "6. 记忆翻牌", "7. 贪吃蛇", "8. 俄罗斯方块", "9. 退出"]
    
    # 分页设置
    items_per_page = 6
    total_pages = (len(options) + items_per_page - 1) // items_per_page
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, len(options))
    
    # 绘制当前页的选项
    menu_start_x = 100
    menu_start_y = 120
    for i, option in enumerate(options[start_idx:end_idx]):
        color = WHITE if (i + start_idx) != selected else RED
        text = menu_font.render(option, True, color)
        screen.blit(text, (menu_start_x, menu_start_y + i * 60))
    
    # 绘制页码信息
    page_info = f"第 {page + 1}/{total_pages} 页"
    page_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)
    page_text = page_font.render(page_info, True, WHITE)
    screen.blit(page_text, (screen.get_width()//2 - page_text.get_width()//2, screen.get_height() - 50))
    
    # 绘制操作提示
    hint_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 20)
    hints = [
        "↑↓: 选择游戏",
        "←→: 翻页",
        "数字键: 快速选择",
        "Enter: 确认",
        "Esc: 退出"
    ]
    hint_x = screen.get_width() - 180
    for i, hint in enumerate(hints):
        hint_text = hint_font.render(hint, True, WHITE)
        screen.blit(hint_text, (hint_x, 120 + i * 30))
    
    pygame.display.flip()

def main():
    # 初始化pygame并检查返回值
    init_result = pygame.init()
    if init_result[1] != 0:
        print(f"Pygame初始化失败，错误数：{init_result[1]}")
        return
        
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("游戏合集")
    clock = pygame.time.Clock()
    
    selected = 0
    current_page = 0
    items_per_page = 6
    running = True
    
    while running:
        clock.tick(30)
        draw_menu(screen, selected, current_page)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 9
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 9
                elif event.key == pygame.K_LEFT:
                    if current_page > 0:
                        current_page -= 1
                        selected = current_page * items_per_page
                elif event.key == pygame.K_RIGHT:
                    if (current_page + 1) * items_per_page < 9:
                        current_page += 1
                        selected = current_page * items_per_page
                # 数字键快速选择
                elif event.key in range(pygame.K_1, pygame.K_9 + 1):
                    num = event.key - pygame.K_1
                    if num < 9:  # 确保选择有效
                        selected = num
                        current_page = num // items_per_page
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        game = BreakoutGame()
                        game.run()
                    elif selected == 1:
                        game = Game2048()
                        game.run()
                    elif selected == 2:
                        game = MinesweeperGame()
                        game.run()
                    elif selected == 3:
                        game = PlaneGame()
                        game.run()
                    elif selected == 4:
                        game = SudokuGame()
                        game.run()
                    elif selected == 5:
                        game = MemoryGame()
                        game.run()
                    elif selected == 6:
                        game = SnakeGame()
                        game.run()
                    elif selected == 7:
                        game = TetrisGame()
                        game.run()
                    elif selected == 8:
                        running = False
                    # 重置窗口大小
                    screen = pygame.display.set_mode((800, 600))
                    pygame.display.set_caption("游戏合集")
    
    pygame.quit()

if __name__ == "__main__":
    main()