class Settings:
    def __init__(self):
        self.screen_width=1200
        self.screen_height=800
        self.bg_color = (230,230,230)
        self.ship_limit=3
        self.fleet_drop_speed=10
        self.bullet_width=100
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.bullets_allowed=100
        self.speedup_scale=1.1
        self.score_scale=1.5
        self.difficulty = 'medium'
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        self.fleet_direction=1
        self.set_difficulty(self.difficulty)
        self.alien_points=50
    def increase_speed(self):
        self.ship_speed *=self.speedup_scale
        self.bullet_speed *=self.speedup_scale
        self.alien_speed *=self.speedup_scale
        self.alien_points = int(self.alien_points*self.score_scale)
    def set_difficulty(self,level):
        if level == 'easy':
            self.ship_speed = 5
            self.bullet_speed = 6
            self.alien_speed = 2
        elif level == 'medium':
            self.ship_speed=4
            self.bullet_speed=5
            self.alien_speed=4
        elif level == 'hard':
            self.ship_speed=4
            self.bullet_speed=5
            self.alien_speed=7