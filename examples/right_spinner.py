"""
examples.right_spinner
~~~~~~~~~~~~~~~~~~~~~~

Left and Right spinner position.
"""

import time

from yaspin import yaspin


def main():
    with yaspin(text="Right spinner", side="right", color="cyan") as sp:
        time.sleep(2)

        # Switch to left spinner
        sp.side = "left"  # or just ``sp.left``
        sp.text = "Left spinner"

        time.sleep(2)


if __name__ == "__main__":
    main()
