# -*- coding: utf-8 -*-

"""
tests.test_in_out
~~~~~~~~~~~~~~~~~

Checks that all input data is converted to unicode.
And all output data is converted to builtin str type.
"""

import sys

import pytest

from yaspin import Spinner, yaspin
from yaspin.compat import PY2, basestring, builtin_str, str
from yaspin.constants import ENCODING
from yaspin.helpers import to_unicode


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


def test_hide_show(capsys, text, request):
    # Setup
    swirl = yaspin()
    swirl.start()

    # Ensure that swirl.stop() will be executed
    def teardown():
        swirl.stop()
    request.addfinalizer(teardown)

    #
    # Actual test
    #
    swirl.hide()

    # ensure that hidden spinner flag was set
    assert swirl._hide_spin.is_set()
    out, _ = capsys.readouterr()

    # ensure that text was cleared with the hide method
    assert out[-4:] == '\r\033[K'

    # properly encode text to unicode if running in PY2
    if PY2:
        text = to_unicode(text).encode(ENCODING)

    # ``\n`` is required to flush stdout during
    # the hidden state of the spinner
    sys.stdout.write('{0}\n'.format(text))
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

    swirl.show()

    # ensure that hidden spinner flag was cleared
    assert not swirl._hide_spin.is_set()
    out, _ = capsys.readouterr()

    # ensure that text was cleared before resuming the spinner
    assert out[:4] == '\r\033[K'
