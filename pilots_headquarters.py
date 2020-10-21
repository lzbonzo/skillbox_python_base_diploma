from math import sin, radians, cos

from robogame_engine.geometry import Point, Vector


class PilotBoss:
    """Класс - начальник пилотов """

    @staticmethod
    def choose_pilot(drone):
        """ Определяет какого пилота посадить """
        if drone.id == 1:
            return ReaperPilot(drone)
        elif drone.id in [2, 3, 4]:
            return MothershipKillerPilot(drone)
        else:
            return DefenderPilot(drone)


class Pilot:

    def __init__(self, drone):
        self.drone = drone

    def move_at_base_point(self):
        field_height = self.drone.scene.field[1]
        if self.drone.mothership.y < field_height / 2:
            # bottom corners
            base_y = self.drone.mothership.y + 300 * sin(radians(90 / (len(self.drone.teammates) + 1) * self.drone.id))
            base_x = self.drone.mothership.x + 300 * cos(radians(90 / (len(self.drone.teammates) + 1) * self.drone.id))
        else:
            # top corners
            base_y = self.drone.mothership.y - 300 * sin(radians(-90 / (len(self.drone.teammates) + 1) * self.drone.id))
            base_x = self.drone.mothership.x - 300 * cos(radians(-90 / (len(self.drone.teammates) + 1) * self.drone.id))
        self.drone.move_at(Point(abs(base_x), abs(base_y)))

    def move_at_enemy_attack_point(self):
        field_width = self.drone.scene.field[0]
        field_height = self.drone.scene.field[1]
        if self.drone.enemy.y > field_height / 2 and self.drone.enemy.x < field_width / 2:
            # top left
            enemy_y = self.drone.enemy.y + 400 * sin(
                radians(-90 / (len(self.drone.teammates) + 1) * self.drone.id))
            enemy_x = self.drone.enemy.x + 400 * cos(
                radians(-90 / (len(self.drone.teammates) + 1) * self.drone.id))
        elif self.drone.enemy.y > field_height / 2 and self.drone.enemy.x > field_width / 2:
            # top right
            enemy_y = self.drone.enemy.y + 400 * sin(
                radians(90 / (len(self.drone.teammates) + 1) * self.drone.id) - 180)
            enemy_x = self.drone.enemy.x + 400 * cos(
                radians(90 / (len(self.drone.teammates) + 1) * self.drone.id) - 180)
        elif self.drone.enemy.y < field_height / 2 and self.drone.enemy.x > field_width / 2:
            # bottom right
            enemy_y = self.drone.enemy.y + 400 * sin(
                radians(180 - 90 / (len(self.drone.teammates) + 1) * self.drone.id))
            enemy_x = self.drone.enemy.x + 400 * cos(
                radians(180 - 90 / (len(self.drone.teammates) + 1) * self.drone.id))
        else:
            # bottom left
            enemy_y = self.drone.enemy.y - 400 * sin(
              radians(90 / (len(self.drone.teammates) + 1) * self.drone.id))
            enemy_x = self.drone.enemy.x - 400 * cos(
               radians(90 / (len(self.drone.teammates) + 1) * self.drone.id))
        print('enemy', enemy_x, enemy_y, 'coord', self.drone.enemy.coord)
        self.drone.move_at(Point(abs(enemy_x), abs(enemy_y)))

    def find_next(self):
        """
        Находит следующий пункт назначения
        """
        targets = [drone.next_asteroid for drone in self.drone.teammates if drone.next_asteroid is not None]
        asteroids = [asteroid for asteroid in self.drone.asteroids if asteroid not in targets and not asteroid.is_empty]
        if asteroids:
            asteroids = sorted(asteroids, key=lambda x: x.distance_to(self.drone))
            if not self.drone.is_full:
                self.drone.next_asteroid = asteroids[0]
                return
        self.drone.next_asteroid = self.drone.mothership
        self.find_enemy()

    def find_enemy(self):
        """Ищем следующего дрона для атаки"""
        enemy_drones = [drone for drone in self.drone.scene.drones
                        if drone not in self.drone.teammates and drone != self.drone]
        enemy_drones = [drone for drone in enemy_drones if drone.is_alive and drone != self.drone.mothership]
        if len(enemy_drones) > len(self.drone.teammates) + 1:
            targets = [drone.enemy for drone in self.drone.teammates]
            enemy_drones = [drone for drone in enemy_drones if drone not in targets and drone.have_gun]
        if enemy_drones:
            enemy_with_gun = [drone for drone in enemy_drones if drone.have_gun]
            if enemy_with_gun:
                enemy_drones = enemy_with_gun
            enemy_drones = sorted(enemy_drones, key=lambda x: x.distance_to(self.drone))
            self.drone.enemy = enemy_drones[0]

    def is_not_empty_asteroids(self):
        asteroids = [asteroid for asteroid in self.drone.asteroids if not asteroid.is_empty]
        if asteroids:
            return True
        self.drone.next_asteroid = None

    def brake_drones(self):
        """ Ломаем дронов соперника"""
        enemy_drones = [drone for drone in self.drone.scene.drones
                        if drone not in self.drone.teammates and drone != self.drone]
        enemy_drones = [drone for drone in enemy_drones if drone.is_alive and drone != self.drone.mothership]
        for drone in enemy_drones:
            drone.vector = Vector.from_points(drone.coord, drone.mothership.coord)
            drone.move_at(Point(600, 450))
            drone.stop()
            drone.gun.shot(drone.mothership)

    @property
    def have_enemies(self):
        enemies = [drone for drone in self.drone.scene.drones
                   if drone not in self.drone.teammates and drone != self.drone and drone.is_alive]
        if enemies:
            return True

    def check_motherships(self):
        """ Проверяем, есть ли базы, на которые уже никто не вернется"""
        live_drones_motherships = set(drone.mothership for drone in self.drone.scene.drones
                                      if drone not in self.drone.teammates and drone != self.drone)
        empty_motherships = [m for m in self.drone.scene.motherships
                             if m not in live_drones_motherships and m != self.drone.mothership]
        if empty_motherships:
            return empty_motherships[0]

    def find_enemy_motherships(self):
        enemy_motherships = [mothership for mothership in self.drone.scene.motherships
                             if mothership != self.drone.mothership and mothership not in
                             [drone.enemy for drone in self.drone.teammates]]
        self.drone.enemy = enemy_motherships[0]

    # def teammate_on_fireline(self):
    #     """ Проверям находится ли кто-то из команды на линии огня"""
    #     a = (self.drone.x, self.drone.y)
    #     b = (self.drone.enemy.x, self.drone.enemy.y)
    #     ab = LineString([a, b])  # the line you got from linear regression
    #     circle = ShapelyPoint(a).buffer(self.drone.distance_to(self.drone.enemy))
    #     left_border = rotate(ab, -170, origin=a)
    #     right_border = rotate(ab, 170, origin=a)
    #     splitter = LineString([*left_border.coords, *right_border.coords[::-1]])
    #     sector = split(circle, splitter)[1]
    #     for drone in self.drone.teammates:
    #         if sector.contains(ShapelyPoint(drone.x, drone.y)):
    #             if self.drone.distance_to(drone) < self.drone.distance_to(self.drone.enemy):
    #                 return True


class DefenderPilot(Pilot):

    def on_born(self):
        self.move_at_base_point()

    def on_stop_at_mothership(self):
        self.move_at_base_point()

    def on_wake_up(self):
        self.find_enemy()
        self.drone.turn_to(self.drone.enemy)
        self.drone.gun.shot(self.drone.enemy)


class MothershipKillerPilot(Pilot):

    def on_born(self):
        self.find_enemy_motherships()
        self.move_at_enemy_attack_point()

    def on_stop_at_mothership(self):
        self.find_enemy_motherships()
        self.move_at_enemy_attack_point()

    def on_wake_up(self):
        self.drone.turn_to(self.drone.enemy)
        self.drone.gun.shot(self.drone.enemy)

    def on_wake_up_1(self):
        if self.drone.health <= 80:
            self.drone.turn_to(self.drone.mothership)
            self.drone.move_at(self.drone.mothership)
            return

        if self.have_enemies:
            self.find_enemy()
            if self.drone.distance_to(self.drone.mothership) > 100:
                enemy_near = [drone for drone in self.drone.scene.drones
                              if drone not in self.drone.teammates and drone != self.drone]
                enemy_near = [drone for drone in enemy_near if drone.is_alive
                              and self.drone.distance_to(drone) < 300]


                enemy_near = sorted(enemy_near, key=lambda x: x.distance_to(self.drone))
                if enemy_near:
                    self.drone.enemy = enemy_near[0]
                else:
                    # self.find_enemy()
                    self.move_at_enemy_attack_point()
                enemy_near_mothership = [drone for drone in self.drone.scene.drones
                                         if drone not in self.drone.teammates and drone != self.drone
                                         and drone.distance_to(self.drone.mothership) < 200]
                if enemy_near_mothership:
                    self.drone.enemy = enemy_near_mothership[0]
                self.drone.turn_to(self.drone.enemy)
                # if not self.drone.teammate_on_fireline():

                    # self.drone.stop()

                    # return
                    # self.drone.vector = Vector.from_points(self.drone.coord, self.drone.enemy.coord)
                    # self.drone.move_at_enemy_attack_point()

                self.drone.gun.shot(self.drone.enemy)
            return
        self.drone.move_at(self.drone.mothership)


class ReaperPilot(Pilot):

    def on_born(self):
        self.find_next()
        self.drone.move_at(self.drone.next_asteroid)

    def on_stop_at_mothership(self):
        self.drone.turn_to(45)
        self.drone.unload_to(self.drone.mothership)

    def on_wake_up(self):
        self.find_next()
        self.drone.move_at(self.drone.next_asteroid)

# TODO Enemy mothership attack point. Should be closer to self.mothership
# TODO If no asteroids change pilot to fight in space.
