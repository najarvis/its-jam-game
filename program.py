import math
import random
import pygame
import window
import dialogue_handler
import helpers
import particle

class Program:
    """A program is something that is launchable and has an icon that lives on the desktop"""

    launch_time = 1
    launch_interval = 0.05
    close_time = 0.5

    def __init__(self, icon: pygame.Surface, position: pygame.Vector2 = pygame.Vector2(), name: str="Program", size: pygame.Vector2=(250, 300)):
        self.icon = icon
        self.position: pygame.Vector2 = position
        self.icon_rect = pygame.Rect(self.position, self.icon.size)

        self.selected = False
        self.opening = False
        self.open = False
        self.open_timer = 0
        self.closing = False
        self.closing_timer = 0

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

        if self.closing:
            self.closing_timer += delta
            if self.closing_timer > Program.close_time:
                self.closing = False

        self.window.update(delta)

    def draw_icon(self, surface: pygame.Surface):
        surface.blit(self.icon, self.icon_rect)

        if self.selected:
            surface.blit(self.selected_overlay, self.icon_rect, special_flags=pygame.BLEND_MULT)

    def draw_window(self, surface: pygame.Surface):
        if self.opening:
            # animate a rect going from the program to the size of the window
            # Limit it to make the animation more choppy
            t = (self.open_timer - math.fmod(self.open_timer, self.launch_interval)) / Program.launch_time
            rect_width = pygame.math.lerp(self.icon.width, self.window.size.x, t)
            rect_height = pygame.math.lerp(self.icon.height, self.window.size.y, t)
            rect_pos = self.position + (self.window.position - self.position) * t
            pygame.draw.rect(surface, (30, 30, 30), pygame.rect.FRect(rect_pos, (rect_width, rect_height)), 1)
        
        elif self.closing:
            # animate a rect going from the window to the size of the program
            # Limit it to make the animation more choppy
            t = (self.closing_timer - math.fmod(self.closing_timer, self.launch_interval)) / Program.close_time
            rect_width = pygame.math.lerp(self.window.size.x, self.icon.width, t)
            rect_height = pygame.math.lerp(self.window.size.y, self.icon.height, t)
            rect_pos = self.window.position + (self.position - self.window.position) * t
            pygame.draw.rect(surface, (30, 30, 30), pygame.rect.FRect(rect_pos, (rect_width, rect_height)), 1)
        
        else:
            self.window.draw(surface)

    def launch_program(self):
        self.opening = True
        self.open_timer = 0

    def handle_input(self):
        if pygame.mouse.get_pressed()[0] and self.open and self.window.check_close(pygame.mouse.get_pos()):
            self.close_program()

    def close_program(self):
        self.open = False
        self.closing = True
        self.closing_timer = 0

class ChatSupport(Program):

    def __init__(self, icon: pygame.Surface):
        Program.__init__(self, icon, pygame.Vector2(20, 25), "Interconnect Chat", pygame.Vector2(250, 300))

class LaserCommand(Program):

    def __init__(self, icon: pygame.Surface):
        Program.__init__(self, icon, pygame.Vector2(20, 100), "Laser Command", pygame.Vector2(300, 400))

        self.game_window = pygame.Surface(self.window.content_rect.size)
        self.setup_done = False
        
    def setup(self):
        self.sky_color = helpers.random_hue(80, 80)
        self.ground_color = helpers.random_hue(80, 50)
        
        self.ground_rect = self.game_window.get_rect()
        self.ground_rect.top += self.game_window.height * 0.9
        self.ground_rect.height *= 0.10
        
        self.asteroid_position = pygame.Vector2(random.randint(0, int(self.window.size.x)), 0)
        self.asteroid_goal = pygame.Vector2(random.randint(int(self.window.size.x * 0.25), int(self.window.size.x * 0.75)), self.window.size.y)

        self.asteroid_speed = 50
        self.asteroid_size = 32
        self.asteroid_image = pygame.image.load("res/imgs/asteroid.png").convert_alpha()

        self.asteroid_rect = self.asteroid_image.get_rect()

        self.exploding = False
        self.explosion_timer = 0.0
        self.explosion_length = 5.0
        self.explosion_surf = pygame.Surface(self.game_window.size, flags=pygame.BLEND_ADD)

        self.alive = True
        
        self.setup_done = True
        
        self.asteroid_particles: list[particle.Particle] = []
        self.particle_interval = 0.05
        self.last_particle_time = 0.0

    @staticmethod
    def draw_reticle(surface: pygame.Surface, location: pygame.Vector2):
        reticle_scale = 15
        corner_angle = math.radians(30)
        corner_offset = math.radians(120)
        corner_1 = pygame.Vector2(math.cos(corner_angle), math.sin(corner_angle)) * reticle_scale + location
        corner_2 = pygame.Vector2(math.cos(corner_angle + corner_offset), math.sin(corner_angle + corner_offset)) * reticle_scale + location
        corner_3 = pygame.Vector2(math.cos(corner_angle - corner_offset), math.sin(corner_angle - corner_offset)) * reticle_scale + location

        pygame.draw.polygon(surface, (220, 30, 30), [corner_1, corner_2, corner_3], 3)


    def update(self, delta: float):
        if not self.setup_done:
            self.setup()

        Program.update(self, delta)
        if self.open:
                
            if self.alive:
                self.asteroid_position += (self.asteroid_goal - self.asteroid_position).normalize() * self.asteroid_speed * delta
                self.asteroid_rect.center = self.asteroid_position

                if self.asteroid_position.y > self.game_window.get_rect().height - self.asteroid_size * 1.5:
                    self.exploding = True
                    self.explode_time = self.window.open_timer
                    self.alive = False
                    for _ in range(50):
                        self.add_asteroid_particle()

                    for p in self.asteroid_particles:
                        vec_to_asteroid = (self.asteroid_position - p.position)
                        p.velocity = (-vec_to_asteroid / vec_to_asteroid.magnitude()) * 100
                        p.lifetime = self.explosion_length
                
                if self.last_particle_time + self.particle_interval < self.window.open_timer:
                    self.last_particle_time = self.window.open_timer
                    self.add_asteroid_particle()
                
            for p in self.asteroid_particles:
                p.update(delta)

            if self.exploding:
                self.explosion_timer += delta
                self.exploding = self.explosion_timer < self.explosion_length
                p = self.add_asteroid_particle()
                vec_to_asteroid = (self.asteroid_position - p.position)
                p.velocity = (-vec_to_asteroid / vec_to_asteroid.magnitude()) * 100
                p.lifetime = self.explosion_length
                
            self.clean_up_particles()

        if not self.alive and self.opening:
            self.setup()
            
    def add_asteroid_particle(self):
        # asteroid_velocity = (self.asteroid_goal - self.asteroid_position).normalize() * self.asteroid_speed
        new_particle = particle.Particle(self.asteroid_position.copy() + helpers.random_vector2(8) - pygame.Vector2(0, 8), helpers.random_vector2(5), size_start=12, size_end=25, lifetime=2.0, colorstart=(200, 100, 20))
        self.asteroid_particles.append(new_particle)
        return new_particle
    
    def clean_up_particles(self):
        self.asteroid_particles = list(filter(lambda particle: particle.isalive, self.asteroid_particles))

    def draw_window(self, surface: pygame.Surface):
        Program.draw_window(self, surface)

        if self.open:
            if self.alive or self.exploding:
                # Draw sky
                self.game_window.fill(self.sky_color)
                
                # Draw the ground
                pygame.draw.rect(self.game_window, self.ground_color, self.ground_rect)

                # Draw asteroid particles
                for particle in self.asteroid_particles:
                    particle.draw(self.game_window)

                # Draw asteroid
                self.game_window.blit(self.asteroid_image, self.asteroid_rect)
                
                if self.exploding:
                    explode_ratio = self.explosion_timer / self.explosion_length
                    pygame.draw.circle(self.game_window, pygame.colordict.THECOLORS['white'], self.asteroid_position, pygame.math.lerp(self.asteroid_size, self.asteroid_size * 5, explode_ratio))

                    self.explosion_surf.fill(helpers.lerp_rgb((0, 0, 0), (255, 255, 255), explode_ratio))
                    self.game_window.blit(self.explosion_surf, (0, 0), special_flags=pygame.BLEND_ADD)

                else:
                    # Reticle
                    LaserCommand.draw_reticle(self.game_window, pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(self.window.content_rect.topleft))

            else:
                self.window.draw_fuzzy_screen(self.game_window)

            # Draw the final window onto the screen
            surface.blit(self.game_window, self.window.content_rect)
