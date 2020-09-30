# -*- coding: utf-8 -*-

# pip install -r requirements.txt

from astrobox.space_field import SpaceField
# TODO - Переименуйте класс своего дрона по шаблону [Фамилия]Drone
from allaberdin import Spinozavr


if __name__ == '__main__':
    scene = SpaceField(
        speed=3,
        asteroids_count=5,
    )

    d = Spinozavr()
    scene.go()

# Первый этап: зачёт!
