import pygame
from src.tetris.game import TetrisGame
from src.snake.game import SnakeGame
from common.colors import *

def draw_menu(screen, selected):
    """绘制游戏选择菜单"""
    screen.fill(BACKGROUND)
    font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
    
    # 绘制标题
    title = font.render("游戏合集", True, WHITE)
    screen.blit(title, (100, 50))
    
    # 绘制菜单项
    options = ["1. 俄罗斯方块", "2. 贪吃蛇", "3. 退出"]
    for i, option in enumerate(options):
        color = WHITE if i != selected else RED
        text = font.render(option, True, color)
        screen.blit(text, (100, 150 + i * 60))
    
    pygame.display.flip()

def main():
    # 初始化pygame并检查返回值
    init_result = pygame.init()
    if init_result[1] != 0:
        print(f"Pygame初始化失败，错误数：{init_result[1]}")
        return
        
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("游戏合集")
    clock = pygame.time.Clock()
    
    selected = 0
    running = True
    
    while running:
        clock.tick(30)
        draw_menu(screen, selected)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        game = TetrisGame()
                        game.run()
                    elif selected == 1:
                        game = SnakeGame()
                        game.run()
                    elif selected == 2:
                        running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()