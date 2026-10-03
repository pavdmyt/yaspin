"""
tests.test_cursor
~~~~~~~~~~~~~~~~~

Check that the cursor is hidden for the whole spinner run and only
shown again at ``stop()`` (or when thread start fails).
"""

from unittest import mock

import io
import time

import pytest

from yaspin import yaspin
from yaspin.core import Spinner


class _FakeTTY(io.StringIO):
    """A stream that behaves like a terminal."""

    def isatty(self):
        return True


def test_cursor_stays_hidden_between_start_and_stop():
    stream = _FakeTTY()
    sp = yaspin(Spinner("-|/", 80), text="Loading", stream=stream)
    sp.start()

    try:
        time.sleep(0.25)
        out = stream.getvalue()
        # The cursor was hidden once, at start().
        assert out.count("\033[?25l") == 1
        # And it must not be shown back until stop().
        assert "\033[?25h" not in out
    finally:
        sp.stop()

    # Exactly one show, emitted by stop().
    assert stream.getvalue().count("\033[?25h") == 1


def test_cursor_shown_when_thread_start_fails():
    stream = _FakeTTY()
    sp = yaspin(Spinner("-|/", 80), text="x", stream=stream)

    with mock.patch("threading.Thread.start", side_effect=RuntimeError("boom")):
        with pytest.raises(RuntimeError):
            sp.start()

    # The cursor must be restored when the thread cannot be started.
    assert "\033[?25h" in stream.getvalue()
