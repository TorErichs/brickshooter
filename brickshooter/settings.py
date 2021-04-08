class Settings:
    """class used to store all the general settings of the game"""

    def __init__(self):
        """Set the standard settings"""

        """Screen/windows settings"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (52, 183, 235)
        self.max_fps = 60

        """"Gameplay settings"""
        self.sound = False
        self.start_bricks = 45
        self.min_bricks = 35

        """Game behavior"""
        # speed added when hitting the slider
        self.speed_increase = 0.05

        # starting speed factors
        self.slow_teleporters = 0.5
        self.slow_beach = 0.75

        # chances of special brick
        self.promille_duplicators: int = 10
        self.promille_teleporters: int = 10
        self.promille_beach: int = 5

        # percent of total speed change in horizontal component
        self.friction = 0.1

        """Highscore settings"""
        self.points_per_brick = 2
        self.points_per_reflection = 1
        self.points_per_lost_ball = -25
        self.point_every_x_ms = 10000

        """Developer options"""
        # Enables developer features for testing (auto bottom reflection)
        self.debug = False

        # allows to change starting speed and slider speed accordingly
        self.speed = 300 / self.max_fps

        # self.low_collision_limit = 1
