# -*- coding: utf-8 -*-

from astrobox.core import Drone

from pilots_headquarters import DefenderPilot, ReaperPilot


class AllaberdinDrone(Drone):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enemy = None
        self.next_asteroid = None
        self.death_mothership = None
        teammates = [dr for dr in self.scene.drones if isinstance(dr, AllaberdinDrone)]
        self.number = teammates.index(self)
        self.pilot = DefenderPilot(self)

    def on_born(self):
        self.pilot.on_born()

    def on_load_complete(self):
        self.pilot.find_next()
        self.move_at(self.next_asteroid)


    def on_stop_at_asteroid(self, asteroid):
        if isinstance(self.pilot, ReaperPilot):
            if not asteroid.is_empty:
                self.turn_to(self.mothership)
                self.load_from(asteroid)

    def on_stop_at_mothership(self, mothership):
        if mothership != self.mothership and not mothership.is_empty:
            self.load_from(mothership)
            return
        if not self.is_empty:
            self.unload_to(mothership)
        self.pilot.on_stop_at_mothership()

    def on_wake_up(self):
        self.pilot.on_wake_up()

    def on_heartbeat(self):
        if self.health <= 70:
            self.move_at(self.mothership)
        # TODO - Убирайте неиспользумый код
        # self.pilot.brake_drones()

