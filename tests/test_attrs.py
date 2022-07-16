"""
tests.test_attrs
~~~~~~~~~~~~~~~~

Test Yaspin attributes magic hidden in __getattr__.
"""

import sys

import pytest

from yaspin import yaspin
from yaspin.constants import COLOR_MAP, SPINNER_ATTRS
from yaspin.spinners import Spinners


@pytest.mark.parametrize("attr_name", SPINNER_ATTRS)
def test_set_spinner_by_name(attr_name):
    sp = getattr(yaspin(), attr_name)
    assert sp.spinner == getattr(Spinners, attr_name)


# Values for ``color`` argument
def test_color(monkeypatch, color_test_cases):
    color, expected = color_test_cases
    # ``None`` and ``""`` are skipped
    if not color:
        pytest.skip(f"{color!r} - unsupported case")

    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    sp = yaspin()

    if isinstance(expected, Exception):
        with pytest.raises(AttributeError):
            getattr(sp, color)
    else:
        getattr(sp, color)
        assert sp.color == expected
        assert sp._color_func.keywords["color"] == expected  # pylint: disable=no-member


# Values for ``on_color`` argument
def test_on_color(monkeypatch, on_color_test_cases):
    on_color, expected = on_color_test_cases
    # ``None`` and ``""`` are skipped
    if not on_color:
        pytest.skip(f"{on_color!r} - unsupported case")

    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    sp = yaspin()

    if isinstance(expected, Exception):
        with pytest.raises(AttributeError):
            getattr(sp, on_color)
    else:
        getattr(sp, on_color)
        assert sp.on_color == expected
        assert (
            sp._color_func.keywords["on_color"] == expected  # pylint: disable=no-member
        )  # pylint: disable=no-member


# Values for ``attrs`` argument
@pytest.mark.parametrize(
    "attr", sorted([k for k, v in COLOR_MAP.items() if v == "attrs"])
)
def test_attrs(monkeypatch, attr):
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    sp = yaspin()
    getattr(sp, attr)
    assert sp.attrs == [attr]
    assert sp._color_func.keywords["attrs"] == [attr]  # pylint: disable=no-member


def id_func(case):
    return ", ".join(case)


@pytest.mark.parametrize(
    "attrs",
    [
        ["bold", "bold"],
        ["bold", "dark"],
        ["blink", "reverse", "blink"],
        ["concealed", "underline", "bold", "bold"],
    ],
    ids=id_func,
)
def test_previous_attrs_persist_1(attrs):
    sp = yaspin()
    for attr in attrs:
        getattr(sp, attr)
    assert sp._attrs == set(attrs)


def test_previous_attrs_persist_2():
    sp = yaspin(attrs=["blink", "underline"]).bold.dark
    assert sp._attrs == set(["blink", "underline", "bold", "dark"])


# Values for ``side`` argument
@pytest.mark.parametrize(
    "side, expected",
    [("left", "left"), ("right", "right"), ("center", ValueError())],
)
def test_side(side, expected):
    sp = yaspin()

    if isinstance(expected, Exception):
        with pytest.raises(AttributeError):
            getattr(sp, side)
    else:
        getattr(sp, side)
        assert sp.side == expected
