# -*- coding: utf-8 -*-

"""
yaspin.yaspin
~~~~~~~~~~~~~

A lightweight terminal spinner.
"""

from __future__ import absolute_import

import functools
import itertools
import sys
import threading
import time

from .base_spinner import default_spinner
from .compat import PY2
from .constants import ENCODING
from .helpers import to_unicode


class Yaspin(object):
    """Implements a context manager that spawns a daemon thread
    that writes spinner frames into a tty (stdout) during
    context execution.

    Arguments:
        spinner (yaspin.Spinner): Spinner to use.
        text (str): Text to show along with spinner.

    """
    def __init__(self, spinner=None, text=''):
        self.spinner = self._set_spinner(spinner)

        # Milliseconds to Seconds
        self._interval = self.spinner.interval * 0.001

        if PY2:
            self._frames = to_unicode(self.spinner.frames)
            self._text = to_unicode(text).strip()
        else:
            self._frames = self.spinner.frames
            self._text = text.strip()

        self._cycle = itertools.cycle(self._frames)
        self._stop_spin = None
        self._spin_thread = None

    def __repr__(self):
        repr_ = u'<Yaspin frames={0!s}>'.format(self._frames)
        if PY2:
            return repr_.encode(ENCODING)
        return repr_

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.stop()
        return False  # nothing is handled

    def __call__(self, fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            with self:
                return fn(*args, **kwargs)
        return inner

    def start(self):
        if sys.stdout.isatty():
            self._hide_cursor()

        self._stop_spin = threading.Event()
        self._spin_thread = threading.Thread(target=self.spin)
        self._spin_thread.setDaemon(True)
        self._spin_thread.start()

    def stop(self):
        if self._spin_thread:
            self._stop_spin.set()
            self._spin_thread.join()

        sys.stdout.write("\r")
        self._clear_line()

        if sys.stdout.isatty():
            self._show_cursor()

    def compose_frame(self):
        spin_phase = next(self._cycle)
        if PY2:
            spin_phase = spin_phase.encode(ENCODING)
            text = self._text.encode(ENCODING)
        else:
            text = self._text

        return "\r{0} {1}".format(spin_phase, text)

    def spin(self):
        while not self._stop_spin.is_set():
            frame = self.compose_frame()
            sys.stdout.write(frame)
            sys.stdout.flush()
            time.sleep(self._interval)
            sys.stdout.write('\b')

    @staticmethod
    def _set_spinner(spinner):
        if not spinner:
            sp = default_spinner

        if hasattr(spinner, "frames") and hasattr(spinner, "interval"):
            if not spinner.frames or not spinner.interval:
                sp = default_spinner
            else:
                sp = spinner
        else:
            sp = default_spinner

        return sp

    @staticmethod
    def _hide_cursor():
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    @staticmethod
    def _show_cursor():
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    @staticmethod
    def _clear_line():
        sys.stdout.write("\033[K")


def yaspin(spinner=None, text=''):
    """Display spinner in stdout.

    Can be used as a context manager or as a function decorator.

    Arguments:
        spinner (yaspin.Spinner): Spinner to use.
        text (str): Text to show along with spinner.

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
    return Yaspin(spinner=spinner, text=text)
