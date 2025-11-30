import pygame
from circleshape import CircleShape
from constants import PLAYER_SHOOT_COOLDOWN_SECONDS

class Shot(CircleShape):
    def __init__(self, x, y, radius, velocity):
        super().__init__(x, y, radius)
        self.velocity = velocity
    
    def draw(self, screen):
        # Draw a solid white bullet
        pygame.draw.circle(screen, "cyan", self.position, self.radius)
        
    def update(self, dt):
        self.position += self.velocity * dt