angles = [
    {
        "lower": i - 15,
        "centre": i,
        "upper": i + 15,
    }
    for i in range(15, 360, 30)
]
indeces = [i + 1 for i in reversed(list(range(12)))]
angles_for_leds = dict(zip(indeces[9:] + indeces[:9], angles))  # noqa: B905


def led_for_angle(angle):
    """LED index at `angle`."""
    for index, span in angles_for_leds.items():  # noqa: RET503
        if span["lower"] <= angle <= span["upper"]:
            return index
