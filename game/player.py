import pygame
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 50
        self.speed = 5

    def update(self, keys, tiles):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if keys[pygame.K_LEFT]:
                    self.rect.left = tile.rect.right
                if keys[pygame.K_RIGHT]:
                    self.rect.right = tile.rect.left
                if keys[pygame.K_UP]:
                    self.rect.top = tile.rect.bottom
                if keys[pygame.K_DOWN]:
                    self.rect.bottom = tile.rect.top

    def attack_enemy(self, enemy):
        damage = random.randint(1, 3)
        print(f"Player attacks enemy for {damage} damage!")
        enemy.health -= damage

    def draw_health_bar(self, screen, offset_x, offset_y):
        bar_width = 50
        bar_height = 5
        fill = (self.health / 50) * bar_width
        outline_rect = pygame.Rect(self.rect.x + offset_x, self.rect.y + offset_y - 10, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x + offset_x, self.rect.y + offset_y - 10, fill, bar_height)
        pygame.draw.rect(screen, GREEN, fill_rect)
        pygame.draw.rect(screen, WHITE, outline_rect, 1)
