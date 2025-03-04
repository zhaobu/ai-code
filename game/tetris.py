import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define the dimensions of each block
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Calculate the width and height of the grid
SCREEN_WIDTH = BLOCK_SIZE * GRID_WIDTH
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Define the shapes of the tetriminos
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 1, 0]]   # T
]

# Define the colors of the tetriminos
SHAPE_COLORS = [
    (0, 255, 255),  # I
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (255, 0, 0),    # Z
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (128, 0, 128)   # T
]

class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = SHAPE_COLORS[SHAPES.index(self.shape)]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        rotated_shape = []
        for x in range(len(self.shape[0])):
            new_row = []
            for y in range(len(self.shape) - 1, -1, -1):
                new_row.append(self.shape[y][x])
            rotated_shape.append(new_row)
        self.shape = rotated_shape

    def draw(self, screen):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, (
                        (self.x + x) * BLOCK_SIZE,
                        (self.y + y) * BLOCK_SIZE,
                        BLOCK_SIZE, BLOCK_SIZE
                    ))

class GameGrid:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    def is_inside(self, x, y, shape):
        for row_index, row in enumerate(shape):
            for col_index, cell in enumerate(row):
                if cell:
                    grid_x = x + col_index
                    grid_y = y + row_index

                    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
                        return False
                    if grid_y >= 0 and self.grid[grid_y][grid_x]:
                        return False
        return True

    def place_tetrimino(self, tetrimino):
        for y, row in enumerate(tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[tetrimino.y + y][tetrimino.x + x] = tetrimino.color

    def clear_lines(self):
        lines_cleared = 0
        row_index = GRID_HEIGHT - 1
        while row_index >= 0:
            if all(self.grid[row_index]):
                del self.grid[row_index]
                self.grid.insert(0, [0] * GRID_WIDTH)
                lines_cleared += 1
            else:
                row_index -= 1
        return lines_cleared

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (
                        x * BLOCK_SIZE,
                        y * BLOCK_SIZE,
                        BLOCK_SIZE, BLOCK_SIZE
                    ))
                else:
                    pygame.draw.rect(screen, GRAY, (
                        x * BLOCK_SIZE,
                        y * BLOCK_SIZE,
                        BLOCK_SIZE, BLOCK_SIZE
                    ), 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    grid = GameGrid()
    tetrimino = Tetrimino()
    drop_timer = 0
    drop_speed = 60  # Lower value = faster drop
    fast_drop_speed = 5
    score = 0
    level = 1
    lines = 0
    font = pygame.font.Font(None, 36)

    while True:
        game_over = False
        grid = GameGrid()
        tetrimino = Tetrimino()
        drop_timer = 0
        drop_speed = 60
        fast_drop_speed = 5
        score = 0
        level = 1
        lines = 0

        while not game_over:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if grid.is_inside(tetrimino.x - 1, tetrimino.y, tetrimino.shape):
                            tetrimino.x -= 1
                    if event.key == pygame.K_RIGHT:
                        if grid.is_inside(tetrimino.x + 1, tetrimino.y, tetrimino.shape):
                            tetrimino.x += 1
                    if event.key == pygame.K_DOWN:
                        drop_speed = fast_drop_speed
                    if event.key == pygame.K_UP:
                        rotated_shape = []
                        for x in range(len(tetrimino.shape[0])):
                            new_row = []
                            for y in range(len(tetrimino.shape) - 1, -1, -1):
                                new_row.append(tetrimino.shape[y][x])
                            rotated_shape.append(new_row)
                        if grid.is_inside(tetrimino.x, tetrimino.y, rotated_shape):
                            tetrimino.shape = rotated_shape
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        drop_speed = 60

            # Game logic
            drop_timer += 1
            if drop_timer > drop_speed:
                drop_timer = 0
                if grid.is_inside(tetrimino.x, tetrimino.y + 1, tetrimino.shape):
                    tetrimino.y += 1
                else:
                    grid.place_tetrimino(tetrimino)
                    cleared_lines = grid.clear_lines()
                    if cleared_lines > 0:
                        lines += cleared_lines
                        score += 100 * cleared_lines * level
                        if lines >= level * 10:
                            level += 1
                            drop_speed = max(1, drop_speed - 5)
                    tetrimino = Tetrimino()
                    if not grid.is_inside(tetrimino.x, tetrimino.y, tetrimino.shape):
                        game_over = True

            # Drawing
            screen.fill(BLACK)
            grid.draw(screen)
            tetrimino.draw(screen)

            # Display score and level
            score_text = font.render(f"Score: {score}", True, WHITE)
            level_text = font.render(f"Level: {level}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))

            pygame.display.flip()

            clock.tick(60)

if __name__ == "__main__":
    main()
