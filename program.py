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
        # Opening animation timer update
        if self.opening:
            self.open_timer += delta
            if self.open_timer > Program.launch_time:
                self.open = True
                self.opening = False

        # Closing animation timer update
        if self.closing:
            self.closing_timer += delta
            if self.closing_timer > Program.close_time:
                self.closing = False

        self.window.update(delta)

    def draw_icon(self, surface: pygame.Surface):
        surface.blit(self.icon, self.icon_rect)

        # When the icon is clicked but the window isn't open, color it blue by blending a blue surface
        if self.selected:
            surface.blit(self.selected_overlay, self.icon_rect, special_flags=pygame.BLEND_MULT)

    def draw_window(self, surface: pygame.Surface):
        if self.opening:
            # animate a rect going from the program to the size of the window
            # Limit it to make the animation more choppy (only updates every `launch_interval` seconds)
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
        self.setup_done = False
        
    def setup(self):
        self.dialogue_handler = dialogue_handler.DialogueHandler("dialogue.txt")
        self.chat_window = pygame.Surface(self.window.content_rect.size)
        self.setup_done = True
        
    def update(self, delta: float):
        super().update(delta)
        if not self.setup_done:
            self.setup()
        
    def draw_window(self, surface: pygame.Surface):
        super().draw_window(surface)
        if self.open:
            self.chat_window.fill((0, 0, 0))
            self.dialogue_handler.draw_text(self.chat_window, pygame.rect.Rect((0, 0), self.chat_window.size))
        
            surface.blit(self.chat_window, self.window.content_rect)

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

        self.asteroid_speed = 25
        self.asteroid_image = pygame.image.load("res/imgs/asteroid.png").convert_alpha()
        self.asteroid_size = self.asteroid_image.get_width() / 2

        self.asteroid_rect = self.asteroid_image.get_rect()
        self.asteroid_mask = pygame.mask.from_surface(self.asteroid_image)

        self.exploding = False
        self.explosion_timer = 0.0
        self.explosion_length = 5.0
        self.explosion_surf = pygame.Surface(self.game_window.size, flags=pygame.BLEND_ADD)

        self.alive = True
        
        self.setup_done = True
        
        self.asteroid_particles: list[particle.Particle] = []
        self.explosion_particles: list[particle.Particle] = []
        self.particle_interval = 0.05
        self.last_particle_time = 0.0
        
        self.last_laser_time = 0.0
        self.laser_interval = 0.5
        self.laser_draw_time = 0.5
        self.firing = False
        self.laser_target = pygame.Vector2()
        
        # The laser will blast chunks out of the asteroid and we will use masks to cut away
        self.laser_explosion_radius = 16
        laser_explosion_size = self.laser_explosion_radius * 2 + 1
        
        # Make a circular mask
        self.laser_explosion_mask = pygame.mask.Mask((laser_explosion_size, laser_explosion_size))
        for x in range(laser_explosion_size):
            for y in range(laser_explosion_size):
                x_diff = x - self.laser_explosion_radius
                y_diff = y - self.laser_explosion_radius
                if x_diff * x_diff + y_diff * y_diff <= self.laser_explosion_radius * self.laser_explosion_radius:
                    self.laser_explosion_mask.set_at((x, y))
        

    @staticmethod
    def draw_reticle(surface: pygame.Surface, location: pygame.Vector2):
        reticle_scale = 15
        corner_angle = math.radians(30)
        corner_offset = math.radians(120)
        corner_1 = pygame.Vector2(math.cos(corner_angle), math.sin(corner_angle)) * reticle_scale + location
        corner_2 = pygame.Vector2(math.cos(corner_angle + corner_offset), math.sin(corner_angle + corner_offset)) * reticle_scale + location
        corner_3 = pygame.Vector2(math.cos(corner_angle - corner_offset), math.sin(corner_angle - corner_offset)) * reticle_scale + location

        pygame.draw.polygon(surface, (220, 30, 30), [corner_1, corner_2, corner_3], 3)

    def handle_input(self):
        super().handle_input()
    
        # Fire the laser if we are clicking on the window and we haven't fired the laser recently
        if pygame.mouse.get_just_pressed()[0] and self.window.content_rect.collidepoint(pygame.mouse.get_pos()):
            if self.last_laser_time + self.laser_interval < self.window.open_timer:
                self.last_laser_time = self.window.open_timer
                self.firing = True
                self.laser_target = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(self.window.content_rect.topleft)
                
                if self.check_asteroid_laser_collision():
                    self.handle_asteroid_laser_collision()
                

    def update(self, delta: float):
        if not self.setup_done:
            self.setup()

        Program.update(self, delta)
        if self.open:
            
            # Asteroid only moves and creates a trail if it hasn't impacted
            if self.alive:
                self.asteroid_position += (self.asteroid_goal - self.asteroid_position).normalize() * self.asteroid_speed * delta
                self.asteroid_rect.center = self.asteroid_position

                # Check if the asteroid has impacted the ground
                if self.asteroid_position.y > self.game_window.get_rect().height - self.asteroid_size * 1.5:
                    self.exploding = True
                    self.explode_time = self.window.open_timer
                    self.alive = False
                    
                    # Add a bunch of particles right at the end
                    for _ in range(50):
                        self.add_asteroid_particle()

                    # Make all the particles move away from the asteroid
                    for p in self.asteroid_particles:
                        vec_to_asteroid = (self.asteroid_position - p.position)
                        p.velocity = (-vec_to_asteroid / vec_to_asteroid.magnitude()) * 100
                        p.lifetime = self.explosion_length
                
                # Add new particles every `particle_intervial` seconds
                if self.last_particle_time + self.particle_interval < self.window.open_timer:
                    self.last_particle_time = self.window.open_timer
                    self.add_asteroid_particle()
                
            # Update all asteroids
            for p in self.asteroid_particles:
                p.update(delta)
                
            for p in self.explosion_particles:
                p.update(delta)
                
            if self.firing and self.window.open_timer > self.last_laser_time + self.laser_draw_time:
                self.firing = False

            # Explosion animation
            if self.exploding:
                self.explosion_timer += delta
                self.exploding = self.explosion_timer < self.explosion_length
            
            # Remove any particles that are too old
            self.clean_up_particles()

        # If we have already died once and are now reopening the window, set it back up. Mostly for testing purposes.
        if not self.alive and self.opening:
            self.setup()
            
    def add_asteroid_particle(self):
        # Create and return a new particle moving away from the asteroid
        new_particle = particle.Particle(self.asteroid_position.copy() + helpers.random_vector2(8) - pygame.Vector2(0, 8), helpers.random_vector2(5), size_start=12, size_end=25, lifetime=2.0, colorstart=(200, 100, 20))
        self.asteroid_particles.append(new_particle)
        return new_particle
    
    def add_explosion_particle(self):
        new_particle = particle.Particle(self.laser_target.copy(), helpers.random_vector2(30), 16, 4, 1, (80, 52, 34))
        self.explosion_particles.append(new_particle)
        return new_particle
    
    def clean_up_particles(self):
        # Filter out any particles that are no longer alive. This probably isn't the most efficient way to do this
        self.asteroid_particles = list(filter(lambda particle: particle.isalive, self.asteroid_particles))
        self.explosion_particles = list(filter(lambda particle: particle.isalive, self.explosion_particles))
        
    def draw_laser(self):
        # Draw the laser going from the base to the mouse cursor
        window_rect = self.game_window.get_rect()
        laser_base_height = self.ground_rect.height / 2
        base_position = pygame.Vector2(window_rect.width / 2, window_rect.bottom - laser_base_height)
        
        # Laser ratio is the percentage we are through the animation
        laser_ratio = (self.window.open_timer - self.last_laser_time) / self.laser_draw_time
        
        # Laser gets slightly darker and thinner as the animation plays
        laser_color = helpers.lerp_rgb((255, 0, 0), (200, 0, 0), laser_ratio)
        laser_width = int(pygame.math.lerp(5, 1, laser_ratio))
        
        pygame.draw.line(self.game_window, laser_color, base_position, self.laser_target, laser_width)

    def handle_asteroid_laser_collision(self):
        offset = (self.laser_target - pygame.Vector2(self.laser_explosion_radius, self.laser_explosion_radius)) - (self.asteroid_position - pygame.Vector2(self.asteroid_size, self.asteroid_size))
        self.asteroid_mask.erase(self.laser_explosion_mask, offset)
        
        for _ in range(8):
            self.add_explosion_particle()
        
        # Remove the smallest chunk of the asteroid if two parts get separated
        self.asteroid_mask = self.asteroid_mask.connected_component()
        
    def check_asteroid_laser_collision(self):
        return (self.asteroid_position - self.laser_target).magnitude() < self.asteroid_size
    
    def check_asteroid_destroyed(self):
        return self.asteroid_mask.count() < 5

    def draw_asteroid(self):
        return self.asteroid_mask.to_surface(None, self.asteroid_image, None, None, (0, 0, 0, 0))

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
                    
                if self.firing:
                    self.draw_laser()

                # Draw asteroid
                # self.game_window.blit(self.asteroid_image, self.asteroid_rect)
                self.game_window.blit(self.draw_asteroid(), self.asteroid_rect)
                
                # Draw explosion particles
                for particle in self.explosion_particles:
                    particle.draw(self.game_window)
                
                if self.exploding:
                    # Draw the growing explosion
                    explode_ratio = self.explosion_timer / self.explosion_length
                    pygame.draw.circle(self.game_window, pygame.colordict.THECOLORS['white'], self.asteroid_position, pygame.math.lerp(self.asteroid_size, self.asteroid_size * 5, explode_ratio))

                    # The explosion surface slowly makes the screen more and more white
                    self.explosion_surf.fill(helpers.lerp_rgb((0, 0, 0), (255, 255, 255), explode_ratio))
                    self.game_window.blit(self.explosion_surf, (0, 0), special_flags=pygame.BLEND_ADD)

                else:
                    # Reticle, don't draw during explosion
                    LaserCommand.draw_reticle(self.game_window, pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(self.window.content_rect.topleft))

            else:
                # Draw a "lost connection" screen
                self.window.draw_fuzzy_screen(self.game_window)

            # Draw the final window onto the screen
            surface.blit(self.game_window, self.window.content_rect)
