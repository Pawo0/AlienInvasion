import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Creating bullet at the ship's positions"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create bullet at (0,0) and moving it on ship's top
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store bullet y position in float
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""
        # Update float position of bullet
        self.y -= self.settings.bullet_speed
        # Update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
