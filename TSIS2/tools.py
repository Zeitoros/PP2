import pygame
import math

def flood_fill(surface, x, y, new_color):
    """Инструмент заливки (Flood-fill)"""
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    
    # Используем стек для обхода пикселей
    width, height = surface.get_size()
    pixels = [(x, y)]
    while pixels:
        cx, cy = pixels.pop()
        if surface.get_at((cx, cy)) == target_color:
            surface.set_at((cx, cy), new_color)
            if cx > 0: pixels.append((cx - 1, cy))
            if cx < width - 1: pixels.append((cx + 1, cy))
            if cy > 0: pixels.append((cx, cy - 1))
            if cy < height - 1: pixels.append((cx, cy + 1))

def draw_rhombus(surface, color, start_pos, end_pos, width):
    """Рисование ромба"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    points = [
        (x1 + (x2 - x1) // 2, y1),
        (x2, y1 + (y2 - y1) // 2),
        (x1 + (x2 - x1) // 2, y2),
        (x1, y1 + (y2 - y1) // 2)
    ]
    pygame.draw.polygon(surface, color, points, width)

def draw_right_triangle(surface, color, start_pos, end_pos, width):
    """Прямоугольный треугольник"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, width)

def draw_circle(surface, color, start_pos, end_pos, width):
    """Рисование круга по двум точкам (центр и радиус)"""
    radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
    if radius > 0:
        pygame.draw.circle(surface, color, start_pos, radius, width)