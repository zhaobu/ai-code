import pygame
import random
from pygame.sprite import Sprite, Group

# 游戏常量
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Spaceship(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-50))
        self.speed = 5
        self.health = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Enemy(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(
            center=(random.randint(50, WIDTH-50), -50)
        )
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > HEIGHT:
            self.kill()

class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class SpaceshieldGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.spaceship = Spaceship()
        self.spaceship_group = pygame.sprite.Group(self.spaceship)
        self.enemies = Group()
        self.bullets = Group()
        self.wave = 1
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 1500 // self.wave
        self.score = 0
        # 解决中文乱码：指定支持中文的字体
        font_path = pygame.font.match_font(['msyh', 'simhei', 'arial'])
        self.font = pygame.font.Font(font_path, 36)
        self.paused = False
        self.game_over = False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bullets.add(Bullet(self.spaceship.rect.centerx, self.spaceship.rect.top))
                    elif event.key == pygame.K_ESCAPE:
                        self.paused = True

            # 暂停处理
            while self.paused and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        self.paused = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            self.paused = False
                        elif event.key == pygame.K_m:
                            running = False
                            self.paused = False

                self.screen.fill((0,0,0))
                self.draw_pause_menu()
                pygame.display.flip()

            # 游戏结束处理
            while self.game_over and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running = False
                        elif event.key == pygame.K_r:
                            self.reset_game()  # 修复按键响应

                self.screen.fill((0,0,0))
                self.draw_game_over()
                pygame.display.flip()

            if not self.game_over:
                # 正常游戏逻辑
                self.enemy_spawn_timer += self.clock.get_time()
                if self.enemy_spawn_timer >= self.enemy_spawn_interval:
                    for _ in range(self.wave):
                        self.enemies.add(Enemy())
                    self.enemy_spawn_timer = 0

                self.spaceship.update()
                self.enemies.update()
                self.bullets.update()

                # 碰撞检测
                bullet_collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
                self.score += len(bullet_collisions) * 10

                ship_collisions = pygame.sprite.spritecollide(self.spaceship, self.enemies, True)
                if ship_collisions:
                    self.spaceship.health -= 1
                    if self.spaceship.health <= 0:
                        self.game_over = True

                # 绘制游戏内容
                self.screen.fill((0,0,0))
                self.spaceship_group.draw(self.screen)
                self.enemies.draw(self.screen)
                self.bullets.draw(self.screen)
                self.draw_ui()

            pygame.display.flip()
            self.clock.tick(60)

    def draw_pause_menu(self):
        pause_text = self.font.render("游戏暂停", True, WHITE)
        self.screen.blit(pause_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
        options_text = self.font.render("按C继续，按M退出", True, WHITE)
        self.screen.blit(options_text, (WIDTH//2 - 100, HEIGHT//2))

    def draw_game_over(self):
        game_over_text = self.font.render("游戏结束", True, RED)
        score_text = self.font.render(f"最终得分: {self.score}", True, WHITE)
        self.screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
        self.screen.blit(score_text, (WIDTH//2 - 100, HEIGHT//2))
        options_text = self.font.render("按R重新开始，按Q退出", True, WHITE)
        self.screen.blit(options_text, (WIDTH//2 - 120, HEIGHT//2 + 50))

    def draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        health_text = self.font.render(f"Health: {self.spaceship.health}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(health_text, (10, 50))

    def reset_game(self):
        self.spaceship.health = 3
        self.score = 0
        self.wave = 1
        self.enemy_spawn_interval = 1500 // self.wave
        self.enemies.empty()
        self.bullets.empty()
        self.game_over = False  # 确保重置游戏状态

if __name__ == "__main__":
    game = SpaceshieldGame()
    game.run()
