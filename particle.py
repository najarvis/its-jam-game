import pygame
import helpers

class Particle:
    
    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, size: float, lifetime=1.0, colorstart=(255, 255, 255), colorend=(0, 0, 0)):
        self.position = position
        self.velocity = velocity
        self.size = size
        self.lifetime = lifetime
        self.t = 0
        
        self.colorstart = colorstart
        self.colorend = colorend
        self.color = self.colorstart
        
    def update(self, delta: float):
        self.t += delta
        
        lifetime_ratio = self.t / self.lifetime
        
        self.position += self.velocity * delta
        
        self.color = helpers.lerp_rgb(self.colorstart, self.colorend, lifetime_ratio)
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.size)
        
    @property
    def isalive(self):
        return self.t < self.lifetime