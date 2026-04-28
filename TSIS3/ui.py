import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Verdana", 20)
        self.big_font = pygame.font.SysFont("Verdana", 40)

    def draw_button(self, text, x, y, width, height, event_list):
        """Отрисовка кнопки и проверка клика через список событий"""
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, width, height)
        
        color = (170, 170, 170) if rect.collidepoint(mouse) else (200, 200, 200)
        
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        
        text_surf = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        # Проверка клика
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect.collidepoint(event.pos):
                    return True
        return False

    def menu_screen(self):
        """Главное меню: Play, Leaderboard, Settings, Quit"""
        self.screen.fill(WHITE)
        title = self.big_font.render("RACER", True, BLACK)
        self.screen.blit(title, (130, 100))
        
        play = self.draw_button("Play", 100, 250, 200, 50)
        lb = self.draw_button("Leaderboard", 100, 320, 200, 50)
        sett = self.draw_button("Settings", 100, 390, 200, 50)
        quit_btn = self.draw_button("Quit", 100, 460, 200, 50)
        
        return {"play": play, "leaderboard": lb, "settings": sett, "quit": quit_btn}

    def settings_screen(self, current_diff, event_list):
        """Экран настроек с выбором сложности"""
        self.screen.fill((255, 255, 255))
        img = self.big_font.render("SETTINGS", True, (0, 0, 0))
        self.screen.blit(img, (100, 50))

        # Кнопка переключения сложности (циклично 1 -> 2 -> 3 -> 1)
        diff_btn = self.draw_button(f"Difficulty: {current_diff}", 100, 200, 200, 50, event_list)
        back_btn = self.draw_button("Back", 100, 400, 200, 50, event_list)
        
        return {"change_diff": diff_btn, "back": back_btn}

    def game_over_screen(self, score, distance, event_list):
        """Экран Game Over с кнопками"""
        self.screen.fill((0, 0, 0))

        # Текст проигрыша
        title = self.big_font.render("CRASHED!", True, (255, 0, 0))
        self.screen.blit(title, (90, 150))

        # Статистика
        self.draw_text(f"Final Score: {score}", self.font, 120, 250, (255, 255, 255))
        self.draw_text(f"Distance: {int(distance)}m", self.font, 120, 280, (255, 255, 255))

        # Кнопки взаимодействия
        retry_btn = self.draw_button("RETRY", 100, 400, 200, 50, event_list)
        menu_btn = self.draw_button("MAIN MENU", 100, 470, 200, 50, event_list)

        return {"retry": retry_btn, "menu": menu_btn}

    def draw_text(self, text, font, x, y, color=BLACK):
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def input_name_screen(self, current_name):
        """Экран ввода имени перед началом игры"""
        self.screen.fill(WHITE)
        self.draw_text("Enter your name:", self.font, 120, 200)
        self.draw_text(current_name + "_", self.font, 150, 250, BLUE)
        self.draw_text("Press ENTER to Start", self.font, 100, 350)