import pygame
import datetime
import os
import sys

pygame.init()
W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")

def load_image(name):
    path = os.path.join(IMG_DIR, name)
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error:
        print(f"Критическая ошибка: Не удалось загрузить {path}")
        pygame.quit()
        sys.exit()

main_clock = load_image("clock_without_hands.png")
hand_min_img = load_image("short_hand(1).png")
hand_sec_img = load_image("long_hand.png")

def rotate_hand(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=(W // 2, H // 2))
    return rotated_image, new_rect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    seconds = now.second
    minutes = now.minute

    sec_angle = -seconds * 6 + 90
    min_angle = -minutes * 6 + 90

    screen.fill((255, 255, 255))
    screen.blit(main_clock, (0, 0))

    surf_min, rect_min = rotate_hand(hand_min_img, min_angle)
    surf_sec, rect_sec = rotate_hand(hand_sec_img, sec_angle)

    screen.blit(surf_min, rect_min)
    screen.blit(surf_sec, rect_sec)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()