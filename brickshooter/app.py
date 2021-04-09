#!/usr/bin/env python
#
# The non-ultimate brick shooter
# A first pygame project to practice object oriented programming
# https://github.com/TorErichs/brickshooter
#
# Released under the GNU General Public License

VERSION = "0.5"

try:
    from settings import Settings
    import sys
    import pygame
    from brickshooter import Slider, Ball, Brick
    from handling import load_font
    import sounds

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
        K_SPACE,
    )
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)


class BrickShooter:
    """The main game class to manage the game"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()
        pygame.mixer.init()
        self.running = True
        self.last_loop = False
        self.pause = False
        self.started = False
        self.settings = Settings()

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("The non-ultimate brick shooter (TNUBS)")

        # set background
        self.bg_color = (52, 183, 235)

        # initiate objects
        self.slider = Slider()

        # initiate sprite groups
        self.balls = pygame.sprite.Group()
        self.sliders = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # Add the starting objects to the groups
        self.balls.add(Ball("Starter"))  # First ball is started with a special argument
        for ball in self.balls:
            self.all_sprites.add(ball)
        self.sliders.add(self.slider)
        self.all_sprites.add(self.slider)
        while len(self.bricks) < self.settings.start_bricks:
            new_brick = Brick(self.all_sprites)
            self.bricks.add(new_brick)
            self.all_sprites.add(new_brick)

    def calculate_highscore(self):
        points = int(
            self.settings.points_per_brick * Ball._destroyed_bricks
            + self.settings.points_per_lost_ball * Ball._total_balls
            + self.settings.points_per_reflection * Ball._slider_reflections
            + pygame.time.get_ticks() // self.settings.point_every_x_ms
        )
        return points

    def start_of_game(self):
        font = load_font("comicsansms", 60)
        # font = pygame.font.SysFont("arial", 36)
        text = font.render(f"Welcome! Press SPACE to start.", 1, (0, 150, 0))
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().centerx
        textpos.centery = 0.8 * self.settings.screen_height
        self.screen.blit(text, textpos)

    def paused(self):
        """print paused state on screen
            suppressed in debug mode to make screenshots without
            """
        if not self.settings.debug:
            font = load_font("comicsansms", 80)
            # font = pygame.font.SysFont("arial", 36)
            text = font.render(f"PAUSED! 'p' to continue...", 1, (255, 0, 0))
            textpos = text.get_rect()
            textpos.centerx = self.screen.get_rect().centerx
            textpos.centery = 0.8 * self.settings.screen_height
            self.screen.blit(text, textpos)

    def print_score(self):
        points = self.calculate_highscore()
        font = load_font("comicsansms", 32)
        # font = pygame.font.SysFont("arial", 36)
        text = font.render(f"current score: {str(points)}", 1, (0, 150, 0))
        textpos = text.get_rect()
        textpos.bottomright = self.screen.get_rect().bottomright
        self.screen.blit(text, textpos)

    def print_fps(self, show=False):
        font = load_font("century", 24)
        # font = pygame.font.SysFont("arial", 36)
        text = font.render(str(round(self.clock.get_fps(), 2)), 1, (255, 0, 255))
        textpos = text.get_rect()
        textpos.topright = self.screen.get_rect().topright
        self.screen.blit(text, textpos)

    def end_of_game(self):
        sounds.play_sound("lost", self.settings.sound)

        # Print highscore
        points = self.calculate_highscore()
        font = load_font("comicsansms", 60)
        # font = pygame.font.SysFont("arial", 36)
        text = font.render(f"Your score: {str(points)}", 1, (0, 150, 0))
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().centerx
        textpos.centery = 0.8 * self.settings.screen_height
        self.screen.blit(text, textpos)

        # Print game stats
        font = load_font("comicsansms", 24)
        # TODO: getter function
        text = font.render(
            f"Destroyed bricks: {str(Ball._destroyed_bricks)}, total reflections: {str(Ball._destroyed_bricks)}, total balls: {str(Ball._total_balls)} ",
            1,
            (10, 10, 10),
        )
        textpos = text.get_rect()
        textpos.bottomleft = self.screen.get_rect().bottomleft
        self.screen.blit(text, textpos)

        # Refresh one last time
        pygame.display.flip()

        # wait for user to close
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.locals.KEYDOWN:
                    # stop game with 'ESC'
                    if event.key == K_ESCAPE:
                        sys.exit()
            pygame.time.wait(200)

    def refresh_balls(self, pressed_keys):
        """Ball update handling"""
        for ball in self.balls:
            ball.update(
                self.balls, self.sliders, self.bricks, self.all_sprites, pressed_keys,
            )
        if not len(self.balls):
            self.running = False
        if len(self.bricks) < self.settings.min_bricks:
            new_brick = Brick(self.all_sprites)
            self.bricks.add(new_brick)
            self.all_sprites.add(new_brick)

    def run_game(self):
        """Start the main loop of the game"""
        while self.running and self.last_loop == False:
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
                    if event.key == K_SPACE:
                        self.started = True

            # Creates a dict with key and bool (is pressed?) for the keyboard
            pressed_keys = pygame.key.get_pressed()

            # reacts to the keyboard and changes position of slider
            self.slider.update(pressed_keys)

            # moves the balls
            if self.running and self.started and not self.pause:
                self.refresh_balls(pressed_keys)

            # updates the screen for every iteration
            self.screen.fill(self.settings.bg_color)

            # change background on last loop
            if not self.running:
                self.last_loop = True
                self.screen.fill((156, 26, 26))

            # Print all sprites onto the screen
            for entity in self.all_sprites:
                self.screen.blit(entity.image, entity.rect)

            # Current score
            self.print_score()

            # prints the fps
            self.print_fps(self.settings.print_fps)

            # print starting instructions
            if not self.started:
                pygame.time.wait(100)
                self.start_of_game()

            # allows the game to be paused
            if self.pause:
                self.paused()
                pygame.time.wait(100)

            # prints the current game situation
            pygame.display.flip()

            # self.highscore = self.calculate_highscore()
            # delays the game to have a constant frame rate
            # print(self.clock.get_rawtime())
            self.clock.tick(self.settings.max_fps)

        # Only execute if game was lost and not on user exit
        if not len(self.balls):
            self.end_of_game()


if __name__ == "__main__":
    # Starts the game and runs an instance
    tnups = BrickShooter()
    tnups.run_game()
