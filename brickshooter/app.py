#!/usr/bin/env python  TODO: change completely
#
# The non-ultimate brick shooter
# A first pygame project to practice object oriented programming
# PUT URL HERE?
#
# Released under the GNU General Public License

VERSION = "0.1"

try:
    from settings import Settings
    import sys
    import pygame
    from brickshooter import Slider, Ball, Brick

    # copied from www.realpython.com/pygame-a-primer
    # Import pygame.locals for easier access to key coordinates
    # Updated to conform to flake8 and black standards
    from pygame.locals import (
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        K_p,
        K_PAUSE,
        KEYDOWN,
        QUIT,
    )
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)


class BrickShooter:
    """The main game class to manage the game"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()
        self.running = True
        self.pause = False
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("The non-ultimate brick shooter (TNUBS)")

        # set background
        self.bg_color = (52, 183, 235)  # TODO nice color scheme

        # initiate objects
        self.slider = Slider()
        self.first_ball = Ball()
        self.brick_list = [Brick() for _ in range(0, 1)]

        # initiate sprite groups
        self.balls = pygame.sprite.Group()
        self.sliders = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # Add the starting objects to the groups
        self.balls.add(self.first_ball)
        self.all_sprites.add(self.first_ball)
        self.sliders.add(self.slider)
        self.all_sprites.add(self.slider)
        self.bricks.add(self.brick_list[0])
        self.all_sprites.add(self.brick_list[0])

    def add_bricks(self):
        pass

    def run_game(self):
        """Start the main loop of the game"""
        while self.running:
            # Checks for keyboard input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # checking for key input
                elif event.type == pygame.locals.KEYDOWN:
                    # stop game with 'ESC'
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_p:  # Change pause flag
                        self.pause = not self.pause

            if (
                self.pause
            ):  # Combined with above gives the change to pause the game for a moment (or demonstration)
                continue  # TODO: find more elegant solution (add delay or sleep)

            # Creates a dict with key and bool (is pressed?) for the keyboard
            pressed_keys = pygame.key.get_pressed()

            # reacts to the keyboard and changes position of slider
            self.slider.update(pressed_keys)

            # moves the balls
            if (
                self.running
            ):  # TODO: Define different loss behavior than just close window

                for ball in self.balls:
                    ball.update(self.slider, self.brick_list)
                if not len(self.balls):
                    self.running = False

            # updates the screen for every iteration
            self.screen.fill(self.settings.bg_color)

            # Print all sprites onto the screen
            for entity in self.all_sprites:
                self.screen.blit(entity.image, entity.rect)

            # prints the current game situation
            pygame.display.flip()
        # TODO exit text oder so


if __name__ == "__main__":
    # Starts the game and runs an instance
    tnups = BrickShooter()
    tnups.run_game()
