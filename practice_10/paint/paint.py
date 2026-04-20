import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

current_color = BLACK
current_tool = "brush"  # brush, rectangle, circle, eraser
drawing = False
start_pos = (0, 0)

colors = [BLACK, RED, GREEN, BLUE, YELLOW]
color_rects = []
for i, color in enumerate(colors):
    rect = pygame.Rect(10 + i * 40, 10, 30, 30)
    color_rects.append((rect, color))


tools = ["brush", "rect", "circle", "eraser"]
tool_rects = []
for i, tool in enumerate(tools):
    rect = pygame.Rect(250 + i * 80, 10, 70, 30)
    tool_rects.append((rect, tool))

def draw_ui():
    """Отрисовка панели управления"""
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, 50))
    
    for rect, color in color_rects:
        pygame.draw.rect(screen, color, rect)
        if current_color == color:
            pygame.draw.rect(screen, WHITE, rect, 2)

    font = pygame.font.SysFont("Arial", 14)
    for rect, tool in tool_rects:
        color = (100, 100, 100) if current_tool == tool else (150, 150, 150)
        pygame.draw.rect(screen, color, rect)
        text = font.render(tool.capitalize(), True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 5))


running = True
while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_pos[1] > 50:
                drawing = True
                start_pos = mouse_pos
            else:
                for rect, color in color_rects:
                    if rect.collidepoint(mouse_pos):
                        current_color = color
                        if current_tool == "eraser":
                            current_tool = "brush"
                
                for rect, tool in tool_rects:
                    if rect.collidepoint(mouse_pos):
                        current_tool = tool

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if current_tool == "rect":
                    rect_width = mouse_pos[0] - start_pos[0]
                    rect_height = mouse_pos[1] - start_pos[1]
                    pygame.draw.rect(canvas, current_color, (start_pos[0], start_pos[1], rect_width, rect_height), 2)
                elif current_tool == "circle":
                    radius = int(((mouse_pos[0]-start_pos[0])**2 + (mouse_pos[1]-start_pos[1])**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

                drawing = False

    if drawing:
        if current_tool == "brush":
            pygame.draw.circle(canvas, current_color, mouse_pos, 3)
        elif current_tool == "eraser":
            pygame.draw.circle(canvas, WHITE, mouse_pos, 20)
        elif current_tool == "rect":
            rect_width = mouse_pos[0] - start_pos[0]
            rect_height = mouse_pos[1] - start_pos[1]
            pygame.draw.rect(screen, current_color, (start_pos[0], start_pos[1], rect_width, rect_height), 2)
        elif current_tool == "circle":
            radius = int(((mouse_pos[0]-start_pos[0])**2 + (mouse_pos[1]-start_pos[1])**2)**0.5)
            pygame.draw.circle(screen, current_color, start_pos, radius, 2)

    draw_ui()
    pygame.display.flip()

pygame.quit()
sys.exit()