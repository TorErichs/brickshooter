from pygame import image as pg_image
from pygame import error as pg_error
from pygame import font
from pprint import pprint

from os import path as os_path


def load_font(chosen_font=None, size=36):
    try:
        font_object = font.SysFont(chosen_font, size)
    except FileNotFoundError as message:
        print(message, "\n Reverting to standard font.")
        font_object = font.Font(None, size)
    return font_object


def load_png(name):
    """ Load image and return image object"""
    fullname = os_path.join("../images/", name)
    try:
        image = pg_image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pg_error as message:
        print("Cannot load image:", fullname)
        raise SystemExit(message)
    return image, image.get_rect()


if __name__ == "__main__":
    pprint(font.get_fonts())
    print(font.get_default_font())
