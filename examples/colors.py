# -*- coding: utf-8 -*-

"""
examples.colors
~~~~~~~~~~~~~~~

Basic usage of the 'color', 'on_color' and 'attrs' arguments.
"""

import time

from yaspin import yaspin


def all_colors():
    with yaspin(text="Colors!").bouncingBar as sp:
        time.sleep(2)

        colors = ("red", "green", "yellow", "blue", "magenta", "cyan", "white")
        for color in colors:
            sp.color, sp.text = color, color
            time.sleep(2)


def all_highlights():
    with yaspin(text="Highlights!").pong as sp:
        time.sleep(2)

        highlights = (
            "on_red",
            "on_green",
            "on_yellow",
            "on_blue",
            "on_magenta",
            "on_cyan",
            "on_white",
            "on_grey",
        )
        for highlight in highlights:
            text = "On {0} color".format(highlight.split("_")[1])
            sp.on_color, sp.text = highlight, text
            time.sleep(2)


def all_attributes():
    with yaspin(text="Attributes!").point as sp:
        time.sleep(2)

    attrs = ("bold", "dark", "underline", "blink", "reverse", "concealed")
    # New spinner instance should be created every iteration since
    # multiple simultaneous color attributes are supported. Hence,
    # updating attribute of the instance will add new attribute to
    # the existing list of previous attributes.
    for attr in attrs:
        with yaspin().point as sp:
            sp.attrs, sp.text = [attr], attr
            time.sleep(2)


def main():
    all_colors()
    all_highlights()
    all_attributes()


if __name__ == "__main__":
    main()
