import pygame
from settings import *
from health_bar import HealthBar

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.max_health = 12
        self.health = self.max_health
        self.attack_damage = 2
        self.health_bar = HealthBar(self)

    def update(self, player):
        # Simple enemy AI: move towards the player
        if player.rect.x > self.rect.x:
            self.rect.x += 1
        elif player.rect.x < self.rect.x:
            self.rect.x -= 1
        if player.rect.y > self.rect.y:
            self.rect.y += 1
        elif player.rect.y < self.rect.y:
            self.rect.y -= 1

    def take_damage(self, amount):
        self.health -= amount
        print(f"Enemy takes {amount} damage, health now {self.health}")
        if self.health <= 0:
            self.kill()

    def attack(self, player):
        damage = self.attack_damage
        player.take_damage(damage)
        print(f"Enemy attacks player for {damage} damage!")

    def draw_health_bar(self, screen, offset_x, offset_y):
        self.health_bar.draw(screen, offset_x, offset_y)
