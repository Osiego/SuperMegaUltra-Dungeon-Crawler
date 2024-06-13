import pygame
from settings import *


class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)  # Use default font and size 36

    def draw(self, screen):
        # Render health text
        health_text = self.font.render(
            f'Health: {self.player.health}', True, WHITE)
        screen.blit(health_text, (10, 10))  # Draw at top left corner

        # Render score text
        score_text = self.font.render(
            f'Score: {self.player.score}', True, WHITE)
        screen.blit(score_text, (10, 50))  # Draw below health text
