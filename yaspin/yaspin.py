# -*- coding: utf-8 -*-

"""
yaspin.yaspin
~~~~~~~~~~~~~

A lightweight terminal spinner.
"""

import functools
import itertools
import sys
import threading
import time


PY2 = sys.version_info[0] == 2
ENCODING = 'utf-8'


def to_unicode(unicode_or_str, encoding=ENCODING):
    if isinstance(unicode_or_str, str):
        return unicode_or_str.decode(encoding)
    return unicode_or_str


class Yaspin(object):
    """Implements a context manager that spawns a daemon thread
    that writes spinner frames into a tty (stdout) during
    context execution.

    Arguments:
        text (str): Text to show along with spinner.
        sequence (str|unicode): Optional sequence of symbols to iterate
            over to render the the spinner. Defaults to dots spinner.
        interval (float): Interval between each symbol in sequence.

    """
    _default_seq = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    _default_interval = 0.08

    def __init__(self, text='', sequence='', interval=None):
        if sequence and interval:
            self._sequence = sequence
            self._interval = interval
        else:
            self._sequence = self._default_seq
            self._interval = self._default_interval

        if PY2:
            self._sequence = to_unicode(self._sequence)
            self._text = to_unicode(text).strip()
        else:
            self._text = text.strip()

        self._cycle = itertools.cycle(self._sequence)
        self._stop_spin = None
        self._spin_thread = None

    def __repr__(self):
        repr_ = u'<Yaspin sequence={0!s}>'.format(self._sequence)
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


def spinner(text='', sequence='', interval=None):
    """Display spinner in stdout.

    Can be used as a context manager or as a function decorator.

    Arguments:
        text (str): Text to show along with spinner.
        sequence (str|unicode): Optional sequence of symbols to iterate
            over to render the the spinner. Defaults to dots spinner.
        interval (float): Interval between each symbol in sequence.

    Example::

        # Use as a context manager
        with spinner():
            some_operations()

        # Context manager with text
        with spinner(text="Processing..."):
            some_operations()

        # Context manager with custom sequence
        with spinner(sequence='-\\|/', interval=0.15):
            some_operations()

        # As decorator
        @spinner(text="Loading...")
        def some_operations():
            time.sleep(5)

    """
    return Yaspin(text=text, sequence=sequence, interval=interval)
