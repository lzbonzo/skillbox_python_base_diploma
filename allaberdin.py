# -*- coding: utf-8 -*-
from astrobox.core import Drone


class Spinozavr(Drone):

    def on_born(self):
        #  TODO Начинать должен с ближайшего
        self.move_at(self.asteroids[0])

    def on_stop_at_asteroid(self, asteroid):
        self.load_from(asteroid)

    def on_load_complete(self):
        # TODO сделать так, чтобы дрон летел на ближайший астероид, если он не полон, а из текущего забрал все
        if not self.is_full:
            for asteroid in self.asteroids:
                if self.near(asteroid):
                    if not asteroid.is_empty:
                        self.move_at(asteroid)
        self.move_at(self.my_mothership)

    def on_stop_at_mothership(self, mothership):
        self.unload_to(mothership)

    def on_unload_complete(self):
        for asteroid in self.asteroids:
            if not asteroid.is_empty:
                self.move_at(asteroid)
