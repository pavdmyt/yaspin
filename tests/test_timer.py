# -*- coding: utf-8 -*-

"""
tests.test_timer
~~~~~~~~~~~~~~~~~~~~~

"""

import time
import re

from yaspin import yaspin


def test_no_timer():
    sp = yaspin(timer=False)
    sp._freeze("")

    assert re.search(r"\(\d+:\d{2}:\d{2}\)", sp._last_frame) is None


def test_timer_idle():
    sp = yaspin(timer=True)

    assert sp.elapsed_time == 0

    sp._freeze("")

    assert "(0:00:00)" in sp._last_frame


def test_timer_in_progress():
    sp = yaspin(timer=True)
    sp.start()

    t1 = sp.elapsed_time
    time.sleep(0.001)
    t2 = sp.elapsed_time

    sp.stop()

    assert t2 - t1 >= 0.001

    sp._freeze("")

    assert re.search(r"\(\d+:\d{2}:\d{2}\)", sp._last_frame) is not None


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

    assert re.search(r"\(\d+:\d{2}:\d{2}\)", sp._last_frame) is not None
