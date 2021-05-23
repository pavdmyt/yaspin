"""
examples.hide_show
~~~~~~~~~~~~~~~~~~

Basic usage of the ``hide`` and ``show`` methods.
Starting from yaspin v1.1.0 handled by ``hidden`` context manager.
"""

import sys
import time

from yaspin import yaspin


def main():
    with yaspin(text="Downloading images") as sp:
        # task 1
        time.sleep(1)
        with sp.hidden():
            sys.stdout.write("> image 1 download complete\n")

        # task 2
        time.sleep(2)
        with sp.hidden():
            sys.stdout.write("> image 2 download complete\n")

        # finalize
        sp.green.ok("✔")


if __name__ == "__main__":
    main()
