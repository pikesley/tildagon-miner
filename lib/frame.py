class Frame(list):
    """A Frame."""

    def __init__(self, bits, width=16):
        """Construct."""
        super().__init__()
        self.width = width
        self.bits = bits

        for line in bits:
            padded_line = "0" * self.width + line + "0" * self.width
            self.append([int(x) for x in padded_line])

    def __str__(self):
        """Print us."""
        s = ""

        for line in self:
            for c in line:
                s += str(c)
            s += "\n"

        return s
