# :copyright: (c) 2021 by Pavlo Dmytrenko.
# :license: MIT, see LICENSE for more details.

"""
yaspin.api
~~~~~~~~~~

This module implements the Yaspin API.
"""

from typing import Any, Callable, TypeVar

import functools
import signal

from .core import default_handler, Yaspin

T = TypeVar("T")


def yaspin(*args: Any, **kwargs: Any) -> Yaspin:
    """Display spinner in stdout (default) or a custom stream.

    Can be used as a context manager or as a function decorator.

    Arguments:
        spinner (core.Spinner, optional): Spinner object to use.
        text (str, optional): Text to show along with spinner.
        color (str, optional): Spinner color.
        on_color (str, optional): Color highlight for the spinner.
        attrs (list, optional): Color attributes for the spinner.
        reversal (bool, optional): Reverse spin direction.
        side (str, optional): Place spinner to the right or left end
            of the text string.
        sigmap (dict, optional): Maps POSIX signals to their respective
            handlers.
        timer (bool, optional): Prints a timer showing the elapsed time.
        ellipsis (str, optional): Sets a custom ellipsis to signal text
            truncation due to overflow.
        stream (TextIO, optional): Output stream for the spinner. Defaults
            to sys.stdout. Use sys.stderr to display spinner on stderr while
            redirecting stdout to a file.
        warn_on_closed_stream (bool, optional): If True, emits a warning
            when attempting to write to a closed stream. Useful for debugging
            stream lifecycle issues. Defaults to False for silent operation.

    Returns:
        core.Yaspin: instance of the Yaspin class.

    Raises:
        ValueError: If unsupported ``color`` is specified.
        ValueError: If unsupported ``on_color`` is specified.
        ValueError: If unsupported color attribute in ``attrs``
            is specified.
        ValueError: If trying to register handler for SIGKILL signal.
        ValueError: If unsupported ``side`` is specified.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan,
        on_white, on_grey.

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
        with yaspin(Spinner("-\\|/", 150)):
            some_operations()


        # As decorator
        @yaspin(text="Loading...")
        def foo():
            time.sleep(5)


        foo()

    """
    return Yaspin(*args, **kwargs)


def inject_spinner(*args: Any, **kwargs: Any) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator that injects a yaspin spinner into the decorated function.
    The spinner is passed as the first argument to the decorated function.

    Example:
        @inject_spinner(Spinners.dots, text="Processing...", color="green")
        def process_data(spinner: Yaspin, data: list) -> None:
            for i, item in enumerate(data):
                spinner.text = f"Processing item {i+1}/{len(data)}"
                # Process item...
            spinner.ok("✓")
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*func_args: Any, **func_kwargs: Any) -> T:
            with yaspin(*args, **kwargs) as spinner:
                return func(spinner, *func_args, **func_kwargs)

        return wrapper

    return decorator


def kbi_safe_yaspin(*args: Any, **kwargs: Any) -> Yaspin:
    """
    Create a Yaspin instance with a default signal handler for SIGINT.

    Wraps the Yaspin initialization to ensure that a default
    signal handler for SIGINT is set, which allows for safe interruption
    (KeyboardInterrupt) handling.

    Returns:
        Yaspin: An instance of the Yaspin spinner with the specified arguments and
        a default SIGINT handler.
    """
    kwargs["sigmap"] = {signal.SIGINT: default_handler}
    return Yaspin(*args, **kwargs)


# Handle PYTHONOPTIMIZE=2 case, when docstrings are set to None.
if yaspin.__doc__:
    _kbi_safe_doc = yaspin.__doc__.replace("yaspin", "kbi_safe_yaspin")
    kbi_safe_yaspin.__doc__ = _kbi_safe_doc
