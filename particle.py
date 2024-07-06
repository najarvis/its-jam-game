import pygame
import helpers

class Particle:
    
    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, size_start: float, size_end: float, lifetime=1.0, colorstart=(255, 255, 255), colorend=(0, 0, 0)):
        self.position = position
        self.velocity = velocity
        self.size = size_start
        self.size_start = size_start
        self.size_end = size_end
        self.lifetime = lifetime
        self.t = 0
        
        self.colorstart = colorstart
        self.colorend = colorend
        self.color = self.colorstart
        
    def update(self, delta: float):
        self.t += delta
        self.position += self.velocity * delta
        
        lifetime_ratio = self.t / self.lifetime
        self.color = helpers.lerp_rgb(self.colorstart, self.colorend, lifetime_ratio)
        self.size = pygame.math.lerp(self.size_start, self.size_end, lifetime_ratio)
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.size)
        
    @property
    def isalive(self):
        return self.t < self.lifetime