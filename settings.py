class Settings:
    """A Class to store all settings for game"""

    def __init__(self) -> None:
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship setting
        self.ship_life_limit = 3

        # Bullet setting
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # Alien bullet setting
        self.a_bullet_width = 3
        self.a_bullet_height = 15
        self.a_bullet_color = (255, 0, 0)
        self.a_bullet_speed = 3.0
        # Probability to shot in scale 1/x
        self.prob_to_shot = 1000

        # Alien setting
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

    def initialize_dynamic_settings_easy(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 3.5
        self.bullet_speed = 5.0
        self.alien_speed = 1.0
        self.difficulty_mult = 1

        self._universal_dynamic_settings()

    def initialize_dynamic_settings_medium(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 3.5
        self.bullet_speed = 5.0
        self.alien_speed = 1.5
        self.difficulty_mult = 1.2

        self._universal_dynamic_settings()

    def initialize_dynamic_settings_hard(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 3.5
        self.bullet_speed = 5.0
        self.alien_speed = 2
        self.difficulty_mult = 1.5

        self._universal_dynamic_settings()

    def _universal_dynamic_settings(self):
        """Initialize settings that show up in every difficulty level"""
        # fleet direction; 1 = right ; -1 = left
        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        """Increase speed and points settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
