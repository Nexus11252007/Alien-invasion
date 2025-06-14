class Settings:
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width=1200
        self.screen_height=600
        self.bg_color=(230,230,230)
        #Ship settings
        self.ship_limit=3
        #Bullet settings
        self.bullet_height=18
        self.bullet_width=5
        self.bullet_color=(60,60,60)
        self.bullet_allowed=3
        #Alien settings
        self.fleet_drop_speed=20
        

        # How quickly the game speeds up
        self.speed_up_scale=1.5

        # How quickly the alien point values increase
        self.score_scale=1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):

        self.ship_speed=1.0
        self.bullet_speed=1.5
        self.alien_speed=0.3
        
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction=1

        # Scoring
        self.alien_points=50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed*=self.speed_up_scale
        self.bullet_speed*=self.speed_up_scale
        self.alien_speed*=self.speed_up_scale

        self.alien_points=int(self.alien_points*self.score_scale)