# -*- coding: utf-8 -*-

"""
examples.demo
~~~~~~~~~~~~~

Yaspin features demonstration.
"""

import random
import time

from yaspin import yaspin
from yaspin.spinners import Spinners
from yaspin.termcolor import colored


def any_spinner_you_like():
    params = [
        ("line",         0.8),
        ("dots10",       0.8),
        ("dots11",       0.8),
        ("simpleDots",   1),
        ("star",         0.5),
        ("balloon",      0.7),
        ("noise",        0.5),
        ("arc",          0.5),
        ("arrow2",       0.5),
        ("bouncingBar",  1),
        ("bouncingBall", 1),
        ("smiley",       0.7),
        ("hearts",       0.5),
        ("clock",        0.7),
        ("earth",        0.7),
        ("moon",         0.7),
        ("runner",       0.5),
        ("pong",         1),
        ("shark",        1.5),
        ("christmas",    0.5),
    ]
    random.shuffle(params)

    # Setup printing
    max_len = 45
    msg = "[Any spinner you like]"

    for name, period in params:
        spinner = getattr(Spinners, name)

        spaces_qty = max_len - len(name) - len(msg) - len(spinner.frames[0])
        text = "{0}{1}{2}".format(name, " " * spaces_qty, msg)

        with yaspin(spinner, text=text, color="cyan"):
            time.sleep(period)


def colors_simple():
    # Setup printing
    max_len = 25
    msg = "[Colors]"

    with yaspin(Spinners.dots12) as sp:
        colors = ("red", "green", "yellow", "blue", "magenta", "cyan", "white")

        for color in colors:
            spaces_qty = max_len - len(color) - len(msg)
            text = "{0}{1}{2}".format(color, " " * spaces_qty, msg)

            sp.color = color
            sp.text = text
            time.sleep(0.7)


def color_highlights():
    setups = [
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
    # Setup printing
    max_len = 40
    msg = "[Color Highlights]"

    with yaspin(Spinners.bouncingBall) as sp:

        for name, color_func in setups:
            spaces_qty = max_len - len(name) - len(msg)
            text = "{0}{1}{2}".format(name, " " * spaces_qty, msg)

            sp.color = color_func
            sp.text = text

            time.sleep(0.5)


def color_attributes():
    setups = [
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
    ]
    # Setup printing
    max_len = 42
    msg = "[Color Attributes]"

    with yaspin(Spinners.bouncingBall) as sp:

        for name, color_func in setups:
            spaces_qty = max_len - len(name) - len(msg)
            text = "{0}{1}{2}".format(name, " " * spaces_qty, msg)

            sp.color = color_func
            sp.text = text

            time.sleep(0.8)


def color_craziness():
    setups = [
        (
            "Bold underline reverse cyan color",
            lambda frame: colored(frame, 'cyan', attrs=['bold', 'underline', 'reverse'])  # noqa
        ),
        (
            "Dark blink concealed white color",
            lambda frame: colored(frame, 'white', attrs=['dark', 'blink', 'concealed'])  # noqa
        ),
        (
            "Underline red on grey color",
            lambda frame: colored(frame, 'red', 'on_grey', attrs=['underline'])
        ),
        (
            "Reversed green on red color",
            lambda frame: colored(frame, 'green', 'on_red', attrs=['reverse'])
        ),
    ]
    # Setup printing
    max_len = 58
    msg = "[Color Craziness 🙀 ]"

    with yaspin(Spinners.pong) as sp:

        for name, color_func in setups:
            spaces_qty = max_len - len(name) - len(msg)
            text = "{0}{1}{2}".format(name, " " * spaces_qty, msg)

            sp.color = color_func
            sp.text = text

            time.sleep(1.3)


def right_spinner():
    with yaspin(text="Right spinner", right=True, color="cyan") as sp:
        time.sleep(2)

        # Switch to left spinner
        sp.right = False
        sp.text = "Left spinner"

        time.sleep(2)


def reversed_spinner():
    with yaspin(text="Reversed spinner", reverse=True, color="cyan") as sp:
        time.sleep(1)

        sp.spinner = Spinners.line

        time.sleep(1)

        sp.text = "Enjoy!"
        sp.ok('☀️')


def main():
    any_spinner_you_like()
    colors_simple()
    color_highlights()
    color_attributes()
    color_craziness()
    right_spinner()
    reversed_spinner()


if __name__ == '__main__':
    main()
