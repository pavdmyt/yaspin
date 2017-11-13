# -*- coding: utf-8 -*-

import time

from yaspin import yaspin
from yaspin.spinners import Spinners


def manual_setup():
    swirl = yaspin(text="Default spinner")
    swirl.start()

    time.sleep(2)

    swirl.spinner = Spinners.arc
    swirl.text = "Arc spinner"

    time.sleep(2)

    swirl.stop()


def context_mngr_setup():
    with yaspin(Spinners.noise, text="Noise spinner") as swirl:
        time.sleep(2)

        swirl.spinner = Spinners.simpleDotsScrolling
        swirl.text = "Scrolling Dots spinner"

        time.sleep(2)


def main():
    manual_setup()
    context_mngr_setup()


if __name__ == '__main__':
    main()
