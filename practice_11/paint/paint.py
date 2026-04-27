import pygame
import sys
import math


pygame.init()


WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")


WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200, 200)


canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)


current_color = BLACK
current_tool = "square"
drawing = False
start_pos = (0,0)


font = pygame.font.SysFont("Arial", 12)


tools = ["square", "right_tri", "eq_tri", "rhombus", "eraser"]
tool_rects = []

for i, tool in enumerate(tools):
    rect = pygame.Rect(10 + i * 110, 10, 100, 30)
    tool_rects.append((rect, tool))

def draw_ui():
    """Draws the top control bar"""
    pygame.draw.rect(screen, GRAY, (0,0, WIDTH, 50))
    for rect, tool in tool_rects:
        color = (150,150,150) if current_tool == tool else (180,180,180)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        text = font.render(tool.replace('_', ' ').capitalize(), True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 8))

def get_shapes_points(tool, start, end):
    """Calculates coordinates of points for different shapes based on mouse movement"""
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    if tool == "square":
        side = max(abs(dx), abs(dy))
        s_x = x1 if x2 > x1 else x1 - side
        s_y = y1 if y2 > y1 else y1 - side
        return [pygame.Rect(s_x, s_y, side, side)]

    elif tool == "right_tri":
        return [(x1, y1), (x1, y2), (x2, y2)]

    elif tool == "eq_tri":
        side = math.sqrt(dx**2 + dy**2)
        height = (math.sqrt(3) / 2) * side
        angle = math.atan2(dy, dx)
        
        p2 = (x1 + side * math.cos(angle), y1 + side * math.sin(angle))
        p3 = (x1 + side * math.cos(angle - math.pi/3), y1 + side * math.sin(angle - math.pi/3))
        return [(x1, y1), p2, p3]

    elif tool == "rhombus":
        return [(x1 + dx//2, y1), (x2, y1 + dy//2), (x1 + dx//2, y2), (x1, y1 + dy//2)]
    
    return []

while True:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_pos[1] > 50:
                drawing = True
                start_pos = mouse_pos
            else:
                for rect, tool in tool_rects:
                    if rect.collidepoint(mouse_pos):
                        current_tool = tool

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                points = get_shapes_points(current_tool, start_pos, mouse_pos)
                if current_tool == "square":
                    pygame.draw.rect(canvas, current_color, points[0], 2)
                elif current_tool == "eraser":
                    pass
                else:
                    pygame.draw.polygon(canvas, current_color, points, 2)
                drawing = False

    if drawing:
        if current_tool == "eraser":
            pygame.draw.circle(canvas, WHITE, mouse_pos, 20)
        else:
            points = get_shapes_points(current_tool, start_pos, mouse_pos)
            if current_tool == "square":
                pygame.draw.rect(screen, current_color, points[0], 2)
            else:
                pygame.draw.polygon(screen, current_color, points, 2)

    draw_ui()
    pygame.display.flip()