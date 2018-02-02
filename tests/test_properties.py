# -*- coding: utf-8 -*-

"""
tests.test_properties
~~~~~~~~~~~~~~~~~~~~~

Test getters and setters.
"""

from inspect import getsource

import pytest

from yaspin import Spinner, yaspin
from yaspin.base_spinner import default_spinner
from yaspin.compat import basestring, builtin_str, str
from yaspin.helpers import to_unicode


#
# Yaspin.spinner
#
def test_spinner_getter(frames, interval):
    swirl = yaspin()
    assert swirl.spinner == default_spinner

    new_spinner = Spinner(frames, interval)
    swirl.spinner = new_spinner
    assert swirl.spinner == swirl._set_spinner(new_spinner)


def test_spinner_setter(frames, interval):
    swirl = yaspin()
    assert swirl._spinner == default_spinner
    assert isinstance(swirl._frames, str)
    assert swirl._interval == swirl._spinner.interval * 0.001
    assert isinstance(repr(swirl), builtin_str)

    new_spinner = Spinner(frames, interval)
    swirl.spinner = new_spinner
    assert swirl._spinner == swirl._set_spinner(new_spinner)

    if isinstance(swirl._frames, basestring):
        assert isinstance(swirl._frames, str)

    if isinstance(swirl._frames, (list, tuple)):
        assert isinstance(swirl._frames[0], str)

    assert swirl._interval == swirl._spinner.interval * 0.001
    assert isinstance(repr(swirl), builtin_str)


#
# Yaspin.text
#
def test_text_getter(text):
    swirl = yaspin(text=text)
    assert swirl.text == to_unicode(text)


def test_text_setter(text):
    swirl = yaspin()
    swirl.text = text
    assert isinstance(swirl._text, str)
    assert swirl._text == to_unicode(text)


#
# Yaspin.right
#
def test_right_getter(right):
    swirl = yaspin(right=right)
    assert swirl.right == right


def test_right_setter(right):
    swirl = yaspin()
    swirl.right = right
    assert swirl._right == right


#
# Yaspin.reverse
#
def test_reverse_getter(reverse):
    swirl = yaspin(reverse=reverse)
    assert swirl.reverse == reverse


def test_reverse_setter(reverse):
    swirl = yaspin()
    swirl.reverse = reverse
    assert isinstance(swirl._frames, str)
    assert swirl._reverse == reverse


#
# Yaspin.color
#
def test_color_getter(supported_colors):
    color = supported_colors
    swirl = yaspin(color=color)
    assert swirl.color == color


def test_color_setter(colors_test_cases):
    color, expected = colors_test_cases
    swirl = yaspin()

    # Exception
    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            swirl.color = color

    # Callable arg
    elif callable(color):
        # Compare source code to check funcs equality
        swirl.color = color
        fn1 = swirl._color
        fn2 = expected
        assert getsource(fn1) == getsource(fn2)

    # Common arg
    else:
        swirl.color = color
        assert swirl._color == expected
