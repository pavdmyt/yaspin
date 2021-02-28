# -*- coding: utf-8 -*-

"""
tests.test_in_out
~~~~~~~~~~~~~~~~~

Checks that all input data is converted to unicode.
And all output data is converted to builtin str type.
"""

import re
import sys
import time

import pytest

from yaspin import Spinner, yaspin
from yaspin.compat import PY2, basestring, builtin_str, str
from yaspin.constants import ENCODING
from yaspin.helpers import to_unicode


def test_input_converted_to_unicode(text, frames, interval, reversal, side):
    sp = Spinner(frames, interval)
    sp = yaspin(sp, text, side=side, reversal=reversal)

    if isinstance(sp._frames, basestring):
        assert isinstance(sp._frames, str)

    if isinstance(sp._frames, (list, tuple)):
        assert isinstance(sp._frames[0], str)

    assert isinstance(sp._text, str)


def test_out_converted_to_builtin_str(text, frames, interval, reversal, side):
    sp = Spinner(frames, interval)
    sp = yaspin(sp, text, side=side, reversal=reversal)

    for _ in range(len(frames)):
        frame = next(sp._cycle)
        out = sp._compose_out(frame)
        assert isinstance(out, builtin_str)


def test_repr(text, frames, interval):
    sp = Spinner(frames, interval)
    sp = yaspin(sp, text)

    assert isinstance(repr(sp), builtin_str)


def test_compose_out_with_color(
    color_test_cases, on_color_test_cases, attrs_test_cases
):
    color, color_exp = color_test_cases
    on_color, on_color_exp = on_color_test_cases
    attrs, attrs_exp = attrs_test_cases

    # Skip non relevant cases
    empty = not color_exp or not on_color_exp or not attrs_exp
    is_exc = any(
        [
            isinstance(color_exp, Exception),
            isinstance(on_color_exp, Exception),
            isinstance(attrs_exp, Exception),
        ]
    )
    if empty or is_exc:
        items = [repr(color_exp), repr(on_color_exp), repr(attrs_exp)]
        pytest.skip("{0} - unsupported case".format(items))

    # Actual test
    sp = yaspin(color=color, on_color=on_color, attrs=attrs)
    assert sp._color == color
    assert sp._on_color == on_color
    assert sp._attrs == set(attrs)

    out = sp._compose_out(frame=u"/")
    assert out.startswith("\r\033")
    assert isinstance(out, builtin_str)


def test_write(capsys, text):
    sp = yaspin()
    sp.write(text)

    out, _ = capsys.readouterr()
    # cleans stdout from _clear_line and \r
    out = out.replace("\r\033[K", "")

    # handle out and text encodings (come out messy in PY2)
    # Under PY2 ``capsys.readouterr`` always produces ``out``
    # of type ``unicode``. Conversion to bytes is required
    # for proper ``out`` and ``text`` comparison.
    if PY2:
        out = out.encode(ENCODING)
        if isinstance(text, str):
            text = text.encode(ENCODING)

    assert isinstance(out, basestring)
    assert out[-1] == "\n"
    if text:
        assert out[:-1] == text


def test_hide_show(capsys, text, request):
    # Setup
    sp = yaspin()
    sp.start()

    # Ensure that sp.stop() will be executed
    def teardown():
        sp.stop()

    request.addfinalizer(teardown)

    #
    # Actual test
    #
    sp.hide()

    # ensure that hidden spinner flag was set
    assert sp._hide_spin.is_set()
    out, _ = capsys.readouterr()

    # ensure that text was cleared with the hide method
    assert out[-4:] == "\r\033[K"

    # properly encode text to unicode if running in PY2
    if PY2:
        text = to_unicode(text).encode(ENCODING)

    # ``\n`` is required to flush stdout during
    # the hidden state of the spinner
    sys.stdout.write("{0}\n".format(text))
    out, _ = capsys.readouterr()

    # cleans stdout from _clear_line and \r
    out = out.replace("\r\033[K", "")

    # handle out and text encodings (come out messy in PY2)
    # Under PY2 ``capsys.readouterr`` always produces ``out``
    # of type ``unicode``. Conversion to bytes is required
    # for proper ``out`` and ``text`` comparison.
    if PY2:
        out = out.encode(ENCODING)
        if isinstance(text, str):
            text = text.encode(ENCODING)

    assert isinstance(out, basestring)
    assert out[-1] == "\n"
    if text:
        assert out[:-1] == text

    sp.show()

    # ensure that hidden spinner flag was cleared
    assert not sp._hide_spin.is_set()
    out, _ = capsys.readouterr()

    # ensure that text was cleared before resuming the spinner
    assert out[:4] == "\r\033[K"


def test_spinner_write_race_condition(capsys):
    # test that spinner text does not overwrite write() contents
    # this generally happens when the spinner thread writes
    # between write()'s \r and the text it actually wants to write

    sp = yaspin(text="aaaa")
    sp.start()
    sp._interval = 0.0
    start_time = time.time()
    while time.time() - start_time < 3.0:
        sp.write("bbbb")
    sp.stop()

    out, _ = capsys.readouterr()
    assert "aaaa" in out  # spinner text is present
    assert "bbbb" in out  # write() text is present
    assert not re.search(r"aaaa[^\rb]*bbbb", out)


def test_spinner_hiding_with_context_manager(capsys):
    HIDDEN_START = "hidden start"
    HIDDEN_END = "hidden end"
    sp = yaspin(text="foo")
    sp.start()

    with sp.hidden():
        assert sp._hide_spin.is_set()
        sp.write(HIDDEN_START)

        # give the spinner some time to spin if it would not be hidden
        time.sleep(3 * sp._interval)

        sp.write(HIDDEN_END)

    assert not sp._hide_spin.is_set()
    sp.stop()

    # make sure no spinner text was printed while the spinner was hidden
    out, _ = capsys.readouterr()
    out = out.replace("\r\033[K", "")
    assert "{}\n{}".format(HIDDEN_START, HIDDEN_END) in out


def test_spinner_nested_hiding_with_context_manager(capsys):
    HIDDEN_START = "hidden start"
    HIDDEN_END = "hidden end"
    sp = yaspin(text="foo")
    sp.start()

    with sp.hidden():
        sp.write(HIDDEN_START)

        with sp.hidden():
            assert sp._hidden_level == 2
            with sp.hidden():
                assert sp._hidden_level == 3
                time.sleep(3 * sp._interval)

        assert sp._hidden_level == 1
        assert sp._hide_spin.is_set()
        sp.write(HIDDEN_END)

    assert not sp._hide_spin.is_set()
    sp.stop()

    # make sure no spinner text was printed while the spinner was hidden
    out, _ = capsys.readouterr()
    out = out.replace("\r\033[K", "")
    assert "{}\n{}".format(HIDDEN_START, HIDDEN_END) in out


def test_spinner_hiding_with_context_manager_and_exception():
    sp = yaspin(text="foo")
    sp.start()

    try:
        with sp.hidden():
            raise ValueError()
    except ValueError:
        pass
    else:
        assert False, "Expected a ValueError, something has eaten the exception"

    # make sure spinner is unhidden again
    assert sp._hidden_level == 0
    assert not sp._hide_spin.is_set()

    sp.stop()


@pytest.mark.parametrize(
    "obj, obj_str",
    [
        ("foo", "foo"),
        (dict(cat="meow"), "{'cat': 'meow'}"),
        (23, "23"),
        (["foo", "bar", "'", 23], """['foo', 'bar', "'", 23]"""),
    ],
)
def test_write_non_str_objects(capsys, obj, obj_str):
    sp = yaspin()
    capsys.readouterr()
    sp.write(obj)
    out, _ = capsys.readouterr()
    assert out == "\r\033[K{}\n".format(obj_str)
