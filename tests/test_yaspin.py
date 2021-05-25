"""
tests.test_yaspin
~~~~~~~~~~~~~~~~~

Basic unittests.
"""

from collections import namedtuple

import pytest

from yaspin import Spinner, yaspin
from yaspin.base_spinner import default_spinner


@pytest.mark.parametrize(
    "spinner, expected",
    [
        # None
        (None, default_spinner),
        # hasattr(spinner, "frames") and not hasattr(spinner, "interval")
        (namedtuple("Spinner", "frames")("-\\|/"), default_spinner),
        # not hasattr(spinner, "frames") and hasattr(spinner, "interval")
        (namedtuple("Spinner", "interval")(42), default_spinner),
        # Both attrs, not set
        (Spinner("", 0), default_spinner),
        # Both attrs, not frames
        (Spinner("", 42), default_spinner),
        # Both attrs, not interval
        (Spinner("-\\|/", 0), default_spinner),
        # Both attrs, are set
        (Spinner("-\\|/", 42), Spinner("-\\|/", 42)),
    ],
    ids=[
        "None",
        "no `interval` attr",
        "no `frames` attr",
        "attrs not set",
        "`frames` not set",
        "`interval` not set",
        "both attrs are set",
    ],
)
def test_set_spinner(spinner, expected):
    sp = yaspin(spinner)
    assert sp.spinner == expected
