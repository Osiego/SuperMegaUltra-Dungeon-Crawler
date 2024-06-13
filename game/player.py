import pygame
import random
from settings import *
from health_bar import HealthBar

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 1
        self.max_health = 50
        self.health = self.max_health
        self.score = 0
        self.attack_damage = 10
        self.turn_points = 0
        self.health_bar = HealthBar(self)

    def update(self, keys, walls):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        self.rect.x += dx
        self.rect.y += dy

        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x -= dx
            self.rect.y -= dy

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            print("Player died")
            self.kill()

    def add_score(self, points):
        self.score += points

    def attack_enemy(self, enemy):
        damage = random.randint(0, 3)  # Unarmed attack deals 0-3 damage
        enemy.take_damage(damage)
        print(f"Player attacks enemy for {damage} damage!")

    def draw_health_bar(self, screen, offset_x, offset_y):
        self.health_bar.draw(screen, offset_x, offset_y)
