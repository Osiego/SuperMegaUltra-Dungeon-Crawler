import pygame
import random

TILE_SIZE = 32


class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.hp = 20 + 10 * enemy_type
        self.max_hp = self.hp
        self.attack = 5 + 2 * enemy_type
        self.defense = 2 + enemy_type
        self.xp_value = 10 + 5 * enemy_type
        self.gold_value = 5 + 3 * enemy_type
        self.sprite = pygame.image.load(f"assets/enemy{enemy_type + 1}.png")
        self.sprite = pygame.transform.scale(self.sprite, (TILE_SIZE, TILE_SIZE))

    def move(self, player, level):
        dx = player.x - self.x
        dy = player.y - self.y
        if abs(dx) + abs(dy) <= 5:  # Only move if player is within 5 tiles
            if random.random() < 0.8:  # 80% chance to move towards player
                if abs(dx) > abs(dy):
                    new_x = self.x + (1 if dx > 0 else -1)
                    if level.is_walkable(new_x, self.y):
                        self.x = new_x
                else:
                    new_y = self.y + (1 if dy > 0 else -1)
                    if level.is_walkable(self.x, new_y):
                        self.y = new_y
            else:  # 20% chance to move randomly
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                new_x = self.x + direction[0]
                new_y = self.y + direction[1]
                if level.is_walkable(new_x, new_y):
                    self.x = new_x
                    self.y = new_y

    def draw(self, screen):
        screen.blit(self.sprite, (self.x * TILE_SIZE, self.y * TILE_SIZE))
        # Draw health bar
        health_percentage = self.hp / self.max_hp
        pygame.draw.rect(screen, (255, 0, 0), (self.x * TILE_SIZE, self.y * TILE_SIZE - 5, TILE_SIZE, 3))
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.x * TILE_SIZE, self.y * TILE_SIZE - 5, int(TILE_SIZE * health_percentage), 3))
