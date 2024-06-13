import pygame


class HealthBar:
    def __init__(self, entity):
        self.entity = entity
        self.max_width = 50
        self.height = 5

    def draw(self, screen, offset_x, offset_y):
        # Calculate the current width based on health
        current_width = int(self.max_width * (self.entity.health / self.entity.max_health))

        # Background (black)
        pygame.draw.rect(screen, (0, 0, 0),
                         (
                         self.entity.rect.x + offset_x, self.entity.rect.y + offset_y - self.height - 2, self.max_width,
                         self.height))

        # Health bar (red)
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.entity.rect.x + offset_x, self.entity.rect.y + offset_y - self.height - 2, current_width,
                          self.height))
