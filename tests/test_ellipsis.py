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
