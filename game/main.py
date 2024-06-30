import pygame
from game import Game
from constants import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PixelQuest: Procedural Dungeon Crawler")

    game = Game(screen)
    game.run()


if __name__ == "__main__":
    main()

