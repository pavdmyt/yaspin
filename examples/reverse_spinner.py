# -*- coding: utf-8 -*-

"""
examples.reverse_spinner
~~~~~~~~~~~~~~~~~~~~~~~~

Reverse spinner rotation.
"""

import time

from yaspin import yaspin
from yaspin.spinners import Spinners


def main():
    with yaspin(Spinners.clock, text="Clockwise") as sp:

        # Clockwise rotation
        time.sleep(3)

        # Reverse spin direction
        sp.reversal = True
        sp.text = "Counterclockwise"

        # Counterclockwise rotation
        time.sleep(3)


if __name__ == "__main__":
    main()
