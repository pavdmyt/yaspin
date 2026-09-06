"""
examples.timer_spinner
~~~~~~~~~~~~~~~~~~~~~~

Show elapsed time at the end of the line.
"""

import time

from yaspin import yaspin


def default_timer():
    with yaspin(text="elapsed time", timer=True) as sp:
        # Floats are rounded into two decimal digits in timer output.
        time.sleep(3.1415)
        sp.ok()


def custom_timer():
    with yaspin(text="elapsed time", timer=" ({})") as sp:
        # A custom format can omit fractions of a second.
        time.sleep(3.1415)
        sp.ok()


if __name__ == "__main__":
    default_timer()
    custom_timer()
