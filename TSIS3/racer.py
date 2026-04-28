import pygame
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        try:
            self.image = pygame.image.load("TSIS3/assets/Player.png").convert_alpha()
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(self.speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        try:
            self.image = pygame.image.load("TSIS3/assets/Enemy.png").convert_alpha()
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.spawn()

    def spawn(self):
        # Безопасный спавн вне зоны видимости
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# НОВЫЙ КЛАСС: Препятствия на дороге
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Выбор типа препятствия: масляное пятно или барьер
        self.type = random.choice(["oil", "barrier"])
        
        if self.type == "oil":
            # Масляное пятно
            try:
                self.image = pygame.image.load("TSIS3/assets/oil.png").convert_alpha()
            except:
                self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
                pygame.draw.ellipse(self.image, (50, 50, 50, 180), self.image.get_rect())
        else:
            # Дорожный барьер
            try:
                self.image = pygame.image.load("TSIS3/assets/barrier.png").convert_alpha()
            except:
                self.image = pygame.Surface((60, 20))
                self.image.fill((200, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH-50), -100)

    def update(self, speed):
        # Препятствия движутся вместе с дорогой
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, p_type):
        super().__init__()
        self.type = p_type # Nitro, Shield, Repair
        try:
            self.image = pygame.image.load(f"TSIS3/assets/{p_type.lower()}.png").convert_alpha()
        except:
            self.image = pygame.Surface((10, 10))
            colors = {"Nitro": (255, 165, 0), "Shield": (0, 0, 255), "Repair": (0, 255, 0)}
            self.image.fill(colors.get(p_type, (255, 255, 255)))
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -50)
        self.created_at = pygame.time.get_ticks()

    def update(self, speed):
        self.rect.move_ip(0, speed)
        # Удаление по таймауту 5 секунд
        if pygame.time.get_ticks() - self.created_at > 5000 or self.rect.top > SCREEN_HEIGHT:
            self.kill()