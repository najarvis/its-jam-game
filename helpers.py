import pygame

def adjust_brightness_rgb(r: int, g: int, b: int, t: float) -> tuple[int, int, int]:
    return tuple(map(lambda x : int(min(max(x, 0), 255)), pygame.Vector3(r, g, b) * t))

def bottom_edge_rect(rect: pygame.rect.FRect) -> pygame.rect.FRect:
    return pygame.rect.FRect(rect.left, rect.bottom, rect.width, 1)

def bottom_edge_line(rect: pygame.rect.FRect) -> tuple[pygame.Vector2, pygame.Vector2]:
    return pygame.Vector2(rect.bottomleft), pygame.Vector2(rect.bottomright)
