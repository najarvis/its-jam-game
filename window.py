import pygame
import helpers


class Window:

    title_bar_height = 40
    title_bar_font_size = 25

    def __init__(self, size: pygame.Vector2, position: pygame.Vector2, title: str, font: pygame.font.Font=None):
        self.size: pygame.Vector2 = size
        self.position: pygame.Vector2 = position
        self.rect = pygame.rect.Rect(self.position, self.size)
        self.title_bar_rect = pygame.rect.Rect(self.position, (self.rect.width, Window.title_bar_height))

        self.title = title
        self.font: pygame.font.Font = font
        if self.font is None:
            self.get_font()

        self.title_bar_text = self.font.render(self.title, True, (0, 0, 0))
        self.title_bar_text_rect = self.title_bar_text.get_rect(center = self.title_bar_rect.center)

        self.content_rect = pygame.rect.Rect(self.position.x, self.position.y + Window.title_bar_height,
                                             self.size.x, self.size.y - Window.title_bar_height)

        self.close_rect = pygame.rect.Rect(pygame.Vector2(self.title_bar_rect.right - Window.title_bar_height * 0.75,
                                                          self.title_bar_rect.top + Window.title_bar_height // 4),
                                           pygame.Vector2(Window.title_bar_height // 2, 
                                                          Window.title_bar_height // 2))
        
        self.overlay_image = pygame.Surface(self.size)
        self.overlay_image.set_alpha(40)
        
        self.focused = False
        
        self.open_timer = 0.0
        self.fuzzy_interval = 0.25
        self.fuzzy_time = 0.0
        self.fuzzy_size = 16 # size of fuzzy particles

    def get_font(self):
        assert pygame.font.get_init()

        self.font = pygame.font.SysFont(None, Window.title_bar_font_size)


    def update(self, delta: float):
        self.rect.topleft = self.position
        self.title_bar_rect.topleft = self.rect.topleft
        self.title_bar_text_rect.center = self.title_bar_rect.center

        self.close_rect = pygame.rect.Rect(pygame.Vector2(self.title_bar_rect.right - Window.title_bar_height * 0.75,
                                                          self.title_bar_rect.top + Window.title_bar_height // 4),
                                           pygame.Vector2(Window.title_bar_height // 2, 
                                                          Window.title_bar_height // 2))
                                                          
        self.content_rect = pygame.rect.Rect(self.position.x, self.position.y + Window.title_bar_height,
                                             self.size.x, self.size.y - Window.title_bar_height)
        
        self.open_timer += delta

    def draw(self, surface: pygame.Surface):
        title_color = (240, 240, 240)
        background_color = helpers.adjust_brightness_rgb(*title_color, 0.9)
        close_color = (200, 40, 0)

        # Outer border
        pygame.draw.rect(surface, background_color, self.rect)
        pygame.draw.line(surface, helpers.adjust_brightness_rgb(*background_color, 0.5), *helpers.bottom_edge_line(self.rect))

        # Title bar
        pygame.draw.rect(surface, title_color, self.title_bar_rect)
        pygame.draw.line(surface, helpers.adjust_brightness_rgb(*title_color, 0.5), *helpers.bottom_edge_line(self.title_bar_rect))

        # Title text
        surface.blit(self.title_bar_text, self.title_bar_text_rect)

        # Close Button
        pygame.draw.rect(surface, close_color, self.close_rect)
        pygame.draw.line(surface, helpers.adjust_brightness_rgb(*close_color, 0.5), *helpers.bottom_edge_line(self.close_rect))

        if not self.focused:
            surface.blit(self.overlay_image, self.rect)

    def draw_fuzzy_screen(self, surface: pygame.Surface):
        if self.open_timer - self.fuzzy_time > self.fuzzy_interval:
            self.fuzzy_time = self.open_timer

            for x in range((self.content_rect.width // self.fuzzy_size) + 1):
                for y in range((self.content_rect.height // self.fuzzy_size) + 1):
                    pygame.draw.rect(surface, helpers.random_gray(), (x * self.fuzzy_size, y * self.fuzzy_size, self.fuzzy_size, self.fuzzy_size))


    def check_close(self, pos: pygame.Vector2) -> bool:
        return self.close_rect.collidepoint(pos) and self.focused
        