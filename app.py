from math import radians
from random import random

from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable
from tildagonos import tildagonos

import app

from .lib.background import Background
from .lib.conf import conf
from .lib.gamma import gamma_corrections
from .lib.willy import Willy
from .pikesley.angles_for_leds.angles_for_leds import led_for_angle
from .pikesley.rgb_from_hue.rgb_from_hue import rgb_from_hue


class Miner(app.App):
    """Miner."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        self.button_states = Buttons(self)
        self.hue = random()
        self.scale = conf["willy-size"]["default"]
        self.opacity = 1.0
        self.rotation = 0
        self.rotation_increment = conf["rotation-amount"]
        self.scale_direction = "up"

        y = 110 - (self.scale * 16)
        self.willy = Willy(
            x=0, y=y, scale=self.scale, hue=self.hue, opacity=self.opacity
        )

    def update(self, _):
        """Update."""
        self.scan_buttons()
        self.willy.animate()
        self.willy.hue = self.hue
        self.willy.scale = self.scale
        self.willy.y = 110 - (self.scale * 16)

        self.hue += 0.001
        self.rotation = (self.rotation - self.rotation_increment) % 360
        self.adjust_scale()
        self.light_leds()

    def adjust_scale(self):
        """Scale up or down."""
        if self.scale_direction == "up":
            if self.scale < conf["willy-size"]["max"]:
                self.scale += conf["scale-factor"]
            else:
                self.scale_direction = "down"

        elif self.scale > conf["willy-size"]["min"]:
            self.scale -= conf["scale-factor"]
        else:
            self.scale_direction = "up"

    def draw(self, ctx):
        """Draw."""
        ctx.rotate(radians(self.rotation))
        self.overlays = []
        self.overlays.append(Background(colour=rgb_from_hue((self.hue + 0.5) % 1)))

        self.overlays.extend(self.willy.pixels)

        self.draw_overlays(ctx)

    def scan_buttons(self):
        """Buttons."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

        if self.button_states.get(BUTTON_TYPES["RIGHT"]):
            self.button_states.clear()
            self.willy.bump_index()

        if self.button_states.get(BUTTON_TYPES["LEFT"]):
            self.button_states.clear()
            self.willy.randomise = not self.willy.randomise

    def light_leds(self):
        """Light the lights."""
        colour = rgb_from_hue(self.hue)
        tildagonos.leds[
            led_for_angle((conf["rotation-offset"] - self.rotation) % 360)
        ] = [gamma_corrections[int(i * 255 * conf["led-brightness"])] for i in colour]

        tildagonos.leds.write()


__app_export__ = Miner
