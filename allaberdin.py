# -*- coding: utf-8 -*-
from astrobox.core import Drone


class AllaberdinDrone(Drone):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.full_charged_distance = 0
        # self.not_empty_distance = 0
        # self.empty_distance = 0

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
        # if self.target == self.mothership:
        #     self.print_stat()
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
                # self.sum_distance()
                return
        if not self.near(self.mothership):
            self.target = self.mothership
            # self.sum_distance()

    # def sum_distance(self):
    #     if self.is_full:
    #         self.full_charged_distance += self.distance_to(self.target)
    #     elif self.is_empty:
    #         self.empty_distance += self.distance_to(self.target)
    #     elif 0 < self.fullness < 1:
    #         self.not_empty_distance += self.distance_to(self.target)
    #
    #
    # def print_stat(self):
    #     print(f'Дрон номер {self.id} пролетел:')
    #     print(f'\t - Полностью загруженным: {self.full_charged_distance}')
    #     print(f'\t - Загруженным не полностью: {self.not_empty_distance}')
    #     print(f'\t - Пустым: {self.empty_distance}')
    #
    # def on_overlap_with(self, obj_status):
    #     if obj_status in self.teammates:
    #         if self.distance_to(self.mothership) > 150:
    #             if not self.loaded:
    #                 if self.free_space >= obj_status.payload:
    #                     print('hey where')
    #                     self.loaded = True
    #                     self.move_at(obj_status)
    #                     obj_status.move_at(self)
    #                     self.load_from(obj_status)
    #                     #
    #                     self.find_next()
    #                     self.move_at(self.target)
    #                     obj_status.find_next()
    #                     obj_status.move_at(obj_status.target)
    #
    #                     return
    # - решить проблему с бесконечным обменом между дронами
    # - Могу предложить сделать флаг дрона отдающий/принимающий. И в зависимости от него действовать.
    #  Далее принявший сбрасывает флаг принимающего, когда разгрузился на базе
