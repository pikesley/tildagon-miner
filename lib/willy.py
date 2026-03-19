from random import choice, randint

from ..common.rgb_from_hue import rgb_from_hue
from ..common.shapes.circle import Circle
from ..common.shapes.hexagon import Hexagon
from ..common.shapes.pentagon import Pentagon
from ..common.shapes.pentagram import Pentagram
from ..common.shapes.square import Square
from ..common.shapes.triangle import Triangle
from .conf import conf

shapes_list = [
    Circle,
    Square,
    Hexagon,
    Pentagon,
    Triangle,
    Pentagram,
]


class Willy:
    """Willy."""

    def __init__(self, x=0, y=0, scale=5, hue=1.0, opacity=0.7, speed=1):  # noqa: PLR0913
        """Construct."""
        self.x = x
        self.y = y
        self.scale = scale
        self.hue = hue
        self.opacity = opacity
        self.speed = speed

        self.frames = conf["frames"]
        self.frame_keys = ["regular", "wide", "regular", "narrow"]
        self.frame_key_index = 0
        self.shapes_index = 0
        self.randomise = conf["start-randomised"]

    def move(self):
        """Walk."""
        self.x += self.speed

    def animate(self):
        """Animate."""
        self.frame_key_index = (self.frame_key_index + 1) % len(self.frame_keys)

    @property
    def pixels(self):
        """Draw."""
        scale = self.scale

        pix = []
        start_y = (-scale * 15) + self.y
        colour = rgb_from_hue(self.hue)
        for item in self.frames[self.frame_keys[self.frame_key_index]]:
            bits = f"{item:010b}"
            start_x = scale * -9
            for bit in bits:
                if int(bit) == 1:
                    rotation = 0
                    if self.randomise:
                        rotation = randint(0, 360)
                    pix.append(
                        self.get_shape(
                            centre=(start_x, start_y),
                            colour=colour,
                            size=scale,
                            opacity=self.opacity,
                            rotation=rotation,
                        ),
                    )
                start_x += scale * 2

            start_y += scale * 2
        return pix

    @property
    def get_shape(self):
        """Get the shapes index."""
        if self.randomise:
            return choice(shapes_list)

        return shapes_list[self.shapes_index]

    def bump_index(self):
        """Bump the shapes index."""
        self.shapes_index = (self.shapes_index + 1) % len(shapes_list)
