"""
examples.write_method
~~~~~~~~~~~~~~~~~~~~~

Basic usage of ``write`` method.
"""

import time

from yaspin import yaspin


def main():
    with yaspin(text="Downloading images") as sp:
        # task 1
        time.sleep(1)
        sp.write("> image 1 download complete")

        # task 2
        time.sleep(2)
        sp.write("> image 2 download complete")

        # finalize
        sp.green.ok("✔")


if __name__ == "__main__":
    main()
