# -*- coding: utf-8 -*-
import random

from astrobox.core import Drone


class AllaberdinDrone(Drone):

    def on_born(self):
        self.target = random.choice(self.asteroids)
        self.move_at(self.target)

    def on_stop_at_asteroid(self, asteroid):
        self.load_from(asteroid)

    def on_overlap_with(self, obj_status):
        if obj_status in self.teammates:
            if 300 < self.distance_to(self.mothership):
                if self.is_empty and obj_status.is_full:
                    self.move_at(obj_status)
                    obj_status.move_at(self)
                    self.load_from(obj_status)
                    # TODO решить проблему с бесконечным обменом между дронами

    def on_load_complete(self):
        self.find_closest()
        if not self.is_full:
            if self.distance_to(self.target) < self.distance_to(self.my_mothership):
                self.move_at(self.target)
                return
        self.move_at(self.my_mothership)

    def on_stop_at_mothership(self, mothership):
        self.unload_to(mothership)

    def on_unload_complete(self):
        self.find_closest()
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
                        return
        self.target = self.mothership
