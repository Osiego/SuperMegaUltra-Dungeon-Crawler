import pygame
import random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 12
        self.speed = 2
        self.update_click_box()

    def update(self, player):
        if self.health > 0:
            direction = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y).normalize()
            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed
            self.update_click_box()

    def update_click_box(self):
        self.click_box = pygame.Rect(self.rect.left - 20, self.rect.top - 20, self.rect.width + 40, self.rect.height + 40)

    def attack(self, player):
        damage = random.randint(1, 3)
        print(f"Enemy attacks player for {damage} damage!")
        player.health -= damage

    def draw_health_bar(self, screen, offset_x, offset_y):
        bar_width = 50
        bar_height = 5
        fill = (self.health / 12) * bar_width
        outline_rect = pygame.Rect(self.rect.x + offset_x, self.rect.y + offset_y - 10, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x + offset_x, self.rect.y + offset_y - 10, fill, bar_height)
        pygame.draw.rect(screen, GREEN, fill_rect)
        pygame.draw.rect(screen, WHITE, outline_rect, 1)
