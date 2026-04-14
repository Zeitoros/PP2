import pygame
import os

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont("Arial", 24)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, "music")


if os.path.exists(MUSIC_DIR):
    songs = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav'))]
else:
    songs = []

current_idx = 0
playing = False

def play_song():
    if songs:
        pygame.mixer.music.load(os.path.join(MUSIC_DIR, songs[current_idx]))
        pygame.mixer.music.play()
        return True
    return False

running = True
while running:
    screen.fill((30, 30, 30))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not playing:
                    if play_song(): playing = True
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_s:
                pygame.mixer.music.pause()
            elif event.key == pygame.K_n:
                if songs:
                    current_idx = (current_idx + 1) % len(songs)
                    play_song()
            elif event.key == pygame.K_b:
                if songs:
                    current_idx = (current_idx - 1) % len(songs)
                    play_song()

    if not songs:
        text = font.render("No music files found in 'music/' folder!", True, (255, 100, 100))
    else:
        text = font.render(f"Track: {songs[current_idx]}", True, (255, 255, 255))
    
    screen.blit(text, (50, 150))
    instr = font.render("P: Play | S: Stop | N: Next | B: Back", True, (150, 150, 150))
    screen.blit(instr, (50, 330))
    
    pygame.display.flip()

pygame.quit()