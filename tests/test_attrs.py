# -*- coding: utf-8 -*-

"""
tests.test_attrs
~~~~~~~~~~~~~~~~

Test Yaspin attributes magic hidden in __getattr__.
"""

from __future__ import absolute_import

import pytest

from yaspin import yaspin
from yaspin.compat import iteritems
from yaspin.constants import COLOR_MAP, SPINNER_ATTRS
from yaspin.spinners import Spinners


@pytest.mark.parametrize("attr_name", SPINNER_ATTRS)
def test_set_spinner_by_name(attr_name):
    sp = getattr(yaspin(), attr_name)
    assert sp.spinner == getattr(Spinners, attr_name)


# Values for ``color`` argument
def test_color(color_test_cases):
    color, expected = color_test_cases
    # ``None`` and ``""`` are skipped
    if not color:
        pytest.skip("{0} - unsupported case".format(repr(color)))

    sp = yaspin()

    if isinstance(expected, Exception):
        with pytest.raises(AttributeError):
            getattr(sp, color)
    else:
        getattr(sp, color)
        assert sp.color == expected
        assert sp._color_func.keywords["color"] == expected


# Values for ``on_color`` argument
def test_on_color(on_color_test_cases):
    on_color, expected = on_color_test_cases
    # ``None`` and ``""`` are skipped
    if not on_color:
        pytest.skip("{0} - unsupported case".format(repr(on_color)))

    sp = yaspin()

    if isinstance(expected, Exception):
        with pytest.raises(AttributeError):
            getattr(sp, on_color)
    else:
        getattr(sp, on_color)
        assert sp.on_color == expected
        assert sp._color_func.keywords["on_color"] == expected


# Values for ``attrs`` argument
@pytest.mark.parametrize(
    "attr", [k for k, v in iteritems(COLOR_MAP) if v == "attrs"]
)
def test_attrs(attr):
    sp = yaspin()
    getattr(sp, attr)
    assert sp.attrs == [attr]
    assert sp._color_func.keywords["attrs"] == [attr]
