# -*- coding: utf-8 -*-

import time

from yaspin import Spinner, yaspin


def context_manager_default():
    with yaspin(text="Braille"):
        time.sleep(3)


def context_manager_line():
    line_spinner = Spinner('-\\|/', 150)
    with yaspin(line_spinner, "line"):
        time.sleep(3)


@yaspin(Spinner("⢄⢂⢁⡁⡈⡐⡠", 80), text="Dots")
def decorated_function():
    time.sleep(3)


def main():
    context_manager_default()
    context_manager_line()
    decorated_function()


if __name__ == '__main__':
    main()
