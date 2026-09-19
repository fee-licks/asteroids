import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotation_vector = unit_vector.rotate(self.rotation) # Get vector direction
        movement_vector = rotation_vector * PLAYER_SPEED * dt # Get vector velocity
        self.position += movement_vector

    def shoot(self) -> None:
        if self.shot_cooldown > 0:
            pass
        else:
            new_shot = Shot(self.position.x, self.position.y)
            new_shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.shot_cooldown += PLAYER_SHOOT_COOLDOWN_SECONDS

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.shot_cooldown -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt) # Invert delta time to rotate ccw
        if keys[pygame.K_d]:
            self.rotate(dt) # Use delta time to rotate cw
        if keys[pygame.K_w]:
            self.move(dt) # Use delta time to move forward
        if keys[pygame.K_s]:
            self.move(-dt) # Invert delta time to move backwards
        if keys[pygame.K_SPACE]:
            self.shoot()