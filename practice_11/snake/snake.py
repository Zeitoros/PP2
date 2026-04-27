import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20
FPS = 10


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Verdana", 20)

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = pygame.K_RIGHT
        self.new_blocks = 0 # Сколько блоков нужно добавить (для разного веса)

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == pygame.K_RIGHT: head_x += BLOCK_SIZE
        elif self.direction == pygame.K_LEFT: head_x -= BLOCK_SIZE
        elif self.direction == pygame.K_UP: head_y -= BLOCK_SIZE
        elif self.direction == pygame.K_DOWN: head_y += BLOCK_SIZE

        new_head = (head_x, head_y)
        self.body.insert(0, new_head)
        
        # Если в запасе есть блоки (от съеденной еды), не удаляем хвост
        if self.new_blocks > 0:
            self.new_blocks -= 1
        else:
            self.body.pop()

    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self, snake_body):
        self.spawn(snake_body)

    def spawn(self, snake_body):
        # Генерируем случайную позицию, не занятую змейкой
        while True:
            self.x = random.randrange(0, WIDTH, BLOCK_SIZE)
            self.y = random.randrange(0, HEIGHT, BLOCK_SIZE)
            if (self.x, self.y) not in snake_body:
                break
        
        # Рандомный вес: 70% обычная (1 блок), 30% золотая (3 блока)
        if random.random() < 0.7:
            self.weight = 1
            self.color = RED
            self.timer = 100 # Обычная еда живет дольше
        else:
            self.weight = 3
            self.color = GOLD
            self.timer = 50  # Золотая еда исчезает быстро (50 кадров)

    def update(self, snake_body):
        # Уменьшаем таймер. Если он вышел — спавним новую еду
        self.timer -= 1
        if self.timer <= 0:
            self.spawn(snake_body)

    def draw(self):
        rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        
        # Визуальный индикатор таймера (тонкая полоска сверху еды)
        timer_width = (self.timer / 100) * BLOCK_SIZE if self.weight == 1 else (self.timer / 50) * BLOCK_SIZE
        pygame.draw.rect(screen, WHITE, (self.x, self.y - 4, timer_width, 2))

def main():
    snake = Snake()
    food = Food(snake.body)
    
    score = 0
    level = 1
    current_fps = FPS

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != pygame.K_DOWN:
                    snake.direction = pygame.K_UP
                elif event.key == pygame.K_DOWN and snake.direction != pygame.K_UP:
                    snake.direction = pygame.K_DOWN
                elif event.key == pygame.K_LEFT and snake.direction != pygame.K_RIGHT:
                    snake.direction = pygame.K_LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != pygame.K_LEFT:
                    snake.direction = pygame.K_RIGHT

        snake.move()

        # Проверка съедения
        if snake.body[0] == (food.x, food.y):
            score += food.weight
            snake.new_blocks += food.weight # Добавляем сегменты согласно весу
            
            # Повышение уровня за каждые 5 очков
            if score // 5 >= level:
                level += 1
                current_fps += 1
            
            food.spawn(snake.body)
        else:
            # Если еду не съели, обновляем её таймер жизни
            food.update(snake.body)

        if snake.check_collision():
            return # Выход в начало main (рестарт)

        # Отрисовка
        food.draw()
        for i, block in enumerate(snake.body):
            color = GREEN if i == 0 else BLUE
            pygame.draw.rect(screen, color, (block[0], block[1], BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Статистика
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        level_text = font_small.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (WIDTH - 100, 10))

        pygame.display.update()
        clock.tick(current_fps)

if __name__ == "__main__":
    while True:
        main()