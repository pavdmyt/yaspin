"""
examples.timer_spinner
~~~~~~~~~~~~~~~~~~~~~~

Show elapsed time at the end of the line.
"""

import time

from yaspin import yaspin


def main():
    with yaspin(text="elapsed time", timer=True) as sp:
        # Floats are rounded into two decimal digits in timer output
        time.sleep(3.1415)
        sp.ok()


if __name__ == "__main__":
    main()
