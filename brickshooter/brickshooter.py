# Define the slider object that the player controls
import pygame
from settings import Settings
from random import randint, choice
from handling import load_png

# copied from www.realpython.com/pygame-a-primer
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Slider(pygame.sprite.Sprite):
    def __init__(self):
        super(Slider, self).__init__()
        self.image = pygame.Surface((120, 20))
        self.image.fill((122, 122, 122))
        self.rect = self.image.get_rect()
        self.settings = Settings()
        self.rect.move_ip(
            0.5 * self.settings.screen_width, 0.95 * self.settings.screen_height
        )

    def update(self, pressed_keys):
        """ Calculates the new position, but doesn't allow movement past the sides"""
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

        # Adding the screen limits for the slider
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right >= self.settings.screen_width:
            self.rect.right = self.settings.screen_width


class Ball(pygame.sprite.Sprite):
    """A ball that moves across the screen and for the moment start at a random position in the center of the screen
     Returns: ball object
     Functions: update
     Attributes: speed"""

    # [ball functions (methods) here] TODO: documentation also for other classes
    # [e.g. a function to calculate new position]
    # [and a function to check if it hits the side]

    number_of_balls = 0  # class variable

    def __init__(self):
        super(Ball, self).__init__()

        # tracking the active number of balls  TODO: maybe change to an iterable list?
        Ball.number_of_balls += 1

        # set the image and size
        self.image, self.rect = load_png("ball.png")

        # Starting position somewhere in the upper center of the screen
        self.settings = Settings()
        rand_x = randint(
            self.settings.screen_width / 4, 3 / 4 * self.settings.screen_width
        )
        rand_y = randint(0, self.settings.screen_height / 2)
        self.rect.move_ip(rand_x, rand_y)

        self.speed = [1, -1]

    def update(self, slider_obj, brick_list):
        self.rect.move_ip(self.speed)
        # screen side collisions
        if self.rect.left < 0 or self.rect.right > self.settings.screen_width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0:  # or self.rect.bottom > self.settings.screen_height:
            self.speed[1] = -self.speed[1]

        # slider collision
        if int(self.rect.bottom) == int(slider_obj.rect.top) and (
            (self.rect.left + self.rect.width / 2) > slider_obj.rect.left
            and (self.rect.right - self.rect.width / 2) < slider_obj.rect.right
        ):  # TODO Randtreffer reparieren (doppelte Reflection?)
            self.speed[1] = -self.speed[1]

        # brick collision
        for brick in brick_list:
            pass

        # loss condition if ball leaves screen TODO: What about multiple balls
        if self.rect.top > self.settings.screen_height:
            self.kill()

        # TODO Vergleich mit math.isclose() lösen?


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        super(Brick, self).__init__()
        brick_image = choice(
            ["brick1.png", "brick2.png", "brick3.png", "brick4.png"]
        )  # TODO: Change to the load function when final size is clear
        self.path_bricks: str = f"../images/{brick_image}"
        self.image = pygame.image.load(self.path_bricks)  # .convert()
        self.image = pygame.transform.scale(self.image, (100, 50)).convert()
        self.rect = self.image.get_rect()
        self.settings = Settings()


if __name__ == "__main__":
    print("Your executing the package test area.")
