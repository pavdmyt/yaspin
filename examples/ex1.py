# -*- coding: utf-8 -*-

import time
import yaspin


def context_manager_default():
    with yaspin.spinner(text="Braille"):
        time.sleep(3)


def context_manager_line():
    with yaspin.spinner("Line", '-\\|/', 0.15):
        time.sleep(3)


@yaspin.spinner("Dots", "⢄⢂⢁⡁⡈⡐⡠", 0.08)
def decorated_function():
    time.sleep(3)


def main():
    context_manager_default()
    context_manager_line()
    decorated_function()


if __name__ == '__main__':
    main()
