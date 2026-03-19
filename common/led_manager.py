class LEDManager:
    """Manage the LEDs."""

    def __init__(self):
        """Construct."""
        self.ranges = ranges
        self.orderings = orderings

    def leds_for_angle(self, angle):
        """LEDs for `angle`."""
        angle = int(angle)
        if angle == 360:
            angle = 0

        leds = {}
        for key in self.ranges:
            leds[key] = self.ranges[key][angle]

        return leds

    def ordering(self, surface, start, direction):
        """Get an ordering of lights."""
        o = self.orderings[surface]
        if direction.startswith("anti"):
            o = list(reversed(o))

        lead = o.index(start)

        return o[lead:] + o[:lead]

    def ordered_set(self, surface, angle, direction, shape, factor):
        """Complete LED set."""
        start = self.leds_for_angle(angle)[surface]
        order = self.ordering(surface, start, direction)
        if direction == "round":
            brightnesses = round_intensities(
                len(self.orderings[surface]), shape, factor
            )
        else:
            brightnesses = tail_intensities(len(self.orderings[surface]), shape, factor)

        return tuple(zip(order, brightnesses))  # noqa: B905


def tail_intensities(count, shape, factor=1.0):  # noqa: RET503
    """Brightnesses."""
    if shape == "exponential":
        return [(1 / (i + 1)) * factor for i in range(count)]

    if shape == "linear":
        return [(1 - (i / count)) * factor for i in range(count)]


def round_intensities(count, shape, factor=1.0):
    """Brightnesses, wrapped."""
    half = tail_intensities(int(count / 2), shape, factor)
    return half + [0] + list(reversed(half))[:-1]


### nothing good below this line

orderings = {
    "front": list(reversed([i + 1 for i in range(12)])),
    "rear": list(reversed([i + 13 for i in range(6)])),
    "unified": [14, 3, 2, 13, 1, 12, 18, 11, 10, 17, 9, 8, 16, 7, 6, 15, 5, 4],
}

ranges = {}

front_ranges = []
for i in orderings["front"]:
    front_ranges.extend([i] * 30)
ranges["front"] = front_ranges[285:] + front_ranges[:285]

rear_ranges = []
for i in orderings["rear"]:
    rear_ranges.extend([i] * 60)

ranges["rear"] = rear_ranges[270:] + rear_ranges[:270]


sizes = [15, 23, 22]
unified = []
for index in orderings["unified"]:
    unified.extend([index] * sizes[0])
    sizes = sizes[1:] + sizes[:1]

ranges["unified"] = unified[8:] + unified[:8]
