"""
tests.test_cursor
~~~~~~~~~~~~~~~~~

Check that the cursor is hidden for the whole spinner run and only
shown while paused, at ``stop()``, or when thread start fails.
"""

from unittest import mock

import io
import re
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


@pytest.mark.parametrize("error_type", [RuntimeError, KeyboardInterrupt, SystemExit])
def test_cursor_shown_when_thread_start_fails(error_type):
    stream = _FakeTTY()
    sp = yaspin(Spinner("-|/", 80), text="x", stream=stream)

    error = error_type("boom")
    with mock.patch("threading.Thread.start", side_effect=error), pytest.raises(error_type) as exc_info:
        sp.start()

    assert exc_info.value is error

    # The cursor must be restored when the thread cannot be started.
    assert "\033[?25h" in stream.getvalue()


@pytest.mark.parametrize("stream_type", [_FakeTTY, io.StringIO], ids=["tty", "non-tty"])
def test_cursor_visibility_during_hide_show(stream_type):
    stream = stream_type()
    sp = yaspin(stream=stream)
    sp.start()

    def cursor_codes():
        return re.findall(r"\033\[\?25[lh]", stream.getvalue())

    try:
        sp.hide()
        expected = ["\033[?25l", "\033[?25h"] if stream.isatty() else []
        assert cursor_codes() == expected
        sp.hide()
        assert cursor_codes() == expected

        sp.show()
        if stream.isatty():
            expected.append("\033[?25l")
        assert cursor_codes() == expected
        sp.show()
        assert cursor_codes() == expected
    finally:
        sp.stop()

    if stream.isatty():
        expected.append("\033[?25h")
    assert cursor_codes() == expected


@pytest.mark.parametrize("stream_type", [_FakeTTY, io.StringIO], ids=["tty", "non-tty"])
@pytest.mark.parametrize("raise_error", [False, True], ids=["normal", "exception"])
def test_cursor_visibility_in_nested_hidden_context(stream_type, raise_error):
    stream = stream_type()
    sp = yaspin(stream=stream)
    sp.start()

    def cursor_codes():
        return re.findall(r"\033\[\?25[lh]", stream.getvalue())

    expected = ["\033[?25l", "\033[?25h"] if stream.isatty() else []
    try:
        try:
            with sp.hidden():
                assert cursor_codes() == expected
                with sp.hidden():
                    assert cursor_codes() == expected
                assert cursor_codes() == expected
                if raise_error:
                    raise ValueError("prompt failed")
        except ValueError:
            if not raise_error:
                raise

        if stream.isatty():
            expected.append("\033[?25l")
        assert cursor_codes() == expected
        assert sp._hidden_level == 0
        assert not sp._hide_spin.is_set()
    finally:
        sp.stop()

    if stream.isatty():
        expected.append("\033[?25h")
    assert cursor_codes() == expected
