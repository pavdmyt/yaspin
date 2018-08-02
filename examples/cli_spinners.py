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
from yaspin.spinners import Spinners, _get_attrs


def main():
    names = _get_attrs(Spinners)
    for name in sorted(names):
        spinner = getattr(Spinners, name)
        with yaspin(spinner, text=name):
            time.sleep(3)


if __name__ == "__main__":
    main()
