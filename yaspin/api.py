# -*- coding: utf-8 -*-

"""
yaspin.api
~~~~~~~~~~

This module implements the Yaspin API.

:copyright: (c) 2018 by Pavlo Dmytrenko.
:license: MIT, see LICENSE for more details.
"""

import signal

from .core import Yaspin
from .signal_handlers import default_handler


# TODO: add description for the ``sigmap`` argument.
# TODO: add description for the ``on_color`` argument.
# TODO: add description for the ``attrs`` argument.
def yaspin(*args, **kwargs):
    """Display spinner in stdout.

    Can be used as a context manager or as a function decorator.

    Arguments:
        spinner (yaspin.Spinner, optional): Spinner to use.
        text (str, optional): Text to show along with spinner.
        color (str, callable, optional): Color or color style of the spinner.
        reversal (bool, optional): Reverse spin direction.
        side (str, optional): Place spinner to the right or left end
            of the text string.

    Returns:
        yaspin.Yaspin: instance of the Yaspin class.

    Raises:
        ValueError: If unsupported `color` is specified.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white,
        on_grey.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Example::

        # Use as a context manager
        with yaspin():
            some_operations()

        # Context manager with text
        with yaspin(text="Processing..."):
            some_operations()

        # Context manager with custom sequence
        with yaspin(Spinner('-\\|/', 150)):
            some_operations()

        # As decorator
        @yaspin(text="Loading...")
        def foo():
            time.sleep(5)

        foo()

    """
    return Yaspin(*args, **kwargs)


def kbi_safe_yaspin(*args, **kwargs):
    kwargs["sigmap"] = {signal.SIGINT: default_handler}
    return Yaspin(*args, **kwargs)


kbi_safe_yaspin.__doc__ = yaspin.__doc__
