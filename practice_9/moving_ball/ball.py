import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

radius = 25
x = WIDTH // 2
y = HEIGHT // 2
velocity = 5


clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] and y - velocity >= radius:
        y -= velocity
    if keys[pygame.K_DOWN] and y + velocity <= HEIGHT - radius:
        y += velocity
    if keys[pygame.K_LEFT] and x - velocity >= radius:
        x -= velocity
    if keys[pygame.K_RIGHT] and x + velocity <= WIDTH - radius:
        x += velocity

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (int(x), int(y)), radius)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()