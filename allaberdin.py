# -*- coding: utf-8 -*-
from astrobox.core import Drone


class AllaberdinDrone(Drone):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_born(self):
        self.find_next()
        self.move_at(self.target)

    def on_stop_at_asteroid(self, asteroid):
        self.turn_to(self.mothership)
        self.load_from(asteroid)

    def on_load_complete(self):
        self.find_next()
        self.move_at(self.target)

    def on_stop_at_mothership(self, mothership):
        self.turn_to(45)
        self.unload_to(mothership)

    def on_unload_complete(self):
        self.find_next()
        self.move_at(self.target)

    def find_next(self):
        """
        Находит следующий пункт назначения
        """
        targets = [drone.target for drone in self.teammates if drone.target is not None]
        asteroids = [asteroid for asteroid in self.asteroids if asteroid not in targets and not asteroid.is_empty]
        if asteroids:
            asteroids = sorted(asteroids, key=lambda x: x.distance_to(self))
            if not self.is_full:
                self.target = asteroids[0]
                return
        if not self.near(self.mothership):
            self.target = self.mothership
