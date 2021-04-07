# Define the slider object that the player controls
import pygame
from typing import Tuple, List
from settings import Settings
from random import randint, choice
from handling import load_png
import math

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
        # give the slider less height for collisions:
        self.rect.height = 2
        self.settings = Settings()
        self.rect.move_ip(
            0.5 * self.settings.screen_width, 0.95 * self.settings.screen_height
        )

    def update(self, pressed_keys):
        """ Calculates the new position, but doesn't allow movement past the sides"""
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2 * self.settings.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2 * self.settings.speed, 0)

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

    # Class variables
    _destroyed_bricks: int = 0
    _slider_reflections: int = 0
    _total_balls: int = 0

    def __init__(self, special="Normal", direction=None):
        super(Ball, self).__init__()
        if direction is None:
            self.start_direction = [1, -1]
        else:
            self.start_direction = direction
        self.special = special

        # set the image and size
        if self.special == "Teleporter":
            self.image, self.rect = load_png("bball.png")
        else:
            self.image, self.rect = load_png("ball.png")
        self.image.convert()

        self.resize_rect(
            0.90
        )  # shrink the ball rect slightly to make ball behave less 'rectangly'

        self.settings = Settings()

        # Starting position somewhere in the upper center of the screen
        # self.rand_start_pos()

        # Starting position close to slider
        self.rect.move_ip(
            0.5 * self.settings.screen_width,
            0.95 * self.settings.screen_height - self.rect.height / 0.9,
        )

        # always start with upward speed and make sure that speed has an angle
        if direction is None:
            self.start_direction = [choice([-1, 1]), -1]
        else:
            self.start_direction = direction
        self.speed = self.calculate_speed()
        # self.speed = [1.2, -0.1]
        # Tried random direction but is mostly boring. 45° seems to work best
        # self.speed = self.random_direction()
        # Set up the modulos to allow for floats
        self.rest_speed = [0.0, 0.0]

    def random_direction(self):
        x_speed = randint(1, int(self.settings.speed - 2))
        y_speed = -math.sqrt(self.settings.speed ** 2 - x_speed ** 2)
        speed = [x_speed, y_speed]
        return speed

    def calculate_speed(self):
        dir_len = math.sqrt(self.start_direction[0] ** 2 + self.start_direction[1] ** 2)
        x_speed = self.start_direction[0] / math.sqrt(dir_len) * self.settings.speed
        y_speed = self.start_direction[1] / math.sqrt(dir_len) * self.settings.speed
        if self.special == "Teleporter":
            speed = [
                x_speed * self.settings.slow_teleporters,
                y_speed * self.settings.slow_teleporters,
            ]
        else:
            speed = [x_speed, y_speed]
        return speed

    def resize_rect(self, factor):
        """function to make the collision area of the ball slightly smaller,
            suggested on the internet for non-square objects
            for more realistic collision look
            """
        tmp_centerx = self.rect.centerx
        tmp_centery = self.rect.centery
        self.rect.width = factor * self.rect.width
        self.rect.height = factor * self.rect.height
        self.rect.centerx = tmp_centerx
        self.rect.centery = tmp_centery

    def rand_start_pos(self):
        """generate and set random start position at more at the center of upper half of screen"""
        rand_x = randint(
            self.settings.screen_width / 4, 3 / 4 * self.settings.screen_width
        )
        rand_y = randint(0, self.settings.screen_height / 2)
        self.rect.move_ip(rand_x, rand_y)

    def float_move_ip(self):  # TODO: Add try/except
        """Add up the non-full pixels so they get executed at some point"""
        tmp_speed = [0, 0]
        for i in [0, 1]:
            tmp_speed[i] = self.speed[i] + self.rest_speed[i]
            if tmp_speed[i] > 0:
                self.rest_speed[i] = tmp_speed[i] % 1.0
            else:
                self.rest_speed[i] = -(abs(tmp_speed[i]) % 1.0)
        self.rect.move_ip(tmp_speed)

    def out_of_bounds(self):
        """remove the ball if it leaves the screen and still moving down"""
        if self.rect.centery > self.settings.screen_height and self.speed[1] > 0:
            self.kill()
            self._total_balls += 1

    def side_collisions(self):
        """handles the direction changes when hitting sides
            Normal should work like a standard reflection
            Teleporter goes through the walls
        """
        if self.special == "Teleporter":
            if self.rect.centerx < 0:
                self.rect.centerx = self.rect.centerx + self.settings.screen_width
            elif self.rect.centerx > self.settings.screen_width:
                self.rect.centerx = self.rect.centerx % self.settings.screen_width
            elif self.rect.top < 0:
                self.rect.bottom = self.settings.screen_height
            elif self.rect.bottom > self.settings.screen_height and self.settings.debug:
                self.speed[1] = -abs(self.speed[1])
        else:  # if the rest is not also treated it can lead to sliding along walls
            if self.rect.left < 0:
                self.speed[0] = abs(self.speed[0])
                self.rest_speed[0] = -self.rest_speed[0]
            elif self.rect.right > self.settings.screen_width:
                self.speed[0] = -abs(self.speed[0])
                self.rest_speed[0] = -abs(self.rest_speed[0])
            elif self.rect.top < 0:
                self.speed[1] = abs(self.speed[1])
                self.rest_speed[1] = abs(self.rest_speed[1])
            elif self.rect.bottom > self.settings.screen_height and self.settings.debug:
                self.speed[1] = -abs(self.speed[1])
                self.rest_speed[1] = -abs(self.rest_speed[1])

    def slider_collision(self, slider):
        """Only reflect from slider when moving down
            also speeds up the ball on each reflection"""
        if pygame.sprite.spritecollideany(self, slider):
            if self.speed[1] > 0:
                self.speed[0] = self.speed[0] * (1 + self.settings.speed_increase)
                self.speed[1] = -self.speed[1] * (1 + self.settings.speed_increase)
                self.rest_speed[1] = -self.rest_speed[1]
                self._slider_reflections += 1

    def brick_collision(self, balls, bricks, all_sprites):
        if pygame.sprite.spritecollideany(self, bricks):
            collided_brick = pygame.sprite.spritecollideany(self, bricks)

            # then remove the brick
            if collided_brick.special == "Teleporter":
                tmp_speed_x, tmp_speed_y = self.speed
                new_ball = Ball("Teleporter", [tmp_speed_x, tmp_speed_y])
                new_ball.rect.left, new_ball.rect.top = self.rect.left, self.rect.top
                balls.add(new_ball)
                all_sprites.add(new_ball)
            elif collided_brick.special == "Duplicator":
                tmp_speed_x, tmp_speed_y = self.speed
                new_ball = Ball("Normal", [tmp_speed_x, tmp_speed_y])
                new_ball.rect.left, new_ball.rect.top = self.rect.left, self.rect.top
                balls.add(new_ball)
                all_sprites.add(new_ball)
            else:  # meant for collided_brick.special == "Normal":
                pass
            dx = self.rect.centerx - collided_brick.rect.centerx
            # if the ball doesn't hit within the central part of the length it reflects on the side
            # give speed tolerance otherwise it would lead to worse side reflection
            if (
                abs(dx) + abs(self.speed[0]) + 2
                > 1 * collided_brick.rect.width / 2 + self.rect.width / 2
            ):
                self.speed[0] = -self.speed[0]
                self.rest_speed[0] = -self.rest_speed[0]
            else:
                self.speed[1] = -self.speed[1]
                self.rest_speed[1] = -self.rest_speed[1]
            collided_brick.kill()
            self._destroyed_bricks += 1

    def update(self, balls, slider, bricks, all_sprites):
        self.float_move_ip()
        # self.rect.move_ip(self.speed)
        # screen side collisions
        self.side_collisions()

        # simple slider collision
        self.slider_collision(slider)

        # brick collision
        self.brick_collision(balls, bricks, all_sprites)

        # Check if ball left screen and remove if case
        self.out_of_bounds()


class Brick(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super(Brick, self).__init__()
        self.settings = Settings()
        rand_type_decision = randint(0, 100)
        if rand_type_decision < self.settings.percent_duplicators:
            self.special = "Duplicator"
        elif rand_type_decision < (
            self.settings.percent_duplicators + self.settings.percent_teleporters
        ):
            self.special = "Teleporter"
        else:
            self.special = "Normal"

        if self.special == "Normal":
            brick_image = choice(
                [
                    "brick1.png",
                    "brick2.png",
                    "brick3.png",
                    "brick4.png",
                    # "brick_blue.png",
                    # "brick_bright.png",
                    # "brick_gray.png",
                    # "brick_green.png",
                    # "brick_red.png",
                ]
            )  # TODO: Change to the load function when final size is clear
        elif self.special == "Duplicator":
            brick_image = "brick_blue.png"
        elif self.special == "Teleporter":
            brick_image = "brick_red.png"

        self.path_bricks: str = f"../images/{brick_image}"
        self.image = pygame.image.load(self.path_bricks)  # .convert()
        self.image = pygame.transform.scale(self.image, (100, 50)).convert()
        self.rect = self.image.get_rect()

        # Add the brick at a random position if that doesn't with any other sprite
        collision = True
        # only try 10 times to stop runaway loop
        n = 0
        while collision or n < 10:
            rand_x = randint(0, self.settings.screen_width - self.rect.width)
            rand_y = randint(0, int(2 * self.settings.screen_height / 3))
            self.rect.left = rand_x
            self.rect.top = rand_y
            collision = pygame.sprite.spritecollideany(self, all_sprites)
            n += 1
        if n >= 10:  # TODO: This won't work because can't be added in main...
            self.kill()


if __name__ == "__main__":
    print("Your executing the package test area.")
