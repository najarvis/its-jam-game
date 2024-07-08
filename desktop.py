import math
import pygame
import program

class Desktop:
    """The desktop stores references to each program, draws the icons and windows, and passes along input and signals"""
    
    background_color = (5, 144, 186)

    def __init__(self, desktop_space: pygame.Rect):
        self.programs: list[program.Program] = []
        self.rect = desktop_space
        
        self.taskbar_size = 25
        self.taskbar_rect = pygame.rect.FRect(0, self.rect.height - self.taskbar_size, self.rect.width, self.taskbar_size)

        self.desktop_image = pygame.Surface(self.rect.size)

        # Variables to help with dragging windows by their title bars
        self.mouse_held = False
        self.was_mouse_held = False
        self.mouse_offset: pygame.Vector2 = pygame.Vector2()
        self.inside_title = False

    @property
    def focused_program(self) -> program.Program:
        return self.programs[-1]

    def draw(self, surface: pygame.Surface, draw_rect: pygame.Rect):
        self.desktop_image.fill(Desktop.background_color)

        # Draw each program (both the icon and window if it should be open).
        # TODO: Icons should not have their own position, the desktop should assign them automatically
        for cur_program in self.programs:
            cur_program.draw_icon(self.desktop_image)
            if cur_program.open or cur_program.opening or cur_program.closing:
                cur_program.draw_window(self.desktop_image)

        # Draw the taskbar
        pygame.draw.rect(self.desktop_image, (200, 200, 200), self.taskbar_rect)
        
        # Draw the desktop image to the screen (or whatever surface is passed)
        surface.blit(self.desktop_image, draw_rect)

    def update(self, delta: float):
        self.was_mouse_held = self.mouse_held
        self.mouse_held = pygame.mouse.get_pressed()[0]
        move_by = pygame.mouse.get_rel() # NOTE: This function calculates based on the last time it was called. Can't really use this anywhere else without messing this up.
        
        # If the user clicks on the title bar and then holds down the mouse,
        # allow them to move the window around by draggin their mouse
        if self.mouse_held and not self.was_mouse_held and self.focused_program.window.title_bar_rect.collidepoint(pygame.mouse.get_pos()):
            self.inside_title = True

        if self.mouse_held and self.was_mouse_held and self.inside_title:
            self.focused_program.window.position += pygame.Vector2(move_by)

        if not self.mouse_held and self.was_mouse_held:
            self.inside_title = False

        # Update and handle input for each program
        for cur_program in self.programs:
            cur_program.handle_input()
            cur_program.update(delta)


    def detect_window_click(self, pos: pygame.Vector2):
        # Since the programs are drawn in the order of their appearance in 
        # self.programs, the "topmost" and focused window should occupy the
        # last element in the array.
        #
        # When the user clicks on the screen, find the window they collide with
        # that is "highest up" and make it the new focused window
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
        
