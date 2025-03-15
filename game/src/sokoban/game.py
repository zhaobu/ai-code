import pygame
import os
from typing import List, Tuple, Optional
from ..common.colors import *

class SokobanGame:
    TILE_SIZE = 60
    
    # 游戏元素的字符表示
    WALL = '#'
    BOX = '$'
    TARGET = '.'
    PLAYER = '@'
    BOX_ON_TARGET = '*'
    PLAYER_ON_TARGET = '+'
    FLOOR = ' '
    
    def __init__(self):
        pygame.init()
        self.level = 0
        self.moves = 0
        self.move_history = []
        self.start_time = pygame.time.get_ticks()
        self.best_records = {}
        self.load_levels()
        self.reset_level()
        
        # 加载图像资源
        self.images = {}
        self.load_images()
        
        # 初始化字体
        self.font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)
        
        # 设置窗口大小
        self.screen = None
        self.resize_screen()
        
        # 游戏规则说明
        self.help_text = [
            "游戏规则：",
            "1. 使用方向键移动角色",
            "2. 将所有箱子(黄色)推到目标点(绿色)",
            "3. R键重置当前关卡",
            "4. Z键撤销上一步",
            "5. 通关后按N键进入下一关",
            "6. H键显示/隐藏帮助"
        ]
        self.show_help = False
    
    def load_levels(self):
        """加载预设关卡数据"""
        self.levels = [
            [
                "  ####",
                "###  #",
                "#. $ #",
                "#@$ .#",
                "#.$ .#",
                "#   ##",
                "#####"
                
            ],
            [
                "########",
                "#  .#  #",
                "#  $   #",
                "#.$@$. #",
                "#  $   #",
                "#  .#  #",
                "########"
            ],
            [
                "  ####  ",
                "###  ###",
                "#   $  #",
                "# #.#  #",
                "# #@$ ##",
                "# $.# #",
                "##$.  #",
                " #.#  #",
                " #   ##",
                " #####"
            ],
            [
                "########",
                "#      #",
                "# .**@.#",
                "#  $$ ##",
                "# #   #",
                "#.#####",
                "#     #",
                "#######"
            ],
            [
                "#######",
                "#     #",
                "# .$. #",
                "##$@$##",
                "# .$. #",
                "#     #",
                "#######"
            ]
        ]
    
    def load_images(self):
        """加载游戏图像资源"""
        image_dir = os.path.join(os.path.dirname(__file__), 'images')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
            
        # 使用颜色块替代图片
        self.images = {
            self.WALL: self.create_surface(GRAY),
            self.BOX: self.create_surface(YELLOW),
            self.TARGET: self.create_surface(GREEN),
            self.PLAYER: self.create_surface(BLUE),
            self.BOX_ON_TARGET: self.create_surface(BROWN),
            self.PLAYER_ON_TARGET: self.create_surface(PURPLE),
            self.FLOOR: self.create_surface(WHITE)
        }
    
    def create_surface(self, color: Tuple[int, int, int]) -> pygame.Surface:
        """创建指定颜色的表面，添加渐变效果"""
        surface = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
        rect = surface.get_rect()
        
        # 创建渐变效果
        for i in range(rect.height):
            progress = i / rect.height
            current_color = tuple(int(c * (0.7 + 0.3 * (1 - progress))) for c in color)
            pygame.draw.line(surface, current_color, (0, i), (rect.width, i))
        
        # 添加边框和高光效果
        pygame.draw.rect(surface, tuple(min(255, c + 50) for c in color), rect, 2)
        pygame.draw.line(surface, tuple(min(255, c + 80) for c in color), (0, 0), (rect.width, 0), 2)
        pygame.draw.line(surface, tuple(min(255, c + 80) for c in color), (0, 0), (0, rect.height), 2)
        return surface
    
    def resize_screen(self):
        """调整窗口大小以适应当前关卡"""
        if not self.current_level:
            return
        width = len(self.current_level[0]) * self.TILE_SIZE + 120  # 增加边距以显示完整墙壁
        height = len(self.current_level) * self.TILE_SIZE + 150  # 增加信息栏空间
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f'推箱子 - 第{self.level + 1}关')
    
    def reset_level(self):
        """重置当前关卡"""
        if 0 <= self.level < len(self.levels):
            self.current_level = [list(row) for row in self.levels[self.level]]
            self.moves = 0
            self.move_history = []
            self.find_player()
            self.resize_screen()
    
    def find_player(self) -> None:
        """找到玩家的位置"""
        for y, row in enumerate(self.current_level):
            for x, cell in enumerate(row):
                if cell in (self.PLAYER, self.PLAYER_ON_TARGET):
                    self.player_pos = (x, y)
                    return
    
    def is_completed(self) -> bool:
        """检查当前关卡是否完成"""
        return all(self.BOX not in row for row in self.current_level)
    
    def move(self, dx: int, dy: int) -> bool:
        """移动玩家"""
        x, y = self.player_pos
        new_x, new_y = x + dx, y + dy
        
        # 检查是否超出边界
        if not (0 <= new_x < len(self.current_level[0]) and 0 <= new_y < len(self.current_level)):
            return False
        
        current = self.current_level[y][x]
        target = self.current_level[new_y][new_x]
        
        # 移动到空地或目标点
        if target in (self.FLOOR, self.TARGET):
            self.move_player(x, y, new_x, new_y)
            return True
        
        # 推箱子
        if target in (self.BOX, self.BOX_ON_TARGET):
            box_x, box_y = new_x + dx, new_y + dy
            
            # 检查箱子移动的目标位置是否有效
            if not (0 <= box_x < len(self.current_level[0]) and 0 <= box_y < len(self.current_level)):
                return False
            
            box_target = self.current_level[box_y][box_x]
            if box_target in (self.FLOOR, self.TARGET):
                # 记录移动历史
                self.move_history.append((x, y, new_x, new_y, box_x, box_y))
                
                # 移动箱子
                is_box_on_target = box_target == self.TARGET
                self.current_level[box_y][box_x] = self.BOX_ON_TARGET if is_box_on_target else self.BOX
                
                # 移动玩家
                self.move_player(x, y, new_x, new_y)
                self.moves += 1
                return True
        
        return False
    
    def move_player(self, x: int, y: int, new_x: int, new_y: int) -> None:
        """更新玩家位置"""
        current = self.current_level[y][x]
        target = self.current_level[new_y][new_x]
        
        # 更新原位置
        self.current_level[y][x] = self.TARGET if current == self.PLAYER_ON_TARGET else self.FLOOR
        
        # 更新新位置
        self.current_level[new_y][new_x] = self.PLAYER_ON_TARGET if target == self.TARGET else self.PLAYER
        
        self.player_pos = (new_x, new_y)
    
    def undo_move(self) -> bool:
        """撤销上一步移动"""
        if not self.move_history:
            return False
        
        x, y, box_x, box_y, old_box_x, old_box_y = self.move_history.pop()
        
        # 恢复箱子位置
        current_box = self.current_level[old_box_y][old_box_x]
        target_box = self.current_level[box_y][box_x]
        
        self.current_level[box_y][box_x] = self.TARGET if target_box == self.BOX_ON_TARGET else self.FLOOR
        self.current_level[old_box_y][old_box_x] = self.BOX_ON_TARGET if current_box == self.TARGET else self.BOX
        
        # 恢复玩家位置
        self.move_player(box_x, box_y, x, y)
        self.moves -= 1
        return True
    
    def draw(self) -> None:
        """绘制游戏画面"""
        self.screen.fill(WHITE)
        
        # 绘制游戏区域
        for y, row in enumerate(self.current_level):
            for x, cell in enumerate(row):
                # 绘制地板
                self.screen.blit(self.images[self.FLOOR], (x * self.TILE_SIZE, y * self.TILE_SIZE))
                
                # 绘制其他游戏元素
                if cell != self.FLOOR:
                    self.screen.blit(self.images[cell], (x * self.TILE_SIZE, y * self.TILE_SIZE))
        
        # 绘制信息栏
        game_time = (pygame.time.get_ticks() - self.start_time) // 1000
        best_record = self.best_records.get(self.level, '无记录')
        
        # 创建信息面板
        info_panel = pygame.Surface((self.screen.get_width(), 50))
        info_panel.fill((240, 240, 240))
        pygame.draw.rect(info_panel, (200, 200, 200), info_panel.get_rect(), 2)
        
        # 绘制时间信息
        time_text = f'时间: {game_time}秒'
        time_surface = self.font.render(time_text, True, (80, 80, 80))
        time_rect = time_surface.get_rect(left=20, centery=25)
        info_panel.blit(time_surface, time_rect)
        
        # 绘制步数信息
        moves_text = f'步数: {self.moves}'
        moves_surface = self.font.render(moves_text, True, (80, 80, 80))
        moves_rect = moves_surface.get_rect(left=info_panel.get_width()//3, centery=25)
        info_panel.blit(moves_surface, moves_rect)
        
        # 绘制最佳记录
        record_text = f'最佳记录: {best_record}步'
        record_surface = self.font.render(record_text, True, (80, 80, 80))
        record_rect = record_surface.get_rect(left=info_panel.get_width()*2//3, centery=25)
        info_panel.blit(record_surface, record_rect)
        
        self.screen.blit(info_panel, (0, self.screen.get_height() - 50))
        
        # 绘制游戏规则说明
        if self.show_help:
            # 创建半透明背景
            overlay = pygame.Surface(self.screen.get_size())
            overlay.fill((0, 0, 0))
            overlay.set_alpha(160)
            self.screen.blit(overlay, (0, 0))
            
            # 创建帮助面板
            help_panel = pygame.Surface((400, 450))
            help_panel.fill((245, 245, 245))
            
            # 添加渐变边框
            border_rect = help_panel.get_rect()
            for i in range(4):
                border_color = (180 - i*10, 180 - i*10, 180 - i*10)
                pygame.draw.rect(help_panel, border_color, border_rect.inflate(-2*i, -2*i), 1)
            
            # 添加标题
            title_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 32)
            title = title_font.render("游戏帮助", True, (60, 60, 60))
            title_rect = title.get_rect(centerx=help_panel.get_width()//2, top=20)
            
            # 添加标题装饰线
            line_width = 200
            line_y = title_rect.bottom + 15
            pygame.draw.line(help_panel, (180, 180, 180),
                           (help_panel.get_width()//2 - line_width//2, line_y),
                           (help_panel.get_width()//2 + line_width//2, line_y), 2)
            
            help_panel.blit(title, title_rect)
            
            # 绘制帮助内容
            help_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)
            y = 90
            for line in self.help_text[1:]:
                text_surface = help_font.render(line, True, (80, 80, 80))
                text_rect = text_surface.get_rect(left=30, top=y)
                help_panel.blit(text_surface, text_rect)
                y += 45
            
            # 添加关闭提示
            close_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)
            close_text = close_font.render("按H键关闭帮助", True, (120, 120, 120))
            close_rect = close_text.get_rect(centerx=help_panel.get_width()//2, bottom=help_panel.get_height()-20)
            help_panel.blit(close_text, close_rect)
            
            # 居中显示帮助面板
            panel_x = (self.screen.get_width() - help_panel.get_width()) // 2
            panel_y = (self.screen.get_height() - help_panel.get_height()) // 2
            self.screen.blit(help_panel, (panel_x, panel_y))
        
        pygame.display.flip()
    
    def run(self) -> None:
        """运行游戏主循环"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    moved = False
                    
                    if event.key == pygame.K_LEFT:
                        moved = self.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        moved = self.move(1, 0)
                    elif event.key == pygame.K_UP:
                        moved = self.move(0, -1)
                    elif event.key == pygame.K_DOWN:
                        moved = self.move(0, 1)
                    elif event.key == pygame.K_r:
                        self.reset_level()
                    elif event.key == pygame.K_z:
                        self.undo_move()
                    elif event.key == pygame.K_n and self.is_completed():
                        self.level = (self.level + 1) % len(self.levels)
                        self.reset_level()
                    elif event.key == pygame.K_h:
                        self.show_help = not self.show_help
                    
                    if moved:
                        pygame.display.set_caption(f'推箱子 - 第{self.level + 1}关 移动次数: {self.moves}')
                        
                        if self.is_completed():
                            # 更新最佳记录
                            if self.level not in self.best_records or self.moves < self.best_records[self.level]:
                                self.best_records[self.level] = self.moves
                            
                            # 显示胜利提示
                            overlay = pygame.Surface(self.screen.get_size())
                            overlay.fill((255, 255, 255))
                            overlay.set_alpha(180)
                            self.screen.blit(overlay, (0, 0))
                            
                            # 创建胜利消息
                            victory_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
                            victory_text = victory_font.render('恭喜通关！', True, (50, 205, 50))
                            victory_rect = victory_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 40))
                            
                            # 添加阴影效果
                            shadow_text = victory_font.render('恭喜通关！', True, (30, 180, 30))
                            shadow_rect = shadow_text.get_rect(center=(victory_rect.centerx + 3, victory_rect.centery + 3))
                            self.screen.blit(shadow_text, shadow_rect)
                            self.screen.blit(victory_text, victory_rect)
                            
                            # 显示按键提示
                            hint_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)
                            hint_text = hint_font.render('按N键进入下一关', True, (100, 100, 100))
                            hint_rect = hint_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 20))
                            self.screen.blit(hint_text, hint_rect)
                            
                            pygame.display.flip()
                            
                            if self.level == len(self.levels) - 1:
                                print("恭喜！你已经完成了所有关卡！")
                                running = False
                            else:
                                print(f"恭喜通过第{self.level + 1}关！按N键进入下一关。")
            
            self.draw()
            clock.tick(30)
        
        # 清理资源
        for surface in self.images.values():
            del surface
        self.images.clear()
        self.font = None
        self.screen = None
        # 重置屏幕状态
        pygame.display.set_mode((800, 600))
        pygame.display.set_caption("游戏合集")
        pygame.display.flip()
        pygame.font.init()  # 重新初始化字体系统

def main():
    game = SokobanGame()
    game.run()

if __name__ == '__main__':
    main()