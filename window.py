import pygame


class Window:

    title_bar_height = 40
    title_bar_font_size = 25

    def __init__(self, size, position, title, font: pygame.font.Font=None):
        self.size = size
        self.position = position
        self.rect = pygame.rect.Rect(self.position, self.size)
        self.title_bar_rect = pygame.rect.Rect(self.position, (self.rect.width, Window.title_bar_height))

        self.title = title
        self.font: pygame.font.Font = font
        if self.font is None:
            self.get_font()

        self.title_bar_text = self.font.render(self.title, True, (0, 0, 0))
        self.title_bar_text_rect = self.title_bar_text.get_rect(center = self.title_bar_rect.center)

    def get_font(self):
        assert pygame.font.get_init()

        self.font = pygame.font.SysFont(None, Window.title_bar_font_size)

    def draw(self, surface):
        # Outer border
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

        # Title bar
        pygame.draw.rect(surface, (0, 0, 0), self.title_bar_rect, 1)

        surface.blit(self.title_bar_text, self.title_bar_text_rect)
