# Define the slider object that the player controls
import pygame
from typing import Tuple, List
from settings import Settings
from random import randint, choice
from handling import load_png
import math
import sounds

# copied from www.realpython.com/pygame-a-primer
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
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
        # load the external init settings
        self.settings = Settings()
        self.special = special
        # self.last_collision = 0

        # set the image and size
        if self.special == "Teleporter":
            self.image, self.rect = load_png("bball.png")
        elif self.special == "Beach":
            self.image, self.rect = load_png("beball.png")
        else:
            self.image, self.rect = load_png("ball.png")
        self.image.convert()

        # shrink the ball rect slightly to make ball behave less 'rectangly'
        self.resize_rect(0.95)
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
        elif direction is [0, 0]:
            self.start_direction = [0, 0]
        else:
            self.start_direction = direction

        self.speed = self.calculate_speed()
        # self.speed = [1.2, -0.1]
        # Tried random direction but is mostly boring. 45° seems to work best
        # self.speed = self.random_direction()
        # Set up the modulos to allow for floats
        self.rest_speed = [0.0, 0.0]

    def random_direction(self):
        x_speed = self.settings.speed * randint(10, 90) / 100
        y_speed = choice([-1, 1]) * math.sqrt(self.settings.speed ** 2 - x_speed ** 2)
        self.start_direction = [x_speed, y_speed]

    def calculate_speed(self):
        # exception for beach ball
        if self.start_direction == [0, 0]:
            self.random_direction()
        dir_len = math.sqrt(self.start_direction[0] ** 2 + self.start_direction[1] ** 2)
        x_speed = self.start_direction[0] / dir_len * self.settings.speed
        y_speed = self.start_direction[1] / dir_len * self.settings.speed
        if self.special == "Teleporter":
            speed = [
                x_speed * self.settings.slow_teleporters,
                y_speed * self.settings.slow_teleporters,
            ]
        elif self.special == "Beach":
            speed = [
                x_speed * self.settings.slow_beach,
                y_speed * self.settings.slow_beach,
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
        # self.last_collision += 1

    def out_of_bounds(self):
        """remove the ball if it leaves the screen"""
        if self.rect.centery > self.settings.screen_height:
            self.kill()
            sounds.play_sound("dropped_ball", self.settings.sound)
            Ball._total_balls += 1

    def side_reflection_teleporter(self):
        if self.rect.centerx < 0:
            self.rect.centerx = self.rect.centerx + self.settings.screen_width
            sounds.play_sound("hit_teleport", self.settings.sound)
        elif self.rect.centerx > self.settings.screen_width:
            self.rect.centerx = self.rect.centerx % self.settings.screen_width
            sounds.play_sound("hit_teleport", self.settings.sound)
        elif self.rect.top < 0:
            self.rect.bottom = self.settings.screen_height
            sounds.play_sound("hit_teleport", self.settings.sound)
        elif self.rect.bottom > self.settings.screen_height and self.settings.debug:
            self.speed[1] = -abs(self.speed[1])
            sounds.play_sound("hit_teleport", self.settings.sound)
        # self.last_collision = 0

    def side_reflection_beach(self):
        if self.rect.left < 0:
            if self.speed[0] > 0:
                pass
            elif self.speed[1] > 0:
                self.speed[0], self.speed[1] = (
                    abs(self.speed[1]),
                    abs(self.speed[0]),
                )
                self.rest_speed[0], self.rest_speed[1] = (
                    abs(self.rest_speed[1]),
                    abs(self.rest_speed[0]),
                )
            else:
                self.speed[0], self.speed[1] = (
                    abs(self.speed[1]),
                    -abs(self.speed[0]),
                )
                self.rest_speed[0], self.rest_speed[1] = (
                    abs(self.rest_speed[1]),
                    -abs(self.rest_speed[0]),
                )
        elif self.rect.right > self.settings.screen_width:
            if self.speed[0] < 0:
                pass
            elif self.speed[1] > 0:
                self.speed[0], self.speed[1] = (
                    -abs(self.speed[1]),
                    abs(self.speed[0]),
                )
                self.rest_speed[0], self.rest_speed[1] = (
                    -abs(self.rest_speed[1]),
                    abs(self.rest_speed[0]),
                )
            else:
                self.speed[0], self.speed[1] = (
                    -abs(self.speed[1]),
                    -abs(self.speed[0]),
                )
                self.rest_speed[0], self.rest_speed[1] = (
                    -abs(self.rest_speed[1]),
                    -abs(self.rest_speed[0]),
                )
        elif self.rect.top < 0:
            if self.speed[1] > 0:
                pass
            elif self.speed[0] > 0:
                self.speed[0], self.speed[1] = (
                    abs(self.speed[1]),
                    abs(self.speed[0]),
                )
                self.rest_speed[0], self.rest_speed[1] = (
                    abs(self.rest_speed[1]),
                    abs(self.rest_speed[0]),
                )
            else:
                self.speed[0], self.speed[1] = (
                    -abs(self.speed[1]),
                    abs(self.speed[0]),
                )
                self.rest_speed[0], self.rest_speed[1] = (
                    -abs(self.rest_speed[1]),
                    abs(self.rest_speed[0]),
                )
        elif self.rect.bottom > self.settings.screen_height and self.settings.debug:
            if self.speed[1] < 0:
                pass
            elif self.speed[0] > 0:
                self.speed[0], self.speed[1] = (
                    abs(self.speed[1]),
                    -abs(self.speed[0]),
                )
                self.rest_speed[0], self.rest_speed[1] = (
                    abs(self.rest_speed[1]),
                    -abs(self.rest_speed[0]),
                )
            else:
                self.rest_speed[0], self.rest_speed[1] = (
                    -abs(self.rest_speed[1]),
                    -abs(self.rest_speed[0]),
                )
        # self.last_collision = 0

    def side_reflection_normal(self):
        if self.rect.left < 0:
            self.speed[0] = abs(self.speed[0])
            self.rest_speed[0] = -self.rest_speed[0]
            sounds.play_sound("wall_hit", self.settings.sound)
        elif self.rect.right > self.settings.screen_width:
            self.speed[0] = -abs(self.speed[0])
            self.rest_speed[0] = -abs(self.rest_speed[0])
            sounds.play_sound("wall_hit", self.settings.sound)
        elif self.rect.top < 0:
            self.speed[1] = abs(self.speed[1])
            self.rest_speed[1] = abs(self.rest_speed[1])
            sounds.play_sound("wall_hit", self.settings.sound)
        elif self.rect.bottom > self.settings.screen_height and self.settings.debug:
            self.speed[1] = -abs(self.speed[1])
            sounds.play_sound("wall_hit", self.settings.sound)

        # self.last_collision = 0

    def side_collisions(self):
        """handles the direction changes when hitting sides
            Normal should work like a standard reflection
            Teleporter goes through the walls
        """
        # if # self.last_collision < self.settings.low_collision_limit:
        #    pass
        if self.special == "Teleporter":
            self.side_reflection_teleporter()
        elif self.special == "Beach":
            self.side_reflection_beach()
        else:  # if the rest is not also treated it can lead to sliding along walls
            self.side_reflection_normal()

    def slider_collision(self, slider, pressed_keys):
        """Only reflect from slider when moving down
            also speeds up the ball on each reflection
            and by friction adds removes speed and changes direction slightly"""
        if (
            pygame.sprite.spritecollideany(self, slider)
            # and # self.last_collision < self.settings.low_collision_limit
        ):
            if self.speed[1] > 0:
                if self.special == "Beach":
                    if self.speed[0] > 0:
                        self.speed[0], self.speed[1] = (
                            abs(self.speed[1]),
                            -abs(self.speed[0]),
                        )
                        sounds.play_sound("bounce", self.settings.sound)
                    else:
                        self.speed[0], self.speed[1] = (
                            -abs(self.speed[1]),
                            -abs(self.speed[0]),
                        )
                        sounds.play_sound("bounce", self.settings.sound)
                else:
                    self.speed[0] = self.speed[0] * (1 + self.settings.speed_increase)
                    self.speed[1] = -self.speed[1] * (1 + self.settings.speed_increase)
                    self.rest_speed[1] = -self.rest_speed[1]
                    Ball._slider_reflections += 1
                    sounds.play_sound("bounce", self.settings.sound)
                    if self.settings.friction:
                        total_speed = math.sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)
                        if pressed_keys[K_LEFT]:
                            self.speed[0] += self.settings.friction * total_speed
                        if pressed_keys[K_RIGHT]:
                            self.speed[0] += -self.settings.friction * total_speed
                # self.last_collision = 0

    def brick_collision(self, balls, bricks, all_sprites):
        if (
            pygame.sprite.spritecollideany(self, bricks)
            # and # self.last_collision < self.settings.low_collision_limit
        ):
            collided_brick = pygame.sprite.spritecollideany(self, bricks)

            # then remove the brick
            if collided_brick.special == "Teleporter":
                direction = self.speed[:]
                new_ball = Ball("Teleporter", direction)
                new_ball.rect.left, new_ball.rect.top = self.rect.left, self.rect.top
                balls.add(new_ball)
                all_sprites.add(new_ball)
                sounds.play_sound("brick_teleporter", self.settings.sound)
            elif collided_brick.special == "Duplicator":
                direction = self.speed[:]
                new_ball = Ball("Normal", direction)
                new_ball.rect.left, new_ball.rect.top = self.rect.left, self.rect.top
                balls.add(new_ball)
                all_sprites.add(new_ball)
                sounds.play_sound("brick_duplicator", self.settings.sound)
            elif collided_brick.special == "Beach":
                new_ball = Ball("Beach", [0, 0])
                new_ball.rect.left, new_ball.rect.top = self.rect.left, self.rect.top
                balls.add(new_ball)
                all_sprites.add(new_ball)
                sounds.play_sound("brick_beach", self.settings.sound)
            else:  # meant for collided_brick.special == "Normal":
                sounds.play_sound("brick_normal", self.settings.sound)
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
            Ball._destroyed_bricks += 1
            # self.last_collision = 0

    def update(self, balls, slider, bricks, all_sprites, pressed_keys):
        self.float_move_ip()
        # self.rect.move_ip(self.speed)
        # screen side collisions
        self.side_collisions()

        # simple slider collision
        self.slider_collision(slider, pressed_keys)

        # brick collision
        self.brick_collision(balls, bricks, all_sprites)

        # Check if ball left screen and remove if case
        self.out_of_bounds()


class Brick(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super(Brick, self).__init__()
        self.settings = Settings()

        # Set the attribute self.special
        self.special = "Normal"
        self.decide_type()

        # Set the image dependent of type
        self.set_image()

        # Add the collision rect
        self.rect = self.image.get_rect()

        # Set random open(!) position
        self.set_rand_position(all_sprites)

    def decide_type(self):
        """subroutine of __init__ setting the brick type by chance"""

        rand_type_decision = randint(1, 1000)
        if rand_type_decision <= self.settings.promille_duplicators:
            self.special = "Duplicator"
        elif rand_type_decision <= (
            self.settings.promille_duplicators + self.settings.promille_teleporters
        ):
            self.special = "Teleporter"
        elif rand_type_decision <= (
            self.settings.promille_duplicators
            + self.settings.promille_teleporters
            + self.settings.promille_beach
        ):
            self.special = "Beach"
        else:
            pass

    def set_image(self):
        """subroutine of __init__:
           depending on the brick type sets the right image
           """
        if self.special == "Normal":
            brick_image = choice(
                [
                    "brick1.png",
                    "brick2.png",
                    "brick3.png",
                    "brick4.png",
                    # "brick_bright.png",
                    # "brick_gray.png",
                    # "brick_green.png",
                ]
            )
        elif self.special == "Duplicator":
            brick_image = "brick_blue.png"
        elif self.special == "Teleporter":
            brick_image = "brick_red.png"
        elif self.special == "Beach":
            brick_image = "brick_yellow.png"
        else:  # Should not happen
            brick_image = "brick_gray.png"

        self.path_bricks: str = f"../images/{brick_image}"
        self.image = pygame.image.load(self.path_bricks)
        self.image = pygame.transform.scale(self.image, (100, 50)).convert()

    def set_rand_position(self, all_sprites):
        """
        Tries different positions for the new brick that are not blocked by other
        objects (alL_sprites);
        Additional runaway loop prevention added for possible future functions,
        that could fill the screen more
        """
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
