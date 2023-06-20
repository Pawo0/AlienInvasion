import pygame
from pygame.sprite import Sprite

from settings import Settings


class AlienBullet(Sprite):
    """Class to manage bullets from aliens"""

    def __init__(self, ai_game, alien):
        """Creating bullet on alien position"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = Settings()
        self.color = self.settings.a_bullet_color

        # Create a bullet at (0,0) and move it on mid bottom of alien
        self.rect = pygame.Rect(
            0, 0, self.settings.a_bullet_width, self.settings.a_bullet_height
        )
        self.rect.midbottom = alien.rect.midbottom

        # Store decimal y position of bullet
        self.y = self.rect.y

    def update(self):
        """Move bullet down the screen"""
        # Increment y value about bullet speed
        self.y += self.settings.a_bullet_speed
        # Update rect position
        self.rect.y = self.y

    def draw_a_bullet(self):
        """Draw alien's bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
