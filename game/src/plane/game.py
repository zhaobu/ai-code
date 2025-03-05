import pygame
import random
from typing import List, Tuple
from src.common.colors import *
from src.common.utils import draw_block

class PlaneGame:
    def __init__(self, width: int = 20, height: int = 25, block_size: int = 30):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen_width = width * block_size
        self.screen_height = height * block_size
        self.score = 0
        self.game_over = False
        self.lives = 3
        
        # 初始化玩家飞机
        self.plane_width = 3
        self.plane_height = 2
        self.plane_pos = [width // 2 - self.plane_width // 2, height - 3]
        self.plane_speed = 15
        self.moving_left = False
        self.moving_right = False
        
        # 初始化子弹
        self.bullets: List[List[float]] = []
        self.bullet_speed = 0.5
        self.last_shot = 0
        self.shoot_delay = 200  # 发射间隔(毫秒)
        
        # 初始化敌机
        self.enemies: List[List[float]] = []
        self.enemy_speed = 0.2
        self.last_enemy = 0
        self.enemy_delay = 1000  # 敌机生成间隔(毫秒)
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("飞机大战")
        self.clock = pygame.time.Clock()
    
    def _spawn_enemy(self) -> None:
        """生成新的敌机"""
        x = random.randint(0, self.width - 2)
        self.enemies.append([float(x), 0.0])
    
    def _check_collision(self, pos1: List[float], size1: List[int], pos2: List[float], size2: List[int]) -> bool:
        """检查两个矩形是否碰撞"""
        rect1 = pygame.Rect(int(pos1[0] * self.block_size),
                          int(pos1[1] * self.block_size),
                          size1[0] * self.block_size,
                          size1[1] * self.block_size)
        rect2 = pygame.Rect(int(pos2[0] * self.block_size),
                          int(pos2[1] * self.block_size),
                          size2[0] * self.block_size,
                          size2[1] * self.block_size)
        return rect1.colliderect(rect2)
    
    def update(self) -> None:
        """更新游戏状态"""
        current_time = pygame.time.get_ticks()
        
        # 更新玩家飞机位置
        if self.moving_left and self.plane_pos[0] > 0:
            self.plane_pos[0] -= self.plane_speed * 0.016
        if self.moving_right and self.plane_pos[0] < self.width - self.plane_width:
            self.plane_pos[0] += self.plane_speed * 0.016
        
        # 更新子弹位置
        for bullet in self.bullets[:]:
            bullet[1] -= self.bullet_speed
            if bullet[1] < 0:
                self.bullets.remove(bullet)
        
        # 更新敌机位置
        for enemy in self.enemies[:]:
            enemy[1] += self.enemy_speed
            if enemy[1] >= self.height:
                self.enemies.remove(enemy)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
        
        # 检查子弹与敌机的碰撞
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if self._check_collision(bullet, [1, 1], enemy, [2, 1]):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                        self.score += 10
        
        # 检查玩家与敌机的碰撞
        for enemy in self.enemies[:]:
            if self._check_collision(self.plane_pos, [self.plane_width, self.plane_height],
                                   enemy, [2, 1]):
                self.game_over = True
        
        # 生成新的敌机
        if current_time - self.last_enemy > self.enemy_delay:
            self._spawn_enemy()
            self.last_enemy = current_time
    
    def run(self):
        while not self.game_over:
            self.screen.fill(BACKGROUND)
            current_time = pygame.time.get_ticks()
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = True
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((600, 500))
                        pygame.display.set_caption("游戏合集")
                        return
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = False
            
            # 处理射击
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and current_time - self.last_shot > self.shoot_delay:
                self.bullets.append([self.plane_pos[0] + self.plane_width/2, self.plane_pos[1]])
                self.last_shot = current_time
            
            self.update()
            
            # 绘制玩家飞机
            for y in range(self.plane_height):
                for x in range(self.plane_width):
                    draw_block(self.screen, BLUE,
                              (self.plane_pos[0] + x, self.plane_pos[1] + y),
                              self.block_size)
            
            # 绘制子弹
            for bullet in self.bullets:
                draw_block(self.screen, RED,
                          (int(bullet[0]), int(bullet[1])),
                          self.block_size)
            
            # 绘制敌机
            for enemy in self.enemies:
                for x in range(2):
                    draw_block(self.screen, GREEN,
                              (enemy[0] + x, enemy[1]),
                              self.block_size)
            
            # 显示得分和生命值
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
            score_text = font.render(f'得分: {self.score}', True, WHITE)
            lives_text = font.render(f'生命: {self.lives}', True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (self.screen_width - 120, 10))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # 游戏结束处理
        while True:
            self.screen.fill(BACKGROUND)
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
            text = font.render(f'最终得分: {self.score}', True, WHITE)
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