# -*- coding: utf-8 -*-

# pip install -r requirements.txt

from astrobox.space_field import SpaceField
from allaberdin import AllaberdinDrone
from stage_03_harvesters.driller import DrillerDrone


NUMBER_OF_DRONES = 5


if __name__ == '__main__':
    scene = SpaceField(
        speed=5,
        asteroids_count=20,
    )

    my_drones = [AllaberdinDrone() for _ in range(NUMBER_OF_DRONES)]
    enemy_drones = [DrillerDrone() for _ in range(NUMBER_OF_DRONES)]
    scene.go()

# Первый этап: зачёт!
# Второй этап: зачёт!
