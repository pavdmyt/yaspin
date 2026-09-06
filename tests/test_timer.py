"""
tests.test_timer
~~~~~~~~~~~~~~~~

Test timer feature.
"""

from io import StringIO

import re
import time

import pytest

from yaspin import yaspin


def test_no_timer():
    sp = yaspin(timer=False)
    sp._freeze("")

    assert re.search(r"\(\d+:\d{2}:\d{2}.\d{2}\)", sp._last_frame) is None


def test_timer_idle():
    sp = yaspin(timer=True)

    assert sp.elapsed_time == 0

    sp._freeze("")

    assert "(0:00:00.00)" in sp._last_frame


@pytest.mark.parametrize(
    "timer, expected",
    [
        pytest.param(" ({})", " (0:00:00)", id="elapsed-time-only"),
        pytest.param(" [{}.{:02.0f}]", " [0:00:00.00]", id="elapsed-time-and-hundredths"),
        pytest.param(" {{{}}}", " {0:00:00}", id="escaped-braces"),
    ],
)
def test_timer_custom_format(timer, expected):
    sp = yaspin(timer=timer)
    sp._freeze("")

    assert expected in sp._last_frame


@pytest.mark.parametrize(
    "timer",
    [
        pytest.param("", id="no-fields"),
        pytest.param("elapsed", id="literal-only"),
        pytest.param("{} {} {}", id="three-fields"),
        pytest.param("{0}", id="indexed-field"),
        pytest.param("{elapsed}", id="named-field"),
        pytest.param("{", id="malformed-brace"),
        pytest.param("{:02.0f}", id="incompatible-format-spec"),
    ],
)
def test_timer_custom_format_validation(timer):
    with pytest.raises(ValueError, match="timer format"):
        yaspin(timer=timer)


@pytest.mark.parametrize("timer", [pytest.param(0, id="integer"), pytest.param(None, id="none")])
def test_timer_rejects_non_bool_or_str_value(timer):
    with pytest.raises(TypeError, match="timer must be a bool or str"):
        yaspin(timer=timer)


def test_custom_timer_format_is_included_in_text_truncation():
    sp = yaspin(text="abc", timer=" ({})", stream=StringIO())
    sp._terminal_width = len("* ") + len(" (0:00:00)") + 2

    assert sp._compose_out("*") == "\r* ab (0:00:00)"


def test_timer_in_progress():
    sp = yaspin(timer=True)
    sp.start()

    t1 = sp.elapsed_time
    time.sleep(0.001)
    t2 = sp.elapsed_time

    sp.stop()

    assert t2 - t1 >= 0.001

    sp._freeze("")

    assert re.search(r"\(\d+:\d{2}:\d{2}.\d{2}\)", sp._last_frame) is not None


@pytest.mark.parametrize("interval, expected", [(0.994, "(0:00:00.99)"), (0.996, "(0:00:01.00)")])
def test_timer_rounding(interval, expected):
    sp = yaspin(timer=True)
    sp.start()
    sp.stop()

    sp._stop_time = sp._start_time + interval
    sp._freeze("")

    assert expected in sp._last_frame


def test_timer_finished():
    sp = yaspin(timer=True)
    sp.start()

    time.sleep(0.001)

    sp.stop()

    assert sp.elapsed_time >= 0.001

    t1 = sp.elapsed_time
    time.sleep(0.001)
    t2 = sp.elapsed_time

    assert t1 == t2

    sp._freeze("")

    assert re.search(r"\(\d+:\d{2}:\d{2}.\d{2}\)", sp._last_frame) is not None
