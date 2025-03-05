import pygame
from src.breakout.game import BreakoutGame
from src.game2048.game import Game2048
from src.minesweeper.game import MinesweeperGame
from src.plane.game import PlaneGame
from src.sudoku.game import SudokuGame
from src.memory.game import MemoryGame
from src.snake.game import SnakeGame
from src.tetris.game import TetrisGame
from src.gomoku.game import GomokuGame
from src.lianliankan.game import LianLianKanGame
from src.xiangqi.game import XiangqiGame
from src.common.colors import *
from src.lianliankan.game import LianLianKanGame
from src.common.colors import *

options = ["1. 打砖块", "2. 2048", "3. 扫雷", "4. 飞机大战", "5. 数独", "6. 记忆翻牌", "7. 贪吃蛇", "8. 俄罗斯方块", "9. 五子棋", "10. 连连看", "11. 中国象棋"]

def draw_menu(screen, selected, page=0):
    """绘制游戏选择菜单"""
    screen.fill(BACKGROUND)
    title_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
    menu_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 32)
    
    # 绘制标题
    title = title_font.render("游戏合集", True, WHITE)
    screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 30))
    
    # 分页设置
    items_per_page = 5
    total_pages = (len(options) + items_per_page - 1) // items_per_page
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, len(options))
    
    # 获取当前页的游戏选项（最多5个，为退出选项预留空间）
    current_options = options[start_idx:min(start_idx + 5, end_idx)]
    
    # 添加退出选项
    current_options.append("6. 退出")
    
    # 绘制当前页的选项
    menu_start_x = 100
    menu_start_y = 120
    for i, option in enumerate(current_options):
        # 移除原始序号
        option = option[option.find(" ") + 1:]
        # 添加新的1-6序号
        option = f"{i + 1}. {option}"
        
        # 设置选中项的颜色
        color = RED if i == selected else WHITE
        text = menu_font.render(option, True, color)
        screen.blit(text, (menu_start_x, menu_start_y + i * 60))
    
    # 绘制页码信息和游戏序号范围
    start_game_num = start_idx + 1
    end_game_num = min(end_idx, len(options))
    page_info = f"第 {page + 1}/{total_pages} 页 (第{start_game_num}-{end_game_num}个游戏)"
    page_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)
    page_text = page_font.render(page_info, True, WHITE)
    screen.blit(page_text, (screen.get_width()//2 - page_text.get_width()//2, screen.get_height() - 50))
    
    # 绘制操作提示
    hint_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 20)
    hints = [
        "↑↓: 选择游戏",
        "←→: 翻页",
        "数字键: 快速选择(1-6)",
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
    items_per_page = 5
    running = True
    
    while running:
        clock.tick(30)
        draw_menu(screen, selected, current_page)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected > 0:
                        selected = (selected - 1)
                    else:
                        if current_page > 0:
                            current_page -= 1
                            selected = min(items_per_page, len(options) - current_page * items_per_page)
                elif event.key == pygame.K_DOWN:
                    current_page_options = min(items_per_page, len(options) - current_page * items_per_page)
                    if selected < current_page_options:
                        selected = (selected + 1)
                    else:
                        if (current_page + 1) * items_per_page < len(options):
                            current_page += 1
                            selected = 0
                elif event.key == pygame.K_LEFT:
                    if current_page > 0:
                        current_page -= 1
                        selected = 0
                elif event.key == pygame.K_RIGHT:
                    if (current_page + 1) * items_per_page < len(options):
                        current_page += 1
                        selected = 0
                # 数字键快速选择
                elif event.key in range(pygame.K_1, pygame.K_6 + 1) or event.key in range(pygame.K_KP1, pygame.K_KP6 + 1):
                    num = event.key - pygame.K_1 if event.key <= pygame.K_6 else event.key - pygame.K_KP1
                    page_start = current_page * items_per_page
                    current_page_options = min(items_per_page, len(options) - current_page * items_per_page)
                    if num <= current_page_options:
                        selected = num
                    elif num == 5:  # 选择退出选项
                        selected = current_page_options
                elif event.key == pygame.K_RETURN:
                    # 检查是否选择了退出选项
                    current_page_options = min(items_per_page, len(options) - current_page * items_per_page)
                    if selected == current_page_options:  # 如果选中了退出选项
                        running = False
                        continue
                    
                    game_index = current_page * items_per_page + selected
                    if game_index < len(options):
                        if game_index == 0:
                            game = BreakoutGame()
                            game.run()
                        elif game_index == 1:
                            game = Game2048()
                            game.run()
                        elif game_index == 2:
                            game = MinesweeperGame()
                            game.run()
                        elif game_index == 3:
                            game = PlaneGame()
                            game.run()
                        elif game_index == 4:
                            game = SudokuGame()
                            game.run()
                        elif game_index == 5:
                            game = MemoryGame()
                            game.run()
                        elif game_index == 6:
                            game = SnakeGame()
                            game.run()
                        elif game_index == 7:
                            game = TetrisGame()
                            game.run()
                        elif game_index == 8:
                            game = GomokuGame()
                            game.run()
                        elif game_index == 9:
                            game = LianLianKanGame()
                            game.run()
                        elif game_index == 10:
                            game = XiangqiGame()
                            game.run()
                        # 重置窗口大小
                        screen = pygame.display.set_mode((800, 600))
                        pygame.display.set_caption("游戏合集")
                    else:
                        running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()