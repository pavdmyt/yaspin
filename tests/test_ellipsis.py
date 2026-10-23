from io import StringIO
from unittest.mock import patch

import shutil
import threading
import time

import pytest

from yaspin import yaspin


def test_wo_ellipsis():
    sp = yaspin()
    frame, timer = 2, 10
    max_len = shutil.get_terminal_size().columns - (frame + len(" ") + timer)

    assert sp._get_max_text_length(frame, timer) == max_len


def test_with_ellipsis():
    ellipsis = "..."
    sp = yaspin(ellipsis=ellipsis)
    frame, timer = 2, 10
    max_len = shutil.get_terminal_size().columns - (frame + len(" ") + timer + len(ellipsis))
    assert sp._get_max_text_length(frame, timer) == max_len


@pytest.mark.parametrize("isatty", [False, True], ids=["non-tty", "tty"])
@pytest.mark.parametrize("side", ["left", "right"])
@pytest.mark.parametrize("mode", [None, "last"], ids=["live", "final"])
@pytest.mark.parametrize("timer", [False, " ({})"], ids=["no-timer", "custom-timer"])
@pytest.mark.parametrize(
    "text, expected_text",
    [
        ("abcde", "abcde"),
        ("abcdef", "abcdef"),
        ("abcdefgh", "abcdefgh"),
        ("abcdefghi", "abcde..."),
    ],
    ids=["short", "fits-without-ellipsis", "exact-fit", "overflow"],
)
def test_ellipsis_only_truncates_overflowing_text(
    monkeypatch, isatty, side, mode, timer, text, expected_text
):
    stream = StringIO()
    monkeypatch.setattr(stream, "isatty", lambda: isatty)
    sp = yaspin(text=text, ellipsis="...", side=side, timer=timer, stream=stream)
    timer_text = " (0:00:00)" if timer else ""
    sp._terminal_width = len("* ") + 8 + len(timer_text)
    body = f"* {expected_text}" if side == "left" else f"{expected_text} *"
    expected = f"\r{body}{timer_text}" if mode is None else f"{body}{timer_text}\n"

    assert sp._compose_out("*", mode=mode) == expected


@patch("shutil.get_terminal_size")
def test_terminal_size_called_once(mock_get_terminal_size):
    mock_get_terminal_size.return_value.columns = 80
    sp = yaspin(ellipsis="...")

    @sp
    def long_running_function():
        time.sleep(0.2)

    long_running_function()
    mock_get_terminal_size.assert_called_once()


@patch("shutil.get_terminal_size")
def test_raises_when_term_is_too_small(mock_get_terminal_size):
    mock_get_terminal_size.return_value.columns = 10
    sp = yaspin(ellipsis="..." * 5)

    with pytest.raises(ValueError):
        # Some low-level trickery is needed here because Yaspin._compose_out()
        # is called in a separate thread and the exception is not propagated.
        # Pytest indicates that by warnings.warn(pytest.PytestUnhandledThreadExceptionWarning(msg))
        sp._stop_spin = threading.Event()
        sp._spin()
