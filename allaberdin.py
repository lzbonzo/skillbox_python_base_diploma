# -*- coding: utf-8 -*-

from astrobox.core import Drone

from pilots_headquarters import PilotBoss


class AllaberdinDrone(Drone):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enemy = None
        self.next_asteroid = None
        self.pilot = PilotBoss().choose_pilot(self)

    def on_born(self):
        self.pilot.on_born()

    def on_load_complete(self):
        self.pilot.find_next()
        self.move_at(self.next_asteroid)

    def on_stop_at_asteroid(self, asteroid):
        self.turn_to(self.mothership)
        self.load_from(asteroid)

    def on_stop_at_mothership(self, mothership):
        self.pilot.on_stop_at_mothership()

    def on_wake_up(self):
        self.pilot.on_wake_up()

    def on_heartbeat(self):
        self.pilot.brake_drones()

