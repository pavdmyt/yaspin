# -*- coding: utf-8 -*-

"""
tests.test_in_out
~~~~~~~~~~~~~~~~~

Checks that all input data is converted to unicode.
And all output data is converted to builtin str type.
"""

from yaspin import Spinner, yaspin
from yaspin.compat import builtin_str, str, basestring


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
