import pygame

class Desktop:

    background_color = (5, 144, 186)

    def __init__(self, desktop_space: pygame.Rect):
        self.programs: list[Program] = []
        self.rect = desktop_space

        self.desktop_image = pygame.Surface(self.rect.size)

    def draw(self, surface: pygame.Surface, draw_rect: pygame.Rect):
        self.desktop_image.fill(Desktop.background_color)

        for program in self.programs:
            program.draw(self.desktop_image)

        surface.blit(self.desktop_image, draw_rect)

class Program:

    def __init__(self, icon: pygame.Surface, position: pygame.Vector2 = pygame.Vector2()):
        self.icon = icon
        self.position = position

        self.selected = False
        self.opening = False
        self.open = False

        self.rect = pygame.Rect(self.position, self.icon.size)

        self.selected_overlay = pygame.Surface(self.rect.size)
        self.selected_overlay.fill((0, 0, 0))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.icon, self.position)

        if self.selected:
            # cover_surface = pygame.Surface()
            # surface.blit()
            pass

class ChatSupport(Program):

    def __init__(self, icon: pygame.Surface):
        Program.__init__(self, icon, pygame.Vector2(50, 50))

