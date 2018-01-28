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


def test_ok(final_text):
    swirl = yaspin()
    swirl.ok(final_text)

    assert isinstance(swirl._last_frame, builtin_str)
    assert swirl._last_frame[-1] == "\n"


def test_ok_empty_case():
    swirl = yaspin()
    swirl.ok()
    assert "OK" in swirl._last_frame


def test_fail(final_text):
    swirl = yaspin()
    swirl.fail(final_text)

    assert isinstance(swirl._last_frame, builtin_str)
    assert swirl._last_frame[-1] == "\n"


def test_fail_empty_case():
    swirl = yaspin()
    swirl.fail()
    assert "FAIL" in swirl._last_frame
