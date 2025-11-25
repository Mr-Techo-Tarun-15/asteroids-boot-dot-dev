import pygame, sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_SHOOT_COOLDOWN_SECONDS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

clock_object = pygame.time.Clock()
dt = 0

updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
Player.containers = (updatable, drawable)

asteroids = pygame.sprite.Group()
Asteroid.containers = (asteroids, updatable, drawable)
AsteroidField.containers = (updatable)
asteroid_field = AsteroidField()

shots = pygame.sprite.Group()
Shot.containers = (shots, updatable)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player = Player((0.5 * SCREEN_WIDTH), (0.5 * SCREEN_HEIGHT), PLAYER_SHOOT_COOLDOWN_SECONDS)

    while True:
        log_state(updatable, drawable, asteroids, shots)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        
        for item in drawable:
            item.draw(screen)
            
        for shot in shots:
            shot.draw(screen)
            
        pygame.display.flip()
        
        dt = clock_object.tick(60) / 1000
        updatable.update(dt)
        
        for asteroid in asteroids:
            if player.collides_with(asteroid) == True:
                log_event("player_hit")                
                print("Game Over!")
                sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid) == True:
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()


if __name__ == "__main__":
    main()