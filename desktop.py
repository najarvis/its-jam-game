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

    def __init__(self, icon: pygame.Surface, position: pygame.Vector2 = pygame.Vector2(), name: str="Program"):
        self.icon = icon
        self.position = position
        self.icon_rect = pygame.Rect(self.position, self.icon.size)

        self.selected = False
        self.opening = False
        self.open = False

        self.window_size = (400, 400)
        self.window_name = name
        self.window = window.Window(self.window_size, pygame.Vector2(100, 100), self.window_name)

        # When an icon is selected, shade the visible parts a blue color
        img_mask = pygame.mask.from_surface(self.icon)
        self.selected_overlay = img_mask.to_surface(setcolor=(0, 50, 200, 255), unsetcolor=(255, 255, 255, 255))

    def draw_icon(self, surface: pygame.Surface):
        surface.blit(self.icon, self.icon_rect)

        if self.selected:
            surface.blit(self.selected_overlay, self.icon_rect, special_flags=pygame.BLEND_MULT)

    def draw_window(self, surface: pygame.Surface):
        self.window.draw(surface)

    def launch_program(self):
        self.open = True

class ChatSupport(Program):

    def __init__(self, icon: pygame.Surface):
        Program.__init__(self, icon, pygame.Vector2(20, 25), "Interconnect Chat")

