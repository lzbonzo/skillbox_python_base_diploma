# -*- coding: utf-8 -*-

# pip install -r requirements.txt

from astrobox.space_field import SpaceField
from allaberdin import Spinozavr


if __name__ == '__main__':
    scene = SpaceField(
        speed=10,
        asteroids_count=5,
    )
    d = Spinozavr()
    scene.go()

