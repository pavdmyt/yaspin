# -*- coding: utf-8 -*-

"""
examples.kb_interrupt_handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handling keyboard interrupt (control+c) with
try-except block.
"""

import random
import time

from yaspin import yaspin
from yaspin.spinners import Spinners


def unpacker():
    sp = yaspin(Spinners.simpleDotsScrolling, side="right")

    try:
        sp.start()
        for p in range(0, 101, 5):
            sp.text = "{0}% Unpacking".format(p)
            time.sleep(random.random())
        sp.green.ok("✔")
    except KeyboardInterrupt:
        sp.red.fail("✘")
        sp.stop()


def main():
    unpacker()


if __name__ == "__main__":
    main()
