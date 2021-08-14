"""
examples.signals
~~~~~~~~~~~~~~~~

Handling signals.

Reference
---------

- Signals in a nutshell:
    https://twitter.com/b0rk/status/981678748763414529

- More detailed overview:
    https://jvns.ca/blog/2016/06/13/should-you-be-scared-of-signals/

- Python signal module examples:
    https://pymotw.com/3/signal/index.html

- Linux signals reference:
    https://www.computerhope.com/unix/signals.htm#linux

"""

import os
import random
import signal
import sys
import time

from yaspin import kbi_safe_yaspin, yaspin
from yaspin.signal_handlers import fancy_handler
from yaspin.spinners import Spinners


DEFAULT_TEXT = "Press Control+C to send SIGINT (Keyboard Interrupt) signal"


#
# Basic usage
#
def simple_keyboard_interrupt_handling():
    with kbi_safe_yaspin(text=DEFAULT_TEXT):
        time.sleep(5)


# Set the handler for signal signalnum to the function handler.
# Handler can be a callable Python object taking two arguments,
# or one of the special values signal.SIG_IGN or signal.SIG_DFL.
def fancy_keyboard_interrupt_handler():
    with yaspin(sigmap={signal.SIGINT: fancy_handler}, text=DEFAULT_TEXT):
        time.sleep(5)


#
# Customizing signal handlers
#
def custom_signal_handler():
    def my_handler(signum, frame, spinner):
        spinner.red.fail("[Received SIGINT]")
        spinner.stop()
        sys.exit(0)

    with yaspin(sigmap={signal.SIGINT: my_handler}, text=DEFAULT_TEXT):
        time.sleep(5)


def passing_additional_info_into_signal_handler():
    heads = random.randint(0, 1) == 1
    tails = not heads

    def my_handler(signum, frame, spinner, context={"heads": heads, "tails": tails}):
        if context["heads"]:
            spinner.text = "heads!"
            spinner.ok("🌕")
        if context["tails"]:
            spinner.text = "tails!"
            spinner.ok("⚪")

        spinner.stop()
        sys.exit(0)

    with yaspin(sigmap={signal.SIGINT: my_handler}).toggle8 as sp:
        sp.text = "Tossing a coin... Press Control-C to view the result"
        time.sleep(10)
        sp.write("The coin has disappeared")


def handling_multiple_signals():
    def my_handler(signum, frame, spinner):
        if signum == int(signal.SIGUSR1):
            spinner.green.ok("[SIGUSR1]")
        if signum == int(signal.SIGTERM):
            spinner.red.ok("[SIGTERM]")

        spinner.stop()
        sys.exit(0)

    sigmap = {signal.SIGUSR1: my_handler, signal.SIGTERM: my_handler}

    with yaspin(sigmap=sigmap, text="Handling SIGUSR1 and SIGTERM") as sp:
        sp.write("Send signals using `kill` command")
        sp.write("E.g. $ kill -USR1 {0}".format(os.getpid()))
        time.sleep(60)
        sp.write("No signal received")


def ignore_signal():
    with yaspin(sigmap={signal.SIGINT: signal.SIG_IGN}, text="You can't interrupt me!"):
        time.sleep(5)


def default_os_handler_for_sigint():
    # Python sets ``signal.default_int_handler`` as a default handler
    # for SIGINT. It raises KeyboardInterrupt exception. It is also
    # possible to set default OS behavior for SIGINT by setting
    # ``signal.SIG_DFL`` as a signal handler.
    #
    # Generally ``signal.SIG_DFL`` performs the default function for the
    # signal.
    with yaspin(
        sigmap={signal.SIGINT: signal.SIG_DFL},
        text="Default OS handler for SIGINT",
    ):
        time.sleep(5)


#
# Real-world examples
#
def unpacker():
    swirl = yaspin(
        spinner=Spinners.simpleDotsScrolling,
        sigmap={signal.SIGINT: fancy_handler},
        side="right",
    )
    with swirl as sp:
        for p in range(0, 101, 5):
            sp.text = "{0}% Unpacking".format(p)
            time.sleep(random.random())
        sp.green.ok("✔")


def main():
    simple_keyboard_interrupt_handling()
    fancy_keyboard_interrupt_handler()
    custom_signal_handler()
    passing_additional_info_into_signal_handler()
    handling_multiple_signals()
    ignore_signal()
    default_os_handler_for_sigint()
    unpacker()


if __name__ == "__main__":
    main()
