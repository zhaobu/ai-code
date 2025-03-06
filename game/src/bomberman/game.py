import pygame
import random
from typing import List, Tuple, Dict, Set
from src.common.colors import *
from src.common.utils import draw_block, draw_grid

class BombermanGame:
    def __init__(self, width: int = 15, height: int = 13, block_size: int = 40):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen_width = width * block_size
        self.screen_height = height * block_size
        self.score = 0
        self.game_over = False
        self.win = False
        self.lives = 3
        
        # 初始化游戏地图
        self.map = [[0] * width for _ in range(height)]
        
        # 地图元素定义: 0=空地, 1=固定墙, 2=可破坏墙, 3=道具
        self.player_pos = [1, 1]  # 玩家初始位置
        self.enemies = []  # 敌人位置列表
        self.bombs = []  # 炸弹列表 [x, y, timer]
        self.explosions = []  # 爆炸效果列表 [x, y, timer]
        self.power_ups = {}  # 道具位置字典 {(x,y): 类型}
        
        # 玩家属性
        self.bomb_limit = 1  # 最大炸弹数
        self.bomb_range = 1  # 炸弹爆炸范围
        self.current_bombs = 0  # 当前放置的炸弹数
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("炸弹人")
        self.clock = pygame.time.Clock()
        
        # 生成游戏地图
        self._generate_map()
        
    def _generate_map(self) -> None:
        """生成游戏地图"""
        # 初始化边界墙和固定墙
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1 or (x % 2 == 0 and y % 2 == 0):
                    self.map[y][x] = 1  # 固定墙
        
        # 确保玩家初始位置及其周围是空地
        self.map[1][1] = 0
        self.map[1][2] = 0
        self.map[2][1] = 0
        
        # 随机生成可破坏墙
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.map[y][x] == 0 and not (x <= 2 and y <= 2):  # 避开玩家初始区域
                    if random.random() < 0.7:  # 70%概率生成可破坏墙
                        self.map[y][x] = 2
        
        # 生成敌人
        self._spawn_enemies(3)  # 生成3个敌人
    
    def _spawn_enemies(self, count: int) -> None:
        """生成敌人"""
        self.enemies = []
        possible_positions = []
        
        # 寻找可以放置敌人的位置
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.map[y][x] == 0 and not (x <= 2 and y <= 2):  # 避开玩家初始区域
                    possible_positions.append((x, y))
        
        # 随机选择位置放置敌人
        if possible_positions:
            for _ in range(min(count, len(possible_positions))):
                pos = random.choice(possible_positions)
                self.enemies.append([pos[0], pos[1], random.choice([(1,0), (0,1), (-1,0), (0,-1)])])  # x, y, 方向
                possible_positions.remove(pos)
    
    def _place_bomb(self) -> None:
        """放置炸弹"""
        x, y = self.player_pos
        
        # 检查是否已经有炸弹在该位置
        for bomb in self.bombs:
            if bomb[0] == x and bomb[1] == y:
                return
        
        # 检查是否达到炸弹数量上限
        if self.current_bombs < self.bomb_limit:
            self.bombs.append([x, y, 180])  # 炸弹3秒后爆炸(60fps * 3)
            self.current_bombs += 1
    
    def _explode_bomb(self, bomb_idx: int) -> None:
        """引爆炸弹"""
        x, y, _ = self.bombs[bomb_idx]
        self.explosions.append([x, y, 30])  # 爆炸效果持续0.5秒
        
        # 向四个方向扩散爆炸
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            for r in range(1, self.bomb_range + 1):
                nx, ny = x + dx * r, y + dy * r
                
                # 检查边界
                if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                    break
                
                # 如果是固定墙，爆炸停止
                if self.map[ny][nx] == 1:
                    break
                
                # 如果是可破坏墙，摧毁它并停止爆炸
                if self.map[ny][nx] == 2:
                    self.map[ny][nx] = 0
                    self.score += 10
                    
                    # 有20%概率生成道具
                    if random.random() < 0.2:
                        power_type = random.choice(["bomb", "range", "life"])
                        self.power_ups[(nx, ny)] = power_type
                    
                    self.explosions.append([nx, ny, 30])
                    break
                
                # 添加爆炸效果
                self.explosions.append([nx, ny, 30])
                
                # 检查是否有敌人在爆炸范围内
                for enemy in self.enemies[:]:
                    if int(enemy[0]) == nx and int(enemy[1]) == ny:
                        self.enemies.remove(enemy)
                        self.score += 100
        
        # 移除炸弹
        self.bombs.pop(bomb_idx)
        self.current_bombs -= 1
    
    def _check_player_collision(self) -> bool:
        """检查玩家碰撞"""
        x, y = self.player_pos
        
        # 检查是否与敌人碰撞
        for enemy in self.enemies:
            if int(enemy[0]) == x and int(enemy[1]) == y:
                return True
        
        # 检查是否在爆炸范围内
        for explosion in self.explosions:
            if explosion[0] == x and explosion[1] == y:
                return True
        
        return False
    
    def _collect_power_up(self) -> None:
        """收集道具"""
        x, y = self.player_pos
        pos = (x, y)
        
        if pos in self.power_ups:
            power_type = self.power_ups[pos]
            if power_type == "bomb":
                self.bomb_limit += 1
            elif power_type == "range":
                self.bomb_range += 1
            elif power_type == "life":
                self.lives += 1
            
            del self.power_ups[pos]
            self.score += 50
    
    def _move_enemies(self) -> None:
        """移动敌人"""
        for enemy in self.enemies:
            x, y, direction = enemy
            dx, dy = direction
            
            # 尝试移动
            nx, ny = x + dx * 0.05, y + dy * 0.05  # 敌人移动速度
            
            # 检查是否可以移动到新位置
            if (0 < int(nx) < self.width - 1 and 0 < int(ny) < self.height - 1 and 
                self.map[int(ny)][int(nx)] == 0):
                # 检查是否有炸弹
                has_bomb = False
                for bomb in self.bombs:
                    if bomb[0] == int(nx) and bomb[1] == int(ny):
                        has_bomb = True
                        break
                
                if not has_bomb:
                    enemy[0], enemy[1] = nx, ny
                else:
                    # 改变方向
                    enemy[2] = random.choice([(1,0), (0,1), (-1,0), (0,-1)])
            else:
                # 改变方向
                enemy[2] = random.choice([(1,0), (0,1), (-1,0), (0,-1)])
    
    def _check_win(self) -> bool:
        """检查是否获胜"""
        return len(self.enemies) == 0
    
    def update(self) -> None:
        """更新游戏状态"""
        if self.game_over or self.win:
            return
        
        # 更新炸弹计时器
        for i in range(len(self.bombs) - 1, -1, -1):
            self.bombs[i][2] -= 1
            if self.bombs[i][2] <= 0:
                self._explode_bomb(i)
        
        # 更新爆炸效果计时器
        for i in range(len(self.explosions) - 1, -1, -1):
            self.explosions[i][2] -= 1
            if self.explosions[i][2] <= 0:
                self.explosions.pop(i)
        
        # 移动敌人
        self._move_enemies()
        
        # 检查玩家是否收集道具
        self._collect_power_up()
        
        # 检查玩家碰撞
        if self._check_player_collision():
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                # 重置玩家位置
                self.player_pos = [1, 1]
        
        # 检查是否获胜
        if self._check_win():
            self.win = True
    
    def run(self):
        while not (self.game_over or self.win):
            self.screen.fill(BACKGROUND)
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
                    elif event.key == pygame.K_SPACE:
                        self._place_bomb()
            
            # 处理玩家移动
            keys = pygame.key.get_pressed()
            new_pos = self.player_pos.copy()
            current_time = pygame.time.get_ticks()
            move_delay = 50  # 快速移动时的延迟(毫秒)
            
            # 记录上次移动时间
            if not hasattr(self, 'last_move_time'):
                self.last_move_time = 0
            
            # 检查是否可以移动（基于时间间隔）
            can_move = current_time - self.last_move_time >= move_delay
            
            if can_move:
                if keys[pygame.K_UP]:
                    new_pos[1] -= 1
                    self.last_move_time = current_time
                elif keys[pygame.K_DOWN]:
                    new_pos[1] += 1
                    self.last_move_time = current_time
                elif keys[pygame.K_LEFT]:
                    new_pos[0] -= 1
                    self.last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    new_pos[0] += 1
                    self.last_move_time = current_time
            
            # 检查新位置是否有效
            if (0 <= new_pos[0] < self.width and 0 <= new_pos[1] < self.height and 
                self.map[new_pos[1]][new_pos[0]] == 0):
                # 检查是否有炸弹
                has_bomb = False
                for bomb in self.bombs:
                    if bomb[0] == new_pos[0] and bomb[1] == new_pos[1]:
                        has_bomb = True
                        break
                
                if not has_bomb:
                    self.player_pos = new_pos
            
            # 更新游戏状态
            self.update()
            
            # 绘制地图
            for y in range(self.height):
                for x in range(self.width):
                    if self.map[y][x] == 1:  # 固定墙
                        draw_block(self.screen, (128, 128, 128), (x, y), self.block_size)  # 深灰色
                    elif self.map[y][x] == 2:  # 可破坏墙
                        draw_block(self.screen, (139, 69, 19), (x, y), self.block_size)  # 深棕色
                    else:  # 空地
                        draw_block(self.screen, (50, 50, 50), (x, y), self.block_size)  # 浅灰色
            
            # 绘制道具
            for pos, power_type in self.power_ups.items():
                if power_type == "bomb":
                    draw_block(self.screen, RED, pos, self.block_size)
                elif power_type == "range":
                    draw_block(self.screen, BLUE, pos, self.block_size)
                elif power_type == "life":
                    draw_block(self.screen, GREEN, pos, self.block_size)
            
            # 绘制炸弹
            for bomb in self.bombs:
                draw_block(self.screen, (255, 69, 0), (bomb[0], bomb[1]), self.block_size)  # 橙红色
            
            # 绘制爆炸效果
            for explosion in self.explosions:
                draw_block(self.screen, YELLOW, (explosion[0], explosion[1]), self.block_size)
            
            # 绘制玩家
            draw_block(self.screen, (0, 191, 255), (self.player_pos[0], self.player_pos[1]), self.block_size)  # 深天蓝色
            
            # 绘制敌人
            for enemy in self.enemies:
                draw_block(self.screen, (255, 0, 0), (int(enemy[0]), int(enemy[1])), self.block_size)  # 纯红色
            
            # 显示得分和生命值
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)
            score_text = font.render(f'得分: {self.score}', True, WHITE)
            lives_text = font.render(f'生命: {self.lives}', True, WHITE)
            bomb_text = font.render(f'炸弹: {self.bomb_limit}', True, WHITE)
            range_text = font.render(f'范围: {self.bomb_range}', True, WHITE)
            
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (self.screen_width - 100, 10))
            self.screen.blit(bomb_text, (10, 40))
            self.screen.blit(range_text, (self.screen_width - 100, 40))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # 游戏结束处理
        while True:
            self.screen.fill(BACKGROUND)
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
            
            if self.win:
                text = font.render(f'恭喜获胜！得分: {self.score}', True, WHITE)
            else:
                text = font.render(f'游戏结束！得分: {self.score}', True, WHITE)
                
            restart_text = font.render('按 R 重新开始', True, WHITE)
            menu_text = font.render('按 ESC 返回菜单', True, WHITE)
            
            text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 60))
            restart_rect = restart_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            menu_rect = menu_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 60))
            
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_text, restart_rect)
            self.screen.blit(menu_text, menu_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.width, self.height, self.block_size)
                        self.run()
                        return
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return