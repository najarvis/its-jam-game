import math
import pygame
import window

class Desktop:

    background_color = (5, 144, 186)

    def __init__(self, desktop_space: pygame.Rect):
        self.programs: list[Program] = []
        self.rect = desktop_space

        self.desktop_image = pygame.Surface(self.rect.size)

    def draw(self, surface: pygame.Surface, draw_rect: pygame.Rect):
        self.desktop_image.fill(Desktop.background_color)

        for program in self.programs:
            program.draw_icon(self.desktop_image)

        surface.blit(self.desktop_image, draw_rect)

class Program:
    """A program is something that is launchable and has an icon that lives on the desktop"""

    launch_time = 1
    launch_interval = 0.05

    def __init__(self, icon: pygame.Surface, position: pygame.Vector2 = pygame.Vector2(), name: str="Program", size: pygame.Vector2=(250, 300)):
        self.icon = icon
        self.position: pygame.Vector2 = position
        self.icon_rect = pygame.Rect(self.position, self.icon.size)

        self.selected = False
        self.opening = False
        self.open = False
        self.open_timer = 0

        self.window_size: pygame.Vector2 = size
        self.window_name = name
        self.window = window.Window(self.window_size, pygame.Vector2(100, 100), self.window_name)

        # When an icon is selected, shade the visible parts a blue color
        img_mask = pygame.mask.from_surface(self.icon)
        self.selected_overlay = img_mask.to_surface(setcolor=(0, 50, 200, 255), unsetcolor=(255, 255, 255, 255))

    def update(self, delta: float):
        if self.opening:
            self.open_timer += delta
            if self.open_timer > Program.launch_time:
                self.open = True
                self.opening = False

    def draw_icon(self, surface: pygame.Surface):
        surface.blit(self.icon, self.icon_rect)

        if self.selected:
            surface.blit(self.selected_overlay, self.icon_rect, special_flags=pygame.BLEND_MULT)

    def draw_window(self, surface: pygame.Surface):
        if self.opening:
            # animate a rect going from the program to the size of the window
            t = self.open_timer / Program.launch_time
            t = t - math.fmod(t, Program.launch_interval) # Limit it to make the animation more choppy
            rect_width = pygame.math.lerp(self.icon.width, self.window.size.x, t)
            rect_height = pygame.math.lerp(self.icon.height, self.window.size.y, t)
            rect_pos = self.position + (self.window.position - self.position) * t
            pygame.draw.rect(surface, (30, 30, 30), pygame.rect.FRect(rect_pos, (rect_width, rect_height)), 1)
        
        else:
            self.window.draw(surface)

    def launch_program(self):
        self.opening = True
        self.open_timer = 0

    def handle_input(self):
        if pygame.mouse.get_pressed()[0] and self.open:
            self.open = not self.window.check_close(pygame.mouse.get_pos())

    def close_program(self):
        self.open = False

class ChatSupport(Program):

    def __init__(self, icon: pygame.Surface):
        Program.__init__(self, icon, pygame.Vector2(20, 25), "Interconnect Chat", pygame.Vector2(250, 300))

