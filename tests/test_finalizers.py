# -*- coding: utf-8 -*-

"""
tests.test_finalizers
~~~~~~~~~~~~~~~~~~~~~

"""

from yaspin import yaspin
from yaspin.compat import builtin_str


def test_freeze(final_text):
    sp = yaspin()
    sp._freeze(final_text)

    assert isinstance(sp._last_frame, builtin_str)
    assert sp._last_frame[-1] == "\n"


def test_ok(final_text):
    sp = yaspin()
    sp.ok(final_text)

    assert isinstance(sp._last_frame, builtin_str)
    assert sp._last_frame[-1] == "\n"


def test_ok_empty_case():
    sp = yaspin()
    sp.ok()
    assert "OK" in sp._last_frame


def test_fail(final_text):
    sp = yaspin()
    sp.fail(final_text)

    assert isinstance(sp._last_frame, builtin_str)
    assert sp._last_frame[-1] == "\n"


def test_fail_empty_case():
    sp = yaspin()
    sp.fail()
    assert "FAIL" in sp._last_frame
