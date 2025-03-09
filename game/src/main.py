import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
from src.bomberman.game import BombermanGame
from src.flappybird.game import FlappyBirdGame
from src.jungle.game import JungleGame
from src.spaceshield.game import SpaceshieldGame
from src.common.colors import *

options = [
    "1. 打砖块",
    "2. 2048",
    "3. 扫雷",
    "4. 飞机大战",
    "5. 数独",
    "6. 记忆翻牌",
    "7. 贪吃蛇",
    "8. 俄罗斯方块",
    "9. 五子棋",
    "10. 连连看",
    "11. 中国象棋",
    "12. 炸弹人",
    "13. Flappy Bird",
"14. 军棋",
"15. 太空防御战"
]

def draw_menu(screen, selected, page=0):
    screen.fill(BACKGROUND)
    title_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
    menu_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 32)
    
    title = title_font.render("游戏合集", True, WHITE)
    screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 30))
    
    items_per_page = 5
    total_pages = (len(options) + items_per_page - 1) // items_per_page
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, len(options))
    
    current_options = options[start_idx:min(start_idx + 5, end_idx)]
    current_options.append("6. 退出")
    
    menu_start_x = 100
    menu_start_y = 120
    for i, option in enumerate(current_options):
        option = option[option.find(" ") + 1:]
        option = f"{i + 1}. {option}"
        color = RED if i == selected else WHITE
        text = menu_font.render(option, True, color)
        screen.blit(text, (menu_start_x, menu_start_y + i * 60))
    
    start_game_num = start_idx + 1
    end_game_num = min(end_idx, len(options))
    page_info = f"第 {page + 1}/{total_pages} 页 (第{start_game_num}-{end_game_num}个游戏)"
    page_text = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24).render(page_info, True, WHITE)
    screen.blit(page_text, (screen.get_width()//2 - page_text.get_width()//2, screen.get_height() - 50))
    
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
                        selected -= 1
                    else:
                        if current_page > 0:
                            current_page -= 1
                            selected = min(items_per_page, len(options) - current_page * items_per_page)
                elif event.key == pygame.K_DOWN:
                    current_page_options = min(items_per_page, len(options) - current_page * items_per_page)
                    if selected < current_page_options:
                        selected += 1
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
                elif event.key in range(pygame.K_1, pygame.K_6 + 1) or event.key in range(pygame.K_KP1, pygame.K_KP6 + 1):
                    num = event.key - pygame.K_1 if event.key <= pygame.K_6 else event.key - pygame.K_KP1
                    page_start = current_page * items_per_page
                    current_page_options = min(items_per_page, len(options) - current_page * items_per_page)
                    if num <= current_page_options:
                        selected = num - 1  # 数字键对应索引需减1
                    elif num == 5:
                        selected = current_page_options
                elif event.key == pygame.K_RETURN:
                    current_page_options = min(items_per_page, len(options) - current_page * items_per_page)
                    if selected == current_page_options:
                        running = False
                        continue

                    game_index = current_page * items_per_page + selected
                    if game_index < len(options):
                        if game_index == 0:
                            game = BreakoutGame()
                        elif game_index == 1:
                            game = Game2048()
                        elif game_index == 2:
                            game = MinesweeperGame()
                        elif game_index == 3:
                            game = PlaneGame()
                        elif game_index == 4:
                            game = SudokuGame()
                        elif game_index == 5:
                            game = MemoryGame()
                        elif game_index == 6:
                            game = SnakeGame()
                        elif game_index == 7:
                            game = TetrisGame()
                        elif game_index == 8:
                            game = GomokuGame()
                        elif game_index == 9:
                            game = LianLianKanGame()
                        elif game_index == 10:
                            game = XiangqiGame()
                        elif game_index == 11:
                            game = BombermanGame()
                        elif game_index == 12:
                            game = FlappyBirdGame()
                        elif game_index == 13:
                            game = JungleGame()
                        elif game_index == 14:
                            game = SpaceshieldGame()
                        game.run()
                        screen = pygame.display.set_mode((800, 600))
                        pygame.display.set_caption("游戏合集")
                    else:
                        running = False

if __name__ == "__main__":
    main()
