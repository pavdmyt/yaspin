# -*- coding: utf-8 -*-

"""
tests.test_finalizers
~~~~~~~~~~~~~~~~~~~~~

"""

from yaspin import yaspin
from yaspin.compat import builtin_str


def test_freeze(final_text):
    swirl = yaspin()
    swirl._freeze(final_text)

    assert isinstance(swirl._last_frame, builtin_str)
    assert swirl._last_frame[-1] == "\n"
