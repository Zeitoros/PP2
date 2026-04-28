import pygame
import datetime
from tools import flood_fill, draw_rhombus, draw_right_triangle, draw_circle

pygame.init()
WIDTH, HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((255, 255, 255))

current_tool = 'pencil'
current_color = (0, 0, 0)
brush_size = 2
drawing = False
start_pos = None

# Текстовый буфер
text_active = False
text_content = ""
text_pos = None
font = pygame.font.SysFont("Arial", 24)

running = True
while running:
    SCREEN.blit(base_layer, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # СМЕНА ИНСТРУМЕНТОВ (ГОРЯЧИЕ КЛАВИШИ)
            if event.key == pygame.K_p: current_tool = 'pencil'
            if event.key == pygame.K_e: current_tool = 'eraser'
            if event.key == pygame.K_l: current_tool = 'line'
            if event.key == pygame.K_r: current_tool = 'rect'
            if event.key == pygame.K_c: current_tool = 'circle'
            if event.key == pygame.K_f: current_tool = 'fill'
            if event.key == pygame.K_t: current_tool = 'text'
            if event.key == pygame.K_h: current_tool = 'rhombus'
            if event.key == pygame.K_g: current_tool = 'right_triangle'

            # СМЕНА РАЗМЕРА КИСТИ
            if event.key == pygame.K_1: brush_size = 2
            if event.key == pygame.K_2: brush_size = 5
            if event.key == pygame.K_3: brush_size = 10

            # Текстовый ввод
            if text_active:
                if event.key == pygame.K_RETURN:
                    img = font.render(text_content, True, current_color)
                    base_layer.blit(img, text_pos)
                    text_active = False
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text_content = text_content[:-1]
                else:
                    text_content += event.unicode

            # Сохранение Ctrl+S
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                filename = f"save_{datetime.datetime.now().strftime('%H%M%S')}.png"
                pygame.image.save(base_layer, filename)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_tool == 'fill':
                flood_fill(base_layer, *event.pos, current_color)
            elif current_tool == 'text':
                text_active = True
                text_pos = event.pos
                text_content = ""
            else:
                drawing = True
                start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                # Фиксация фигур на слое
                if current_tool == 'line':
                    pygame.draw.line(base_layer, current_color, start_pos, mouse_pos, brush_size)
                elif current_tool == 'rect':
                    rect = pygame.Rect(start_pos, (mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
                    pygame.draw.rect(base_layer, current_color, rect, brush_size)
                elif current_tool == 'rhombus':
                    draw_rhombus(base_layer, current_color, start_pos, mouse_pos, brush_size)
                elif current_tool == 'circle':
                    draw_circle(base_layer, current_color, start_pos, mouse_pos, brush_size)
                elif current_tool == 'right_triangle':
                    draw_right_triangle(base_layer, current_color, start_pos, mouse_pos, brush_size)
                drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == 'pencil':
                pygame.draw.line(base_layer, current_color, start_pos, mouse_pos, brush_size)
                start_pos = mouse_pos
            elif current_tool == 'eraser':
                pygame.draw.line(base_layer, (255,255,255), start_pos, mouse_pos, 30)
                start_pos = mouse_pos

    if drawing:
        if current_tool == 'line':
            pygame.draw.line(SCREEN, current_color, start_pos, mouse_pos, brush_size)
        elif current_tool == 'rect':
            rect = pygame.Rect(start_pos, (mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
            pygame.draw.rect(SCREEN, current_color, rect, brush_size)
        elif current_tool == 'circle':
            draw_circle(SCREEN, current_color, start_pos, mouse_pos, brush_size)
        elif current_tool == 'right_triangle':
            draw_right_triangle(SCREEN, current_color, start_pos, mouse_pos, brush_size)
        elif current_tool == 'rhombus':
            draw_rhombus(SCREEN, current_color, start_pos, mouse_pos, brush_size)

    # Отображение текста при наборе
    if text_active:
        txt = font.render(text_content + "|", True, current_color)
        SCREEN.blit(txt, text_pos)

    # Индикация выбранного инструмента
    info = font.render(f"Tool: {current_tool} | Size: {brush_size}", True, (50, 50, 50))
    SCREEN.blit(info, (10, 10))

    controls = font.render("Controls: 1.pencil(p) | 2.line(l) | 3.rect(r) | 4.circle(c) | 5.fill(f) | 6.text(t) | 7.rhombus(h) | 8.right triangle(g) | 9.eraser(e)", True, (80,80,80))
    SCREEN.blit(controls, (10,50))

    pygame.display.flip()
pygame.quit()