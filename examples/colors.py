# -*- coding: utf-8 -*-

"""
examples.colors
~~~~~~~~~~~~~~~

Basic usage of the color argument.
"""

import time

from yaspin import yaspin


def all_text_colors():
    with yaspin(text="Colors!") as sp:
        time.sleep(2)

        colors = ("red", "green", "yellow", "blue", "magenta", "cyan", "white")
        for color in colors:
            sp.color = color
            sp.text = color
            time.sleep(2)


def colored_finalizer():
    with yaspin(text="Processing...", color="yellow") as sp:
        time.sleep(2)
        sp.ok('☀️')


@yaspin(text="Colored decorator", color="yellow")
def decorated_function():
    time.sleep(2)


def main():
    all_text_colors()
    colored_finalizer()
    decorated_function()


if __name__ == '__main__':
    main()
