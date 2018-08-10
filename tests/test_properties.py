# -*- coding: utf-8 -*-

"""
tests.test_properties
~~~~~~~~~~~~~~~~~~~~~

Test getters and setters.
"""

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
# Yaspin.reversal
#
def test_reversal_getter(reversal):
    swirl = yaspin(reversal=reversal)
    assert swirl.reversal == reversal


def test_reversal_setter(reversal):
    swirl = yaspin()
    swirl.reversal = reversal
    assert isinstance(swirl._frames, str)
    assert swirl._reversal == reversal


#
# Yaspin.color
#
def test_color_getter(supported_colors):
    color = supported_colors
    swirl = yaspin(color=color)
    assert swirl.color == color


def test_color_setter(color_test_cases):
    color, expected = color_test_cases
    swirl = yaspin()

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            swirl.color = color
    else:
        swirl.color = color
        assert swirl._color == expected


#
# Yaspin.on_color
#
def test_on_color_getter(supported_highlights):
    on_color = supported_highlights
    swirl = yaspin(on_color=on_color)
    assert swirl.on_color == on_color


def test_on_color_setter(on_color_test_cases):
    on_color, expected = on_color_test_cases
    swirl = yaspin()

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            swirl.on_color = on_color
    else:
        swirl.on_color = on_color
        assert swirl._on_color == expected


#
# Yaspin.attrs
#
def test_attrs_getter(supported_attrs):
    attrs = supported_attrs
    swirl = yaspin(attrs=attrs)
    assert set(swirl.attrs) == set(attrs)


def test_attrs_setter(attrs_test_cases):
    attrs, expected = attrs_test_cases
    swirl = yaspin()

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            swirl.attrs = attrs
    else:
        swirl.attrs = attrs
        assert swirl._attrs == set(expected)
