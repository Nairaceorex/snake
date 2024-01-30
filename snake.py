import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
FPS = 10

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)

# Родительский класс для игровых объектов
class GameObject:
    def __init__(self, color):
        self.position = (0, 0)
        self.color = color

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH//GRID_SIZE)-1) * GRID_SIZE,
                         random.randint(0, (HEIGHT//GRID_SIZE)-1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# Класс змейки
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*GRID_SIZE)) % WIDTH), (cur[1] + (y*GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

    def decrease_length(self):
        if self.length > 1:
            self.length -= 1
            self.positions.pop()

# Класс еды
class Apple(GameObject):
    def __init__(self):
        super().__init__(WHITE)
        self.randomize_position()

# Класс камня
class Stone(GameObject):
    def __init__(self):
        super().__init__(GRAY)
        self.randomize_position()

# Класс банана
class Banana(GameObject):
    def __init__(self):
        super().__init__(YELLOW)
        self.randomize_position()

# Определение направлений
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Основная функция
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    apple = Apple()
    stone = Stone()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    snake.direction = RIGHT

        snake.update()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            stone.randomize_position()
        elif snake.get_head_position() == stone.position:
            snake.decrease_length()
            apple.randomize_position()
            stone.randomize_position()

        surface.fill(BLACK)
        snake.render(surface)
        apple.render(surface)
        stone.render(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
