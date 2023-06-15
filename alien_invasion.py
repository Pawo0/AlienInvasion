import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self) -> None:
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Windowed version
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        # FullScreen version
        """
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        """

        # Create instance to store game statistics and create scoreboard
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        # Game title
        pygame.display.set_caption("Alien Invasion")

        # Initialize the ship
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Initialize the aliens' fleet
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # Make the Play button with lvl-s and set positions
        self.play_button_easy = Button(self, "Play easy")
        self.play_button_med = Button(self, "Play medium")
        self.play_button_hard = Button(self, "Play hard")

        self.play_button_med.prep_msg("Play medium")

        self.play_button_easy.rect.bottom = self.play_button_med.rect.top - 20
        self.play_button_easy.prep_msg("Play easy")

        self.play_button_hard.rect.top = self.play_button_med.rect.bottom + 20
        self.play_button_hard.prep_msg("Play hard")

    def run_game(self):
        """Start main loop for the game"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            # self.clock.tick(60)

    def _check_events(self):
        # Watch for keyboard or mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start new game when player clicks Play"""
        button_clicked_easy = self.play_button_easy.rect.collidepoint(mouse_pos)
        button_clicked_med = self.play_button_med.rect.collidepoint(mouse_pos)
        button_clicked_hard = self.play_button_hard.rect.collidepoint(mouse_pos)
        if button_clicked_easy and not self.game_active:
            self.settings.initialize_dynamic_settings_easy()
            self._start_game()
        if button_clicked_med and not self.game_active:
            self.settings.initialize_dynamic_settings_medium()
            self._start_game()
        if button_clicked_hard and not self.game_active:
            self.settings.initialize_dynamic_settings_hard()
            self._start_game()

    def _start_game(self):
        self.stats.reset_stats()
        self.game_active = True
        self.scoreboard.prep_score()
        self.scoreboard.prep_high_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()

        # Get rid of any remaining bullets and aliens
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship._center_ship()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to key press"""
        # Move a ship
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # Quit the game
        elif event.key == pygame.K_q:
            sys.exit()
        # Fire the bullets
        elif (
            event.key == pygame.K_SPACE or event.key == pygame.K_UP
        ) and self.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.settings.initialize_dynamic_settings_medium()
            self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullet group"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and delete old bullets"""
        # Update position
        self.bullets.update()

        # Delete old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for collision with aliens
        # and get rid (pozbyc) the bullet and the alien
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Check for collision and get rid bullet and alien. Then reset fleet"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.scoreboard.prep_score()
                # Check if there's new high score
                self.scoreboard.check_high_score()
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _update_aliens(self):
        """Check if alien is on edge and update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for alien hitting the bottom screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        # Show crash on the screen
        self._update_screen()

        if self.stats.ships_left > 0:
            # Decrement left ships, and update scoreboard
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Get rid any remaining bullets and aliens
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and center position of ship
            self._create_fleet()
            self.ship._center_ship()

            # Pause
            sleep(1)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and keep adding aliens until we reach right side
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Finished a row; reset x value and increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond if any alien have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_direction()
                break

    def _change_direction(self):
        """Drag the entire fleet and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information
        self.scoreboard.show_score()

        # Draw each bullet on screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button_easy.draw_button()
        if not self.game_active:
            self.play_button_med.draw_button()
        if not self.game_active:
            self.play_button_hard.draw_button()

        # Make most recently draw screen visible
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
