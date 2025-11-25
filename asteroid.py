import pygame
import random
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from circleshape import CircleShape
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, velocity=pygame.Vector2(0, 0)):
        super().__init__(x, y, radius)
        self.velocity = velocity
        
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)        
   
    def update(self, dt):
        self.position += self.velocity * dt
        
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            random_rotation = random.uniform(20, 50)
            first_new_velocity_vector = self.velocity.rotate(random_rotation)
            first_new_velocity_vector *= 1.2

            second_new_velocity_vector = self.velocity.rotate(-random_rotation)
            second_new_velocity_vector *= 1.2
            
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            
            Asteroid(self.position.x, self.position.y, new_radius, first_new_velocity_vector)
            
            Asteroid(self.position.x, self.position.y, new_radius, second_new_velocity_vector)
