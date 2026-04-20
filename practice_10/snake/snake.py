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
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game: Levels")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 50)

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = pygame.K_RIGHT
        self.new_block = False

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == pygame.K_RIGHT: head_x += BLOCK_SIZE
        elif self.direction == pygame.K_LEFT: head_x -= BLOCK_SIZE
        elif self.direction == pygame.K_UP: head_y -= BLOCK_SIZE
        elif self.direction == pygame.K_DOWN: head_y += BLOCK_SIZE

        new_head = (head_x, head_y)
        self.body.insert(0, new_head)
        
        if not self.new_block:
            self.body.pop()
        else:
            self.new_block = False

    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def generate_random_pos(self, snake_body):
        while True:
            x = random.randrange(0, WIDTH, BLOCK_SIZE)
            y = random.randrange(0, HEIGHT, BLOCK_SIZE)
            pos = (x, y)
            if pos not in snake_body:
                return pos

    def draw(self):
        rect = pygame.Rect(self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, RED, rect)

def main():
    snake = Snake()
    food = Food(snake.body)
    
    score = 0
    level = 1
    current_fps = FPS
    foods_to_next_level = 3

    running = True
    while running:
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

        if snake.body[0] == food.position:
            snake.new_block = True
            score += 1
            food = Food(snake.body)
            

            if score % foods_to_next_level == 0:
                level += 1
                current_fps += 2

        if snake.check_collision():
            screen.fill(RED)
            msg = font_large.render("GAME OVER", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.delay(2000)
            main()

        for i, block in enumerate(snake.body):
            color = GREEN if i == 0 else BLUE
            pygame.draw.rect(screen, color, (block[0], block[1], BLOCK_SIZE - 2, BLOCK_SIZE - 2))

        food.draw()

        score_text = font_small.render(f"Score: {score}", True, WHITE)
        level_text = font_small.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (WIDTH - 100, 10))

        pygame.display.update()
        clock.tick(current_fps)

if __name__ == "__main__":
    main()