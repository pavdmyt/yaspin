# -*- coding: utf-8 -*-

"""
examples.finalizers
~~~~~~~~~~~~~~~~~~~

Success and Failure finalizers.
"""

import time

from yaspin import yaspin


def default_finalizers():
    with yaspin(text="Downloading...") as sp:
        time.sleep(2)
        sp.ok()

    with yaspin(text="Downloading...") as sp:
        time.sleep(2)
        sp.fail()


def custom_finalizers():
    with yaspin(text="Processing...") as sp:
        time.sleep(2)
        sp.ok('☀️')

    with yaspin(text="Processing...", right=True) as sp:
        time.sleep(2)
        sp.fail('💥')

    with yaspin(text="Processing...") as sp:
        time.sleep(2)
        sp.ok(b'\xe2\x9c\x94')


def main():
    default_finalizers()
    custom_finalizers()


if __name__ == '__main__':
    main()
