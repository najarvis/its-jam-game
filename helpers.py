"""Helper functions that can be used in any file"""

import random
import pygame
import numpy as np
import numpy.typing as npt

def adjust_brightness_rgb(r: int, g: int, b: int, t: float) -> tuple[int, int, int]:
    return tuple(map(lambda x : int(min(max(x, 0), 255)), pygame.Vector3(r, g, b) * t))

def lerp_rgb(color_a: tuple[int, int, int], color_b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (
        pygame.math.lerp(color_a[0], color_b[0], t, True),
        pygame.math.lerp(color_a[1], color_b[1], t, True),
        pygame.math.lerp(color_a[2], color_b[2], t, True),
    )

def bottom_edge_rect(rect: pygame.rect.FRect) -> pygame.rect.FRect:
    return pygame.rect.FRect(rect.left, rect.bottom, rect.width, 1)

def bottom_edge_line(rect: pygame.rect.FRect) -> tuple[pygame.Vector2, pygame.Vector2]:
    return pygame.Vector2(rect.bottomleft), pygame.Vector2(rect.bottomright)

def random_hue(saturation: float, value: float) -> pygame.Color:
    return pygame.Color.from_hsva(random.uniform(0, 360), saturation, value, 100.0)

def random_bw() -> pygame.Color:
    c = random.randint(0, 1)
    return pygame.Color(c * 255, c * 255, c * 255, 255)

def random_gray() -> pygame.Color:
    c = random.randint(0, 255)
    return pygame.Color(c, c, c, 255)

def random_vector2(scale: float):
    return pygame.Vector2(random.uniform(-scale, scale), random.uniform(-scale, scale))

def scale_around_point(coordinates: list[pygame.Vector2], scale_factor: float, point: pygame.Vector2):
    coord_matrix = np.array(coordinates, dtype=np.float32)
    translate_matrix_1 = np.array([[-point.x + 1, -point.y], [-point.x, -point.y + 1]], dtype=np.float32)
    translate_matrix = np.array([[point.x + 1, point.y], [point.x, point.y + 1]], dtype=np.float32)

    scale_matrix = np.array([[scale_factor, 0], [0, scale_factor]], dtype=np.float32)
    return (translate_matrix @ scale_matrix @ translate_matrix_1 @ coord_matrix.T).T

def convert_cartesian_to_homogenous(coordinates: list[pygame.Vector2]) -> npt.NDArray:
    pass

def convert_homogenous_to_cargesian(coordinates: npt.NDArray) -> list[pygame.Vector2]:
    pass

if __name__ == "__main__":
    coord_a = pygame.Vector2(0, 5)
    coord_b = pygame.Vector2(3, -2)
    coord_c = pygame.Vector2(-3, -2)
    coords = [coord_a, coord_b, coord_c]
    print(scale_around_point(coords, 5, pygame.Vector2(0, 5)))