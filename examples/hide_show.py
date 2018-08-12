# -*- coding: utf-8 -*-

"""
examples.hide_show
~~~~~~~~~~~~~~~~~~

Basic usage of the ``hide`` and ``show`` methods.
"""

import sys
import time

from yaspin import yaspin


def main():
    with yaspin(text="Downloading images") as sp:
        # task 1
        time.sleep(1)
        sp.hide()
        sys.stdout.write("> image 1 download complete\n")
        sp.show()

        # task 2
        time.sleep(2)
        sp.hide()
        sys.stdout.write("> image 2 download complete\n")
        sp.show()

        # finalize
        sp.green.ok("✔")


if __name__ == "__main__":
    main()
