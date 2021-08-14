"""
examples.spinner_properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updating spinner on the fly.
"""

import time

from yaspin import yaspin
from yaspin.spinners import Spinners


def manual_setup():
    sp = yaspin(text="Default spinner")
    sp.start()

    time.sleep(2)

    sp.spinner = Spinners.arc
    sp.text = "Right arc yellow spinner"
    sp.color = "yellow"
    sp.side = "right"

    time.sleep(3)

    sp.text = "Reversed arc spinner"
    sp.reversal = True

    time.sleep(3)

    sp.stop()


def context_mngr_setup():
    with yaspin(Spinners.noise, text="Noise spinner") as sp:
        time.sleep(2)

        sp.spinner = Spinners.simpleDotsScrolling
        sp.text = "Scrolling Dots spinner"
        sp.color = "magenta"

        time.sleep(2)


def main():
    manual_setup()
    context_mngr_setup()


if __name__ == "__main__":
    main()
