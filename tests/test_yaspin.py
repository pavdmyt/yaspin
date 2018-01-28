# -*- coding: utf-8 -*-

"""
tests.test_yaspin
~~~~~~~~~~~~~~~~~

Basic unittests.
"""

from __future__ import absolute_import

from collections import namedtuple

import pytest

from yaspin import Spinner, yaspin
from yaspin.base_spinner import default_spinner
from yaspin.compat import builtin_str


ids = [
    "default frames and interval",
    "str text, str frames",
    "unicode text, unicode frames (marked as unicode)",
    "unicode text, str frames",
    "str text, unicode frames",
    "str text, List[] frames",
    "str text, List[bytes] frames",
    "str text, List[unicode] frames",
    "str text, Tuple[] frames",
    "str text, Tuple[bytes] frames",
    "str text, Tuple[unicode] frames",
]


test_cases = [
    # default frames and interval
    ("", "", None),

    # str text, str frames
    ("Loading", "+x*", 80),

    # unicode text, unicode frames (marked as unicode)
    (u"Загрузка", u"⢄⢂⢁⡁⡈⡐⡠", 80),

    # unicode text, str frames
    ("ℙƴ☂ℌøἤ", "+x*", 80),

    # str text, unicode frames
    ("Loading", "⢄⢂⢁⡁⡈⡐⡠", 80),

    #
    # Iter frames
    #

    # TODO: add custom type that Implements iterable
    #
    # XXX: this is Bad, because different text inputs should
    #      combine with different frames input

    # str text, List[] frames
    ("Empty list", [], 400),

    # str text, List[bytes] frames
    ("Bytes list", [b"\xf0\x9f\x8c\xb2", b"\xf0\x9f\x8e\x84"], 400),

    # str text, List[unicode] frames
    ("Unicode list", [u"🌲", u"🎄"], 400),

    # str text, Tuple[] frames
    ("Empty tuple", (), 400),

    # str text, Tuple[bytes] frames
    ("Bytes tuple", (b"\xf0\x9f\x8c\xb2", b"\xf0\x9f\x8e\x84"), 400),

    # str text, Tuple[unicode] frames
    ("Unicode tuple", (u"🌲", u"🎄"), 400),
]


@pytest.mark.parametrize("spinner, expected", [
    # None
    (None, default_spinner),

    # hasattr(spinner, "frames") and not hasattr(spinner, "interval")
    (namedtuple('Spinner', "frames")("-\\|/"), default_spinner),

    # not hasattr(spinner, "frames") and hasattr(spinner, "interval")
    (namedtuple('Spinner', "interval")(42), default_spinner),

    # Both attrs, not set
    (Spinner("", 0), default_spinner),

    # Both attrs, not frames
    (Spinner("", 42), default_spinner),

    # Both attrs, not interval
    (Spinner("-\\|/", 0), default_spinner),

    # Both attrs, are set
    (Spinner("-\\|/", 42), Spinner("-\\|/", 42)),
])
def test_set_spinner(spinner, expected):
    swirl = yaspin(spinner)
    assert swirl.spinner == expected


def test_ok():
    swirl = yaspin()
    swirl.ok()

    assert isinstance(swirl._last_frame, builtin_str)
    assert swirl._last_frame[-1] == "\n"


def test_fail():
    swirl = yaspin()
    swirl.fail()

    assert isinstance(swirl._last_frame, builtin_str)
    assert swirl._last_frame[-1] == "\n"
