# -*- coding: utf-8 -*-

"""
tests.test_yaspin
~~~~~~~~~~~~~~~~~

Basic unittests.
"""

from __future__ import absolute_import

import os
import sys
from collections import namedtuple

import pytest

from yaspin import Spinner, yaspin
from yaspin.base_spinner import default_spinner
from yaspin.compat import builtin_str, bytes, str
from yaspin.constants import ENCODING


#
# Helpers
#
def to_bytes(str_or_bytes, encoding=ENCODING):
    if isinstance(str_or_bytes, str):
        return str_or_bytes.encode(encoding)
    return str_or_bytes


def to_unicode(str_or_bytes, encoding=ENCODING):
    if isinstance(str_or_bytes, bytes):
        return str_or_bytes.decode(encoding)
    return str_or_bytes


#
# Tests
#
test_cases = [
    # Default frames and interval
    ("", "", None),

    # str text, str frames
    ("Loading", "+x*", 80),

    # unicode text, unicode frames (marked as unicode)
    (u"Загрузка", u"⢄⢂⢁⡁⡈⡐⡠", 80),

    # unicode text, str frames
    ("Загрузка", "+x*", 80),

    # str text, unicode frames
    ("Loading", "⢄⢂⢁⡁⡈⡐⡠", 80),
]


@pytest.mark.parametrize("text, frames, interval", test_cases)
def test_input_converted_to_unicode(text, frames, interval):
    sp = Spinner(frames, interval)
    swirl = yaspin(sp, text)

    assert isinstance(swirl._frames, str)
    assert isinstance(swirl._text, str)


@pytest.mark.parametrize("text, frames, interval", test_cases)
def test_output_converted_to_builtin_str(text, frames, interval):
    sp = Spinner(frames, interval)
    swirl = yaspin(sp, text)

    for _ in range(20):             # test 20 frames
        out = swirl.compose_frame()
        assert isinstance(out, builtin_str)


@pytest.mark.parametrize("text, frames, interval", test_cases)
def test_repr(text, frames, interval):
    sp = Spinner(frames, interval)
    swirl = yaspin(sp, text)

    assert isinstance(repr(swirl), builtin_str)


@pytest.mark.parametrize("text, frames, interval", test_cases)
def test_piping_output(text, frames, interval):
    py_fname = "spin.py"
    fname = "out.txt"

    def teardown():
        os.remove(py_fname)
        os.remove(fname)

    code = """\
# -*- coding: utf-8 -*-

import time
from yaspin import yaspin, Spinner

with yaspin(Spinner('%s', %s), '%s'):
    time.sleep(0.5)
"""

    with open(py_fname, 'wb') as f:
        text = to_unicode(text)
        frames = to_unicode(frames)
        interval = to_unicode(interval)
        code = to_unicode(code)
        res = code % (frames, interval, text)
        f.write(to_bytes(res))

    try:
        # $ python spin.py > out.txt
        os.system("{0} {1} > {2}".format(sys.executable, py_fname, fname))
    except UnicodeEncodeError as err:
        pytest.fail(err)
    finally:
        teardown()


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
