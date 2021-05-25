"""
examples.basic_usage
~~~~~~~~~~~~~~~~~~~~

Common usage patterns for the yaspin spinner.
"""

import signal
import time

from yaspin import Spinner, yaspin
from yaspin.signal_handlers import fancy_handler
from yaspin.spinners import Spinners


def context_manager_default():
    with yaspin(text="Braille"):
        time.sleep(3)


def context_manager_line():
    line_spinner = Spinner("-\\|/", 150)
    with yaspin(line_spinner, "line"):
        time.sleep(3)


@yaspin(Spinner("⢄⢂⢁⡁⡈⡐⡠", 80), text="Dots")
def decorated_function():
    time.sleep(3)


def pre_setup_example():
    swirl = yaspin(
        spinner=Spinners.simpleDotsScrolling,
        text="swirl",
        color="red",
        side="right",
        sigmap={signal.SIGINT: fancy_handler},
    )

    with swirl as sp:
        time.sleep(2)

    with swirl as sp:
        sp.text = "new swirl"
        sp.reversal = True
        time.sleep(2)


def main():
    context_manager_default()
    context_manager_line()
    decorated_function()
    pre_setup_example()


if __name__ == "__main__":
    main()
