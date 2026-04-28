import pygame
import sys
from racer import Player, Enemy, PowerUp, Obstacle
from ui import UI
from persistence import load_settings, save_score, save_settings

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        pygame.display.set_caption("Racer")
        
        self.ui = UI(self.screen)
        self.settings = load_settings()
        self.clock = pygame.time.Clock()
        
        self.state = "MENU"
        self.username = "Player1"
        self.reset_game_data()

    def reset_game_data(self):
        """Инициализация объектов перед стартом игры"""
        # Начальная скорость зависит от сложности (1, 2 или 3)
        self.step_speed = 3 + (self.settings.get('difficulty', 1) * 2)
        self.score = 0
        self.distance = 0.0
        
        self.player = Player((255, 0, 0))
        self.enemies = pygame.sprite.Group([Enemy(self.step_speed)])
        self.powerups = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group([self.player])

        self.active_powerup = None
        self.powerup_timer = 0
        self.shield_active = False

    def game_logic(self):
        """Весь игровой процесс здесь"""
        self.distance += 0.1
        self.player.move()
        self.enemies.update()
        self.obstacles.update(self.step_speed)
        self.powerups.update(self.step_speed)

        # Спавн бонусов и препятствий
        import random
        if random.randint(1, 150) == 1:
            self.powerups.add(PowerUp(random.choice(["Nitro", "Shield", "Repair"])))
        if random.randint(1, 200) == 1:
            self.obstacles.add(Obstacle())

        # Проверка бонусов
        p_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for hit in p_hits:
            if hit.type == "Repair": self.score += 100
            elif hit.type == "Shield": self.shield_active = True
            elif hit.type == "Nitro":
                self.active_powerup = "Nitro"
                self.player.speed = 10
                self.powerup_timer = pygame.time.get_ticks() + 4000

        # Сброс Nitro по времени
        if self.active_powerup == "Nitro" and pygame.time.get_ticks() > self.powerup_timer:
            self.active_powerup = None
            self.player.speed = 5

        # Проверка столкновений
        if pygame.sprite.spritecollide(self.player, self.enemies, False) or \
           pygame.sprite.spritecollide(self.player, self.obstacles, False):
            if self.shield_active:
                self.shield_active = False
                for e in self.enemies: e.spawn()
                for o in self.obstacles: o.kill()
            else:
                save_score(self.username, self.score, self.distance)
                self.state = "OVER"

    def run(self):
        while True:
            # 1. Получаем события (передаем их в UI для кнопок)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            # 2. Отрисовка и логика по состояниям
            if self.state == "MENU":
                self.screen.fill((255, 255, 255))
                # Если нажата кнопка Play — сбрасываем данные и в бой
                if self.ui.draw_button("START GAME", 100, 250, 200, 50, events):
                    self.reset_game_data()
                    self.state = "GAME"
                if self.ui.draw_button("SETTINGS", 100, 320, 200, 50, events):
                    self.state = "SETTINGS"

            elif self.state == "SETTINGS":
                actions = self.ui.settings_screen(self.settings['difficulty'], events)
                if actions['change_diff']:
                    self.settings['difficulty'] = (self.settings['difficulty'] % 3) + 1
                    save_settings(self.settings)
                if actions['back']:
                    self.state = "MENU"

            elif self.state == "GAME":
                self.game_logic()
                
                self.screen.fill((100, 100, 100))
                self.all_sprites.draw(self.screen)
                self.enemies.draw(self.screen)
                self.obstacles.draw(self.screen)
                self.powerups.draw(self.screen)
                
                self.ui.draw_text(f"Score: {self.score}", self.ui.font, 10, 10)
                self.ui.draw_text(f"Dist: {int(self.distance)}m", self.ui.font, 10, 35)
                if self.shield_active:
                    self.ui.draw_text("SHIELD ON", self.ui.font, 280, 10, (0, 0, 255))

            elif self.state == "OVER":
                actions = self.ui.game_over_screen(self.score, self.distance, events)
                if actions['retry']: 
                    self.reset_game_data()
                    self.state = "GAME"
                if actions['menu']: self.state = "MENU"

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()