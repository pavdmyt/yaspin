# -*- coding: utf-8 -*-

"""
examples.cli_spinners
~~~~~~~~~~~~~~~~~~~~~

Run all spinners from cli-spinners library:
https://github.com/sindresorhus/cli-spinners

Spinners are sorted alphabetically.
"""

import time

from yaspin import yaspin
from yaspin.constants import SPINNER_ATTRS
from yaspin.spinners import Spinners


def main():
    for name in SPINNER_ATTRS:
        spinner = getattr(Spinners, name)
        with yaspin(spinner, text=name):
            time.sleep(3)


if __name__ == "__main__":
    main()
