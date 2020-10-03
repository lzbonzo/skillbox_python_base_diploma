# -*- coding: utf-8 -*-
import random

from astrobox.core import Drone


class AllaberdinDrone(Drone):

    def on_born(self):
        self.available_asteroids = self.asteroids
        self.target = random.choice(self.asteroids)
        self.move_at(self.target)

    def on_stop_at_asteroid(self, asteroid):
        self.load_from(asteroid)

    def on_load_complete(self):
        if not self.is_full:
            next_asteroid = self.find_closest()
            if next_asteroid:
                if self.distance_to(next_asteroid) < self.distance_to(self.my_mothership):
                    self.move_at(next_asteroid)
                    return
        self.move_at(self.my_mothership)

    def on_stop_at_mothership(self, mothership):
        self.unload_to(mothership)

    def on_unload_complete(self):
        next_asteroid = self.find_closest()
        if next_asteroid:
            self.target = next_asteroid
            self.move_at(self.target)

    def find_closest(self):
        """
        Находит ближайший не пустой астреоид
        """
        distances = sorted(self.distance_to(ast) for ast in self.asteroids)
        targets = [drone.target for drone in self.teammates]
        for i in range(len(distances)):
            for asteroid in self.asteroids:
                if self.distance_to(asteroid) == distances[i] and not asteroid.is_empty:
                        if asteroid not in targets:
                            self.target = asteroid
                            return asteroid
