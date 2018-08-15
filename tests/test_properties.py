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
    sp = yaspin()
    assert sp.spinner == default_spinner

    new_spinner = Spinner(frames, interval)
    sp.spinner = new_spinner
    assert sp.spinner == sp._set_spinner(new_spinner)


def test_spinner_setter(frames, interval):
    sp = yaspin()
    assert sp._spinner == default_spinner
    assert isinstance(sp._frames, str)
    assert sp._interval == sp._spinner.interval * 0.001
    assert isinstance(repr(sp), builtin_str)

    new_spinner = Spinner(frames, interval)
    sp.spinner = new_spinner
    assert sp._spinner == sp._set_spinner(new_spinner)

    if isinstance(sp._frames, basestring):
        assert isinstance(sp._frames, str)

    if isinstance(sp._frames, (list, tuple)):
        assert isinstance(sp._frames[0], str)

    assert sp._interval == sp._spinner.interval * 0.001
    assert isinstance(repr(sp), builtin_str)


#
# Yaspin.text
#
def test_text_getter(text):
    sp = yaspin(text=text)
    assert sp.text == to_unicode(text)


def test_text_setter(text):
    sp = yaspin()
    sp.text = text
    assert isinstance(sp._text, str)
    assert sp._text == to_unicode(text)


#
# Yaspin.side
#
def test_side_getter(side):
    sp = yaspin(side=side)
    assert sp.side == side


@pytest.mark.parametrize(
    "side, expected",
    [("left", "left"), ("right", "right"), ("center", ValueError())],
)
def test_side_setter(side, expected):
    sp = yaspin()
    assert sp._side == "left"

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            sp.side = side
    else:
        sp.side = side
        assert sp._side == expected


#
# Yaspin.reversal
#
def test_reversal_getter(reversal):
    sp = yaspin(reversal=reversal)
    assert sp.reversal == reversal


def test_reversal_setter(reversal):
    sp = yaspin()
    sp.reversal = reversal
    assert isinstance(sp._frames, str)
    assert sp._reversal == reversal


#
# Yaspin.color
#
def test_color_getter(supported_colors):
    color = supported_colors
    sp = yaspin(color=color)
    assert sp.color == color


def test_color_setter(color_test_cases):
    color, expected = color_test_cases
    sp = yaspin()

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            sp.color = color
    else:
        sp.color = color
        assert sp._color == expected


#
# Yaspin.on_color
#
def test_on_color_getter(supported_highlights):
    on_color = supported_highlights
    sp = yaspin(on_color=on_color)
    assert sp.on_color == on_color


def test_on_color_setter(on_color_test_cases):
    on_color, expected = on_color_test_cases
    sp = yaspin()

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            sp.on_color = on_color
    else:
        sp.on_color = on_color
        assert sp._on_color == expected


#
# Yaspin.attrs
#
def test_attrs_getter(supported_attrs):
    attrs = supported_attrs
    sp = yaspin(attrs=attrs)
    assert set(sp.attrs) == set(attrs)


def test_attrs_setter(attrs_test_cases):
    attrs, expected = attrs_test_cases
    sp = yaspin()

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            sp.attrs = attrs
    else:
        sp.attrs = attrs
        assert sp._attrs == set(expected)
