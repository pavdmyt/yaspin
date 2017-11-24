# -*- coding: utf-8 -*-

"""
examples.advanced_colors
~~~~~~~~~~~~~~~~~~~~~~~~

Use familiar API of the `termcolor.colored` function to apply any
color, highlight, attribute or their mix to your yaspin spinner.
"""

import sys
import time

from yaspin import yaspin
from yaspin.spinners import Spinners

try:
    from termcolor import colored
except ImportError:
    print("termcolor should be installed to run this example.\n"
          "Run 'pip install termcolor' and try again.")
    sys.exit(1)


def test_highlights():
    test_items = [
        (
            "On gray color",
            lambda frame: colored(frame, on_color='on_grey')
        ),
        (
            "On red color",
            lambda frame: colored(frame, on_color='on_red')
        ),
        (
            "On green color",
            lambda frame: colored(frame, on_color='on_green')
        ),
        (
            "On yellow color",
            lambda frame: colored(frame, on_color='on_yellow')
        ),
        (
            "On blue color",
            lambda frame: colored(frame, on_color='on_blue')
        ),
        (
            "On magenta color",
            lambda frame: colored(frame, on_color='on_magenta')
        ),
        (
            "On cyan color",
            lambda frame: colored(frame, on_color='on_cyan')
        ),
        (
            "On white color",
            lambda frame: colored(frame, on_color='on_white')
        ),
    ]
    for text, color_func in test_items:
        with yaspin(Spinners.bouncingBall, text=text, color=color_func):
            time.sleep(2)


def test_attributes():
    test_items = [
        (
            "Bold gray color",
            lambda frame: colored(frame, 'grey', attrs=['bold'])
        ),
        (
            "Dark red color",
            lambda frame: colored(frame, 'red', attrs=['dark'])
        ),
        (
            "Underline green color",
            lambda frame: colored(frame, 'green', attrs=['underline'])
        ),
        (
            "Blink yellow color",
            lambda frame: colored(frame, 'yellow', attrs=['blink'])
        ),
        (
            "Reversed blue color",
            lambda frame: colored(frame, 'blue', attrs=['reverse'])
        ),
        (
            "Concealed magenta color",
            lambda frame: colored(frame, 'magenta', attrs=['concealed'])
        ),
        (
            "Bold underline reverse cyan color",
            lambda frame: colored(frame, 'cyan', attrs=['bold', 'underline', 'reverse'])  # noqa
        ),
        (
            "Dark blink concealed white color",
            lambda frame: colored(frame, 'white', attrs=['dark', 'blink', 'concealed'])  # noqa
        ),
    ]
    for text, color_func in test_items:
        with yaspin(Spinners.bouncingBar, text=text, color=color_func):
            time.sleep(2)


def test_mixing():
    test_items = [
        (
            "Underline red on grey color",
            lambda frame: colored(frame, 'red', 'on_grey', attrs=['underline'])
        ),
        (
            "Reversed green on red color",
            lambda frame: colored(frame, 'green', 'on_red', attrs=['reverse'])
        ),
    ]
    for text, color_func in test_items:
        with yaspin(Spinners.pong, text=text, color=color_func):
            time.sleep(2)


def main():
    test_highlights()
    test_attributes()
    test_mixing()


if __name__ == '__main__':
    main()
