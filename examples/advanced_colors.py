"""
examples.advanced_colors
~~~~~~~~~~~~~~~~~~~~~~~~

Use familiar API of the `termcolor.colored` function to apply any
color, highlight, attribute or their mix to your yaspin spinner.
"""

import time

from yaspin import yaspin


def white_shark():
    # Set with attributes
    with yaspin().white.bold.shark.on_blue as sp:
        sp.text = "White bold shark in a blue sea 🦈"
        time.sleep(5)


def ping_pong():
    # Set with attributes
    with yaspin(text="🏓").yellow.bold.underline.pong.on_blue:
        time.sleep(5)


def ball():
    # Set with arguments
    with yaspin(
        color="white",
        on_color="on_magenta",
        attrs=["dark", "blink", "concealed"],
    ).bouncingBall as sp:
        sp.text = "Dark blink concealed white ball on magenta color"
        time.sleep(5)


def main():
    white_shark()
    ping_pong()
    ball()


if __name__ == "__main__":
    main()
