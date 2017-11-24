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

    with yaspin(text="Processing...") as sp:
        time.sleep(2)
        sp.fail('💥')


def main():
    default_finalizers()
    custom_finalizers()


if __name__ == '__main__':
    main()
