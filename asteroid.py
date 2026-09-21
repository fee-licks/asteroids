import pygame
import random
from circleshape import CircleShape
from constants import *
from logger import log_event

class Asteroid(CircleShape):

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        new_angle = random.uniform(20, 50)
        first_split_angle = self.velocity.rotate(new_angle)
        second_split_angle = self.velocity.rotate(-new_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        first_split_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        second_split_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        first_split_asteroid.velocity = first_split_angle * 1.2
        second_split_asteroid.velocity = second_split_angle * 1.2

    def update(self, dt:float) -> None:
        self.position += self.velocity * dt