# -*- coding: utf-8 -*-

"""
tests.test_in_out
~~~~~~~~~~~~~~~~~

Checks that all input data is converted to unicode.
And all output data is converted to builtin str type.
"""

import pytest

from yaspin import Spinner, yaspin
from yaspin.compat import PY2, basestring, builtin_str, str
from yaspin.constants import ENCODING


def test_input_converted_to_unicode(text, frames, interval, right, reverse):
    sp = Spinner(frames, interval)
    swirl = yaspin(sp, text, right=right, reverse=reverse)

    if isinstance(swirl._frames, basestring):
        assert isinstance(swirl._frames, str)

    if isinstance(swirl._frames, (list, tuple)):
        assert isinstance(swirl._frames[0], str)

    assert isinstance(swirl._text, str)


def test_out_converted_to_builtin_str(text, frames, interval, right, reverse):
    sp = Spinner(frames, interval)
    swirl = yaspin(sp, text, right=right, reverse=reverse)

    for _ in range(len(frames)):
        frame = next(swirl._cycle)
        out = swirl._compose_out(frame)
        assert isinstance(out, builtin_str)


def test_repr(text, frames, interval):
    sp = Spinner(frames, interval)
    swirl = yaspin(sp, text)

    assert isinstance(repr(swirl), builtin_str)


def test_compose_out_with_color(colors_test_cases):
    color, expected = colors_test_cases

    # Skip non relevant cases
    empty = not expected
    is_exc = isinstance(expected, Exception)
    func = callable(expected)

    if empty or is_exc or func:
        pytest.skip("{0} - unsupported case".format(repr(expected)))

    # Actual test
    swirl = yaspin(color=color)
    out = swirl._compose_out(frame=u'/')
    assert out.startswith('\r\033')
    assert isinstance(out, builtin_str)


def test_write(capsys, text):
    swirl = yaspin()
    swirl.write(text)

    out, _ = capsys.readouterr()
    # cleans stdout from _clear_line and \r
    out = out.replace('\r\033[K', '')

    # handle out and text encodings (come out messy in PY2)
    # Under PY2 ``capsys.readouterr`` always produces ``out``
    # of type ``unicode``. Conversion to bytes is required
    # for proper ``out`` and ``text`` comparison.
    if PY2:
        out = out.encode(ENCODING)
        if isinstance(text, str):
            text = text.encode(ENCODING)

    assert isinstance(out, basestring)
    assert out[-1] == '\n'
    if text:
        assert out[:-1] == text
