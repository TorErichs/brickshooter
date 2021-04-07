class Settings:
    """class used to store all the general settings of the game"""

    def __init__(self):
        """Set the standard settings"""
        # For the screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (52, 183, 235)
        self.max_fps = 60
        # game settings
        self.start_bricks = 20
        self.min_bricks = 15
        # Developer options
        self.debug = False  # Enables features like auto bottom reflection
        self.speed = (
            300 / self.max_fps
        )  # allows to change starting speed and slider speed accordingly
        self.speed_increase = 0.05
        self.slow_teleporters = 0.1
        self.percent_duplicators = 2
        self.percent_teleporters = 2
