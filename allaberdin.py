# -*- coding: utf-8 -*-
from astrobox.core import Drone


class AllaberdinDrone(Drone):

    def __init__(self):
        super().__init__()
        self.full_charged_distance = 0
        self.not_empty_distance = 0
        self.empty_distance = 0

    def on_born(self):
        self.find_next()
        self.move_at(self.target)

    def on_stop_at_asteroid(self, asteroid):
        self.load_from(asteroid)

    # def on_overlap_with(self, obj_status):
    #     if obj_status in self.teammates:
    #         if 300 < self.distance_to(self.mothership):
    #             if self.is_empty and obj_status.is_full:
    #                 self.move_at(obj_status)
    #                 obj_status.move_at(self)
    #                 self.load_from(obj_status)
    #                 return
    # TODO решить проблему с бесконечным обменом между дронами

    def sum_distance(self):
        # TODO Как говорится, важно не как проголосуют, а как посчитают))
        #  Я указал, что если дрон заполнен на 80%, то его уже можно считать полным.
        #  Или лучше считать грубо, если на 99% процентов заполнен - все равно не полный?
        if self.fullness >= .8:
            self.full_charged_distance += self.distance_to(self.target)
        elif self.is_empty:
            self.empty_distance += self.distance_to(self.target)
        elif 0 < self.fullness < .8:
            self.not_empty_distance += self.distance_to(self.target)

    def on_load_complete(self):
        self.find_next()
        self.move_at(self.target)

    def on_stop_at_mothership(self, mothership):
        self.unload_to(mothership)

    def on_unload_complete(self):
        self.find_next()
        if self.target == self.mothership:
            self.print_stat()
        self.move_at(self.target)

    def find_next(self):
        """
        Находит следующий пункт назначения
        """
        targets = [drone.target for drone in self.teammates]
        asteroids = [asteroid for asteroid in self.asteroids if asteroid not in targets and not asteroid.is_empty]
        if asteroids:
            asteroids = sorted(asteroids, key=lambda x: x.distance_to(self))
            if not self.is_full:
                self.target = asteroids[0]
                self.sum_distance()
                return
        if not self.near(self.mothership):
            self.target = self.mothership
            self.sum_distance()

    def print_stat(self):
        print(f'Дрон номер {self.id} пролетел:')
        print(f'\t - Полностью загруженным: {self.full_charged_distance}')
        print(f'\t - Загруженным не полностью: {self.not_empty_distance}')
        print(f'\t - Пустым: {self.empty_distance}')
