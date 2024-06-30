
import pygame

TILE_SIZE = 32

class Item:
    ITEM_TYPES = {
        'health_potion': {'color': (255, 0, 0), 'effect': ('hp', 20)},
        'mana_potion': {'color': (0, 0, 255), 'effect': ('mp', 15)},
        'sword': {'color': (200, 200, 200), 'effect': ('attack', 5)},
        'shield': {'color': (150, 150, 150), 'effect': ('defense', 3)},
    }

    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.color = self.ITEM_TYPES[item_type]['color']
        self.effect = self.ITEM_TYPES[item_type]['effect']

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x * TILE_SIZE + 4, self.y * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8))