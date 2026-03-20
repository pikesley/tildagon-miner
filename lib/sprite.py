import os
from random import choice, randint

from ..common.rgb_from_hue import rgb_from_hue
from ..common.shapes.circle import Circle
from ..common.shapes.hexagon import Hexagon
from ..common.shapes.pentagon import Pentagon
from ..common.shapes.pentagram import Pentagram
from ..common.shapes.square import Square
from ..common.shapes.triangle import Triangle
from .asset_path import ASSET_PATH
from .conf import conf

shapes_list = [
    Circle,
    Square,
    Hexagon,
    Pentagon,
    Triangle,
    Pentagram,
]


class Sprite:
    """Willy."""

    def __init__(self, x=0, y=0, scale=5, hue=1.0, opacity=0.7, speed=1):  # noqa: PLR0913
        """Construct."""
        self.x = x
        self.y = y
        self.scale = scale
        self.hue = hue
        self.opacity = opacity
        self.speed = speed

        self.shapes_index = 0
        self.randomise = conf["start-randomised"]

    def load_frames(self, name):
        """Load frames."""
        self.frames = []
        frame_data = os.listdir(f"{ASSET_PATH}/bitmaps/{name}")
        for item in sorted(frame_data):
            with open(f"{ASSET_PATH}/bitmaps/{name}/{item}") as f:
                self.frames.append([])
                for line in f.read().strip().split("\n"):
                    self.frames[-1].append([int(x) for x in list(line)])

    def move(self):
        """Walk."""
        self.x += self.speed

    def animate(self):
        """Animate."""
        self.frames = self.frames[1:] + [self.frames[0]]

    @property
    def pixels(self):
        """Draw."""
        scale = self.scale

        pix = []
        start_y = (-scale * 15) + self.y
        colour = rgb_from_hue(self.hue)
        for bits in self.frames[0]:
            start_x = scale * -(len(bits))
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
