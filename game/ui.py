import pygame


class UI:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        # Draw player stats
        hp_text = self.font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, (255, 255, 255))
        mp_text = self.font.render(f"MP: {self.player.mp}/{self.player.max_mp}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.player.level}", True, (255, 255, 255))
        xp_text = self.font.render(f"XP: {self.player.xp}/{100 * self.player.level}", True, (255, 255, 255))
        gold_text = self.font.render(f"Gold: {self.player.gold}", True, (255, 255, 255))

        screen.blit(hp_text, (10, 10))
        screen.blit(mp_text, (10, 40))
        screen.blit(level_text, (10, 70))
        screen.blit(xp_text, (10, 100))
        screen.blit(gold_text, (10, 130))

        # Draw inventory
        inventory_text = self.font.render("Inventory:", True, (255, 255, 255))
        screen.blit(inventory_text, (10, 160))
        for i, item in enumerate(self.player.inventory):
            item_text = self.font.render(f"- {item.item_type}", True, (255, 255, 255))
            screen.blit(item_text, (20, 190 + i * 30))
            if item == self.player.equipped_item:
                equipped_text = self.font.render("(E)", True, (255, 255, 0))
                screen.blit(equipped_text, (150, 190 + i * 30))
