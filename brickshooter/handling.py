from pygame import image as pg_image
from pygame import error as pg_error

from os import path as os_path


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
