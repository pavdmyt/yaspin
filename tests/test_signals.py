# -*- coding: utf-8 -*-

"""
tests.test_signals
~~~~~~~~~~~~~~~~~~

Test Yaspin signals handling.
"""

from __future__ import absolute_import

import functools
import signal

import pytest

from yaspin import kbi_safe_yaspin, yaspin
from yaspin.compat import iteritems


def test_sigmap_setting(sigmap_test_cases):
    sigmap = sigmap_test_cases
    sp = yaspin(sigmap=sigmap)
    if sigmap is None:
        assert sp._sigmap == {}
    else:
        assert sp._sigmap == sigmap


def test_sigmap_signals_get_registered(sigmap_test_cases):
    sigmap = sigmap_test_cases
    if not sigmap:
        pytest.skip("{0!r} - unsupported case".format(sigmap))

    sp = yaspin(sigmap=sigmap)
    # If test fails, the spinner may infinitely stuck ignoring
    # signals, except of SIGKILL; try-finally block ensures
    # that spinner get stopped.
    try:
        sp.start()
        for sig, sig_handler in iteritems(sigmap):
            handler = signal.getsignal(sig)
            is_partial = isinstance(handler, functools.partial)

            if callable(sig_handler) and is_partial:
                # Handler function is wrapped into ``partial`` and
                # is accesible via ``func`` attribute.
                assert sig_handler == handler.func
            else:
                # SIG_DFL and SIG_IGN cases
                assert sig_handler == handler
    finally:
        sp.stop()


def test_raise_exception_for_sigkill():
    sp = yaspin(sigmap={signal.SIGKILL: signal.SIG_IGN})
    try:
        with pytest.raises(ValueError):
            sp.start()
    finally:
        sp.stop()


def test_default_handlers_are_set_at_cleanup_stage(sigmap_test_cases):
    sigmap = sigmap_test_cases
    if not sigmap:
        pytest.skip("{0!r} - unsupported case".format(sigmap))

    sp = yaspin(sigmap=sigmap)
    sp.start()
    sp.stop()

    for sig in sigmap.keys():
        handler = signal.getsignal(sig)
        assert handler == sp._dfl_sigmap[sig]


def test_kbi_safe_yaspin():
    sp = kbi_safe_yaspin()

    try:
        sp.start()

        handler = signal.getsignal(signal.SIGINT)
        # Handler function is wrapped into ``partial`` and
        # is accesible via ``func`` attribute.
        assert handler.func == sp._sigmap[signal.SIGINT]
    finally:
        sp.stop()
