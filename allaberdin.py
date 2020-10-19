# -*- coding: utf-8 -*-
from math import cos, sin, radians

from astrobox.core import Drone
from robogame_engine.geometry import Point, Vector


class AllaberdinDrone(Drone):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enemy = None
        self.next_asteroid = None

    def on_load_complete(self):
        self.find_next()
        self.move_at(self.next_asteroid)

    def on_stop_at_asteroid(self, asteroid):
        self.turn_to(self.mothership)
        self.load_from(asteroid)

    def on_stop_at_mothership(self, mothership):
        self.turn_to(45)
        if not self.is_empty:
            self.unload_to(mothership)
        if not self.is_not_empty_asteroids():
            self.find_enemy()

    def find_next(self):
        """
        Находит следующий пункт назначения
        """
        targets = [drone.next_asteroid for drone in self.teammates if drone.next_asteroid is not None]
        asteroids = [asteroid for asteroid in self.asteroids if asteroid not in targets and not asteroid.is_empty]
        if asteroids:
            asteroids = sorted(asteroids, key=lambda x: x.distance_to(self))
            if not self.is_full:
                self.next_asteroid = asteroids[0]
                return
        self.next_asteroid = self.mothership
        self.find_enemy()

    def find_enemy(self):
        """Ищем следующего дрона для атаки"""
        enemy_drones = [drone for drone in self.scene.drones if not isinstance(drone, AllaberdinDrone)]
        enemy_drones = [drone for drone in enemy_drones if drone.is_alive and drone != self.mothership]
        if len(enemy_drones) > len(self.teammates) + 1:
            targets = [drone.enemy for drone in self.teammates]
            enemy_drones = [drone for drone in enemy_drones if drone not in targets and drone.have_gun]
        if enemy_drones:
            enemy_drones = sorted(enemy_drones, key=lambda x: x.distance_to(self))
            self.enemy = enemy_drones[0]
        else:
            self.enemy = None

    def is_not_empty_asteroids(self):
        asteroids = [asteroid for asteroid in self.asteroids if not asteroid.is_empty]
        if asteroids:
            return True
        self.next_asteroid = None

    def brake_drones(self):
        """ Ломаем дронов соперника"""
        return
        # TODO - Тогда теряется весь смысл в соревнованиях. Без хаков, пожалуйста
        enemy_drones = [drone for drone in self.scene.drones if not isinstance(drone, AllaberdinDrone)]
        enemy_drones = [drone for drone in enemy_drones if drone.is_alive and drone != self.mothership]
        for drone in enemy_drones:
            drone.vector = Vector.from_points(drone.coord, drone.mothership.coord)
            drone.stop()
            drone.gun.shot(drone.mothership)

    def on_collide_with(self, obj_status):
        if obj_status in self.teammates:
            self.stop()

    def on_wake_up(self):
        not_empty_ast = [ast for ast in self.asteroids if not ast.is_empty]
        if self.is_not_empty_asteroids():
            self.find_next()
            self.move_at(self.next_asteroid)
            return
        if len(not_empty_ast) < len(self.teammates):
            self.find_enemy()
            enemy_near = [drone for drone in self.scene.drones if not isinstance(drone, AllaberdinDrone)
                          and drone.distance_to(self) <= 300]
            if enemy_near:
                self.enemy = enemy_near[0]
            if self.distance_to(self.mothership) < 200:
                base_y = 150 + 300 * sin(radians(90 / (len(self.teammates) + 1) * self.id))
                base_x = 150 + 300 * cos(radians(90 / (len(self.teammates) + 1) * self.id))
                self.move_at(Point(base_x, base_y))
            if not self.enemy or not self.enemy.is_alive:
                self.find_enemy()
            if self.enemy:
                field_width = self.scene.field[0]
                field_height = self.scene.field[1]
                if self.enemy.mothership.x < field_height / 2 and self.enemy.mothership.y > field_width / 2:
                    angle = -90  # Верхний левый угол
                elif self.enemy.mothership.x > field_height / 2 and self.enemy.mothership.y > field_width / 2:
                    angle = -180  # Верхний правый угол
                elif self.enemy.mothership.x > field_height / 2 and self.enemy.mothership.y < field_width / 2:
                    angle = 180  # Нижний левый угол
                else:
                    angle = 90  # Нижний правый угол
                base_y = self.enemy.mothership.y + 300 * sin(radians(angle / (len(self.teammates) + 1) * self.id))
                base_x = self.enemy.mothership.x + 300 * cos(radians(angle / (len(self.teammates) + 1) * self.id))
                self.move_at(Point(base_x, base_y))
                # TODO - Отладочную информацию выводите в лог-файл
                print(self.id, base_x, base_y)
                if self.distance_to(self.enemy.mothership) <= 300:
                    self.turn_to(self.enemy.mothership)
                    self.gun.shot(self.enemy)
                return
        self.move_at(self.mothership)

    def on_heartbeat(self):
        self.brake_drones()
        if self.health <= 70:
            self.move_at(self.mothership)
