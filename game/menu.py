import pygame
from constants import *
from utils import draw_text, draw_button


class Menu:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 32)

    def draw_main_menu(self, screen):
        screen.fill(BLACK)
        draw_text(screen, "PixelQuest", self.font_large, WHITE, SCREEN_WIDTH // 2, 100, align="center")

        start_button = draw_button(screen, "Start Game", self.font_medium, BLACK, WHITE,
                                   SCREEN_WIDTH // 2 - 100, 300, 200, 50)
        quit_button = draw_button(screen, "Quit", self.font_medium, BLACK, WHITE,
                                  SCREEN_WIDTH // 2 - 100, 400, 200, 50)

        return start_button, quit_button

    def draw_game_over(self, screen, score):
        screen.fill(BLACK)
        draw_text(screen, "Game Over", self.font_large, WHITE, SCREEN_WIDTH // 2, 100, align="center")
        draw_text(screen, f"Score: {score}", self.font_medium, WHITE, SCREEN_WIDTH // 2, 200, align="center")

        restart_button = draw_button(screen, "Restart", self.font_medium, BLACK, WHITE,
                                     SCREEN_WIDTH // 2 - 100, 300, 200, 50)
        quit_button = draw_button(screen, "Quit", self.font_medium, BLACK, WHITE,
                                  SCREEN_WIDTH // 2 - 100, 400, 200, 50)

        return restart_button, quit_button
