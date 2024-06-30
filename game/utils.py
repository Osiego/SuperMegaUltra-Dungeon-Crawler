import pygame
from constants import *

def load_image(filename, scale=1):
    image = pygame.image.load(f"assets/{filename}")
    if scale != 1:
        new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
        image = pygame.transform.scale(image, new_size)
    return image

def draw_text(surface, text, font, color, x, y, align="left"):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "center":
        text_rect.centerx = x
    elif align == "right":
        text_rect.right = x
    else:
        text_rect.left = x
    text_rect.top = y
    surface.blit(text_surface, text_rect)


def draw_button(surface, text, font, text_color, button_color, x, y, width, height):
    pygame.draw.rect(surface, button_color, (x, y, width, height))
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surf, text_rect)
    return pygame.Rect(x, y, width, height)
