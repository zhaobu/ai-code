import pygame
import sys
import random

class FlappyBirdGame:
    def run(self):
        pygame.init()
        
        # 窗口设置
        WIDTH, HEIGHT = 400, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        clock = pygame.time.Clock()
        
        # 小鸟参数
        bird_x = 50
        bird_y = 200
        bird_velocity = 0
        gravity = 0.3
        jump_strength = -6
        
        # 管道参数
        # 管道参数优化
        pipe_gap = 250
        pipe_velocity = -2
        pipes = []
        SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(SPAWNPIPE, 1500)  # 缩短生成间隔到1.5秒
        
        # 小鸟物理参数
        gravity = 0.3
        jump_strength = -6
        
        # 初始化第一个管道（立即出现）
        pipes.append({
            'x': 400,
            'height': random.randint(100, 400)
        })
        
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 添加键盘和鼠标控制
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    bird_velocity = jump_strength
                if event.type == SPAWNPIPE:
                    pipe_height = HEIGHT//2 + random.randint(-100, 100)
                    pipes.append({
                        'x': WIDTH,
                        'height': pipe_height
                    })
            
            # 更新逻辑
            bird_velocity += gravity
            bird_y += bird_velocity
            
            # 移动管道
            removed_pipes = []
            for pipe in pipes:
                pipe['x'] += pipe_velocity
                if pipe['x'] < -50:
                    removed_pipes.append(pipe)
            
            # 移除超出屏幕的管道
            for r in removed_pipes:
                pipes.remove(r)
            
            # 碰撞检测
            for pipe in pipes:
                if (bird_x + 20 > pipe['x'] and 
                    bird_x < pipe['x'] + 30 and 
                    (bird_y - 20 < pipe['height'] or 
                     bird_y + 20 > pipe['height'] + pipe_gap)):
                    game_over = True
            
            # 绘制
            screen.fill((135,206,250))  # 天空蓝色
            # 绘制小鸟
            pygame.draw.circle(screen, (255, 255, 0), (bird_x, int(bird_y)), 20)
            # 绘制地面
            pygame.draw.rect(screen, (0, 128, 0), (0, HEIGHT-50, WIDTH, 50))
            
            # 绘制管道
            for pipe in pipes:
                # 上管道
                pygame.draw.rect(screen, (0, 255, 0), (pipe['x'], 0, 30, pipe['height']))
                # 下管道
                pygame.draw.rect(screen, (0, 255, 0), (pipe['x'], pipe['height']+pipe_gap, 30, HEIGHT - pipe['height'] - pipe_gap))
            
            pygame.display.update()
            clock.tick(30)
