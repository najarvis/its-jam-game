import math
import pygame
import program

class Desktop:

    background_color = (5, 144, 186)

    def __init__(self, desktop_space: pygame.Rect):
        self.programs: list[program.Program] = []
        self.rect = desktop_space

        self.desktop_image = pygame.Surface(self.rect.size)

        self.mouse_held = False
        self.was_mouse_held = False
        self.mouse_offset: pygame.Vector2 = pygame.Vector2()
        self.inside_title = False

    @property
    def focused_program(self) -> program.Program:
        return self.programs[-1]

    def draw(self, surface: pygame.Surface, draw_rect: pygame.Rect):
        self.desktop_image.fill(Desktop.background_color)

        for cur_program in self.programs:
            cur_program.draw_icon(self.desktop_image)

        surface.blit(self.desktop_image, draw_rect)

        for cur_program in self.programs:
            #cur_program.update(delta)
            cur_program.handle_input()
            if cur_program.open or cur_program.opening or cur_program.closing:
                cur_program.draw_window(surface)

    def update(self, delta: float):
        self.was_mouse_held = self.mouse_held
        self.mouse_held = pygame.mouse.get_pressed()[0]
        move_by = pygame.mouse.get_rel()
        
        if self.mouse_held and not self.was_mouse_held and self.focused_program.window.title_bar_rect.collidepoint(pygame.mouse.get_pos()):
            self.inside_title = True

        if self.mouse_held and self.was_mouse_held and self.inside_title:
            self.focused_program.window.position += pygame.Vector2(move_by)

        if not self.mouse_held and self.was_mouse_held:
            self.inside_title = False

        for cur_program in self.programs:
            cur_program.update(delta)


    def detect_window_click(self, pos: pygame.Vector2):
        selected = -1
        for i, program in enumerate(self.programs):
            program.window.focused = False
            if program.open:
                if program.open and program.window.rect.collidepoint(pos):
                    selected = i
                    

        if selected == -1:
            return

        self.programs[selected].window.focused = True
        first = self.programs.pop(selected)
        self.programs.append(first)
        
