# -*- coding: utf-8 -*-

"""
examples.spinner_properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updating spinner on the fly.
"""

import time

from yaspin import yaspin
from yaspin.spinners import Spinners


def manual_setup():
    swirl = yaspin(text="Default spinner")
    swirl.start()

    time.sleep(2)

    swirl.spinner = Spinners.arc
    swirl.text = "Right arc spinner"
    swirl.color = "yellow"
    swirl.right = True

    time.sleep(3)

    swirl.text = "Resersed arc spinner"
    swirl.reverse = True

    time.sleep(3)

    swirl.stop()


def context_mngr_setup():
    with yaspin(Spinners.noise, text="Noise spinner") as swirl:
        time.sleep(2)

        swirl.spinner = Spinners.simpleDotsScrolling
        swirl.text = "Scrolling Dots spinner"
        swirl.color = "magenta"

        time.sleep(2)


def main():
    manual_setup()
    context_mngr_setup()


if __name__ == '__main__':
    main()
