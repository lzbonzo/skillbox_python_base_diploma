from math import sin, radians, cos

from robogame_engine.geometry import Point, Vector


class PilotBoss:
    """Класс - начальник пилотов """

    @staticmethod
    def choose_pilot(drone):
        """ Определяет какого пилота посадить """

        # TODO - Не очень удачная идея определять стратегю на основе id. Т.к. если поменять очередность содания команд,
        #  то все id ваших дронов будут больше 5
        if drone.scene.teams_count == 1:
            return DefenderPilot(drone)
        else:
            if drone.id in [2, 3]:
                return ReaperPilot(drone)
            else:
                return DefenderPilot(drone)


class Pilot:

    def __init__(self, drone):
        self.drone = drone

    def on_born(self):
        pass

    def on_stop_at_mothership(self):
        pass

    def move_at_base_point(self):
        field_width = self.drone.scene.field[0]
        field_height = self.drone.scene.field[1]
        if self.drone.mothership.y > field_height / 2 and self.drone.mothership.x < field_width / 2:
            # top left
            base_y = self.drone.mothership.y + 300 * sin(
                radians(-90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
            base_x = self.drone.mothership.x + 300 * cos(
                radians(-90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
        elif self.drone.mothership.y > field_height / 2 and self.drone.mothership.x > field_width / 2:
            # top right
            base_y = self.drone.mothership.y + 300 * sin(
                radians(90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)) - 180)
            base_x = self.drone.mothership.x + 300 * cos(
                radians(90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)) - 180)
        elif self.drone.mothership.y < field_height / 2 and self.drone.mothership.x > field_width / 2:
            # bottom right
            base_y = self.drone.mothership.y + 300 * sin(
                radians(180 - 90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
            base_x = self.drone.mothership.x + 300 * cos(
                radians(180 - 90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
        else:
            # bottom left
            base_y = self.drone.mothership.y + 300 * sin(
              radians(90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
            base_x = self.drone.mothership.x + 300 * cos(
               radians(90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
        base_point = Point(abs(base_x), abs(base_y))
        self.drone.turn_to(base_point)
        self.drone.move_at(base_point)

    def move_at_enemy_base_point(self):
        field_width = self.drone.scene.field[0]
        field_height = self.drone.scene.field[1]
        if self.drone.enemy.mothership.y > field_height / 2 and self.drone.enemy.mothership.x < field_width / 2:
            # top left
            base_y = self.drone.enemy.mothership.y + 300 * sin(
                radians(-90 / (len(self.drone.teammates) + 1) * self.drone.id))
            base_x = self.drone.enemy.mothership.x + 300 * cos(
                radians(-90 / (len(self.drone.teammates) + 1) * self.drone.id))
        elif self.drone.enemy.mothership.y > field_height / 2 and self.drone.enemy.mothership.x > field_width / 2:
            # top right
            base_y = self.drone.enemy.mothership.y + 300 * sin(
                radians(90 / (len(self.drone.teammates) + 1) * self.drone.id) - 180)
            base_x = self.drone.enemy.mothership.x + 300 * cos(
                radians(90 / (len(self.drone.teammates) + 1) * self.drone.id) - 180)
        elif self.drone.enemy.mothership.y < field_height / 2 and self.drone.enemy.mothership.x > field_width / 2:
            # bottom right
            base_y = self.drone.enemy.mothership.y + 300 * sin(
                radians(180 - 90 / (len(self.drone.teammates) + 1) * self.drone.id))
            base_x = self.drone.enemy.mothership.x + 300 * cos(
                radians(180 - 90 / (len(self.drone.teammates) + 1) * self.drone.id))
        else:
            # bottom left
            base_y = self.drone.enemy.mothership.y + 300 * sin(
              radians(90 / (len(self.drone.teammates) + 1) * self.drone.id))
            base_x = self.drone.enemy.mothership.x + 300 * cos(
               radians(90 / (len(self.drone.teammates) + 1) * self.drone.id))
        print(abs(base_x), abs(base_y))
        self.drone.move_at(Point(abs(base_x), abs(base_y)))

    def move_at_enemy_attack_point(self):
        field_width = self.drone.scene.field[0]
        field_height = self.drone.scene.field[1]
        if self.drone.enemy.y > field_height / 2 and self.drone.enemy.x < field_width / 2:
            # top left
            enemy_y = self.drone.enemy.y + 500 * sin(
                radians(-90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
            enemy_x = self.drone.enemy.x + 500 * cos(
                radians(-90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
        elif self.drone.enemy.y > field_height / 2 and self.drone.enemy.x > field_width / 2:
            # top right
            enemy_y = self.drone.enemy.y + 500 * sin(
                radians(90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)) - 180)
            enemy_x = self.drone.enemy.x + 500 * cos(
                radians(90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)) - 180)
        elif self.drone.enemy.y < field_height / 2 and self.drone.enemy.x > field_width / 2:
            # bottom right
            enemy_y = self.drone.enemy.y + 400 * sin(
                radians(180 - 90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
            enemy_x = self.drone.enemy.x + 400 * cos(
                radians(180 - 90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
        else:
            # bottom left
            enemy_y = self.drone.enemy.y - 400 * sin(
              radians(90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
            enemy_x = self.drone.enemy.x - 400 * cos(
               radians(90 / (len(self.drone.teammates) + 1) * (self.drone.id - 1)))
        attack_point = Point(abs(enemy_x), abs(enemy_y))
        if attack_point.distance_to(self.drone.mothership) < 100:
            self.move_at_base_point()
            return
        print(attack_point)
        self.drone.move_at(attack_point)

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
        if enemy_drones:
            enemy_with_gun = [drone for drone in enemy_drones if drone.have_gun]
            if enemy_with_gun:
                enemy_drones = enemy_with_gun
            enemy_drones = sorted(enemy_drones, key=lambda x: x.distance_to(self.drone))
            self.drone.enemy = enemy_drones[0]

    @property
    def is_not_empty_asteroids(self):
        asteroids = [asteroid for asteroid in self.drone.asteroids if not asteroid.is_empty]
        if asteroids:
            return True
        self.drone.next_asteroid = None

    def brake_drones(self):
        """ Ломаем дронов соперника"""
        return
        enemy_drones = [drone for drone in self.drone.scene.drones
                        if drone not in self.drone.teammates and drone != self.drone]
        enemy_drones = [drone for drone in enemy_drones if drone.is_alive and drone != self.drone.mothership]
        for drone in enemy_drones:
            drone.vector = Vector.from_points(drone.coord, drone.mothership.coord)
            drone.move_at(Point(600, 450))
            drone.stop()
            drone.gun.shot(drone.mothership)

    def find_death_motherships(self):
        """ Проверяем, есть ли базы, на которые уже никто не вернется"""
        death_motherships = [mothership for mothership in self.drone.scene.motherships
                             if mothership != self.drone.mothership and not mothership.is_alive
                             and not mothership.is_empty]
        if death_motherships:
            return death_motherships[0]

    def live_enemy_drones(self):
        return [drone for drone in self.drone.scene.drones
                if drone not in self.drone.teammates and drone != self.drone and drone.is_alive
                and drone not in self.drone.scene.motherships]

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

    def on_wake_up(self):
        enemy_drones = self.live_enemy_drones()
        if len(enemy_drones) <= 2:
            self.drone.pilot = KillerPilot(self.drone)
        if self.find_death_motherships():
            if self.drone.id <= len(self.drone.teammates) // 2:
                self.drone.pilot = MothershipReaperPilot(self.drone)
                return
        self.move_at_base_point()
        self.find_enemy()
        if self.drone.distance_to(self.drone.mothership) > 50:
            self.drone.turn_to(self.drone.enemy)
            self.drone.gun.shot(self.drone.enemy)

    def need_to_be_killer(self):
        enemy_drones = self.live_enemy_drones()
        if len(enemy_drones) <= 2:
            self.drone.pilot = KillerPilot(self.drone)


class ReaperPilot(Pilot):

    def on_born(self):
        self.find_next()
        self.drone.move_at(self.drone.next_asteroid)

    def on_stop_at_mothership(self):
        self.drone.turn_to(45)
        self.drone.unload_to(self.drone.mothership)

    def on_wake_up(self):
        if not self.is_not_empty_asteroids:
            self.drone.pilot = DefenderPilot(self.drone)
            return
        self.find_next()
        self.drone.move_at(self.drone.next_asteroid)


class MothershipReaperPilot(Pilot):

    def on_wake_up(self):
        death_mothership = self.find_death_motherships()
        if death_mothership:
            self.drone.death_mothership = death_mothership
            self.drone.move_at(death_mothership)
            return
        self.drone.pilot = DefenderPilot(self.drone)


class KillerPilot(Pilot):

    def on_wake_up(self):
        live_enemies = self.live_enemy_drones()
        if not live_enemies:
            self.drone.pilot = ReaperPilot(self.drone)
            return
        self.drone.enemy = live_enemies[0]
        self.move_at_enemy_attack_point()
        if self.drone.distance_to(self.drone.mothership) > 100:
            self.drone.turn_to(self.drone.enemy)
            self.drone.gun.shot(self.drone.enemy)
