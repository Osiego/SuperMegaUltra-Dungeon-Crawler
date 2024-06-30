import pygame
from constants import *
from level import Level
from player import Player
from ui import UI
from menu import Menu


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state = STATE_MAIN_MENU
        self.level = None
        self.player = None
        self.ui = None
        self.menu = Menu()
        self.message_log = []
        self.score = 0

    def run(self):
        running = True
        while running:
            if self.state == STATE_MAIN_MENU:
                running = self.run_main_menu()
            elif self.state == STATE_PLAYING:
                running = self.run_game()
            elif self.state == STATE_GAME_OVER:
                running = self.run_game_over()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def run_main_menu(self):
        start_button, quit_button = self.menu.draw_main_menu(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    self.start_new_game()
                elif quit_button.collidepoint(event.pos):
                    return False

        return True

    def run_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.handle_input(event.key)

        self.update()
        self.draw()
        return True

    def run_game_over(self):
        restart_button, quit_button = self.menu.draw_game_over(self.screen, self.score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    self.start_new_game()
                elif quit_button.collidepoint(event.pos):
                    return False

        return True

    def start_new_game(self):
        self.level = Level(1)
        self.player = Player(self.level.rooms[0].center()[0], self.level.rooms[0].center()[1])
        self.ui = UI(self.player)
        self.message_log = []
        self.score = 0
        self.state = STATE_PLAYING

    def handle_input(self, key):
        dx, dy = 0, 0
        if key == pygame.K_UP:
            dy = -1
        elif key == pygame.K_DOWN:
            dy = 1
        elif key == pygame.K_LEFT:
            dx = -1
        elif key == pygame.K_RIGHT:
            dx = 1
        elif key == pygame.K_SPACE:
            self.player.use_item()
        elif key == pygame.K_TAB:
            self.player.cycle_equipped_item()

        if dx != 0 or dy != 0:
            self.player.move(dx, dy, self.level)
            self.check_for_item_pickup()
            self.check_for_enemy_collision()
            self.check_for_stairs()

    def update(self):
        for enemy in self.level.enemies:
            enemy.move(self.player, self.level)
        self.check_for_enemy_collision()

    def draw(self):
        self.screen.fill(BLACK)
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        for enemy in self.level.enemies:
            enemy.draw(self.screen)
        for item in self.level.items:
            item.draw(self.screen)
        self.ui.draw(self.screen)

    def check_for_item_pickup(self):
        for item in self.level.items[:]:
            if item.x == self.player.x and item.y == self.player.y:
                self.player.pickup_item(item)
                self.level.items.remove(item)
                self.message_log.append(f"Picked up {item.item_type}")

    def check_for_enemy_collision(self):
        for enemy in self.level.enemies[:]:
            if enemy.x == self.player.x and enemy.y == self.player.y:
                damage_to_enemy = max(0, self.player.attack - enemy.defense)
                damage_to_player = max(0, enemy.attack - self.player.defense)

                enemy.hp -= damage_to_enemy
                self.player.hp -= damage_to_player

                self.message_log.append(f"Player deals {damage_to_enemy} damage to enemy")
                self.message_log.append(f"Enemy deals {damage_to_player} damage to player")

                if enemy.hp <= 0:
                    self.level.enemies.remove(enemy)
                    self.player.gain_xp(enemy.xp_value)
                    self.player.gold += enemy.gold_value
                    self.score += enemy.xp_value
                    self.message_log.append(f"Defeated enemy, gained {enemy.xp_value} XP and {enemy.gold_value} gold")

                if self.player.hp <= 0:
                    self.state = STATE_GAME_OVER

    def check_for_stairs(self):
        if (self.player.x, self.player.y) == self.level.stairs_pos:
            self.next_level()

    def next_level(self):
        self.level = Level(self.level.level_number + 1)
        self.player.x, self.player.y = self.level.rooms[0].center()
        self.message_log.append(f"Descended to level {self.level.level_number}")
        self.score += 100 * self.level.level_number
