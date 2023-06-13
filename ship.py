import pygame


class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game) -> None:
        """Initialize the ship and set its starting point"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # Start each ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store decimal value for ship's vertical position
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Updating the ship's position based on the movement flag"""
        # Update the ship's x value, bot rect
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed
        # Update rect from x position
        self.rect.x = self.x

        # Check if is too far, if is set horizontal on edge
        if self.rect.right > self.screen_rect.right:
            self.rect.right = self.screen_rect.right
            self.x = self.rect.x
        if self.rect.left < self.screen_rect.left:
            self.rect.left = self.screen_rect.left
            self.x = self.rect.x

    def _center_ship(self):
        """Center ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw a ship at its current location"""
        self.screen.blit(self.image, self.rect)
