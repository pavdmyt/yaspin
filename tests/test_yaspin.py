# -*- coding: utf-8 -*-

"""
tests.test_yaspin
~~~~~~~~~~~~~~~~~

Basic unittests.
"""

from __future__ import absolute_import

import os
import sys

import pytest
from yaspin import spinner

from .compat import builtin_str, bytes, str


#
# Helpers
#
def to_bytes(str_or_bytes, encoding='utf-8'):
    if isinstance(str_or_bytes, str):
        return str_or_bytes.encode(encoding)
    return str_or_bytes


def to_unicode(str_or_bytes, encoding='utf-8'):
    if isinstance(str_or_bytes, bytes):
        return str_or_bytes.decode(encoding)
    return str_or_bytes


#
# Tests
#
test_cases = [
    # Default sequence and interval
    ("", "", None),

    # str text, str sequence
    ("Loading", "+x*", 0.08),

    # unicode text, unicode sequence (marked as unicode)
    (u"Загрузка", u"⢄⢂⢁⡁⡈⡐⡠", 0.08),

    # unicode text, str sequence
    ("Загрузка", "+x*", 0.08),

    # str text, unicode sequence
    ("Loading", "⢄⢂⢁⡁⡈⡐⡠", 0.08),
]


@pytest.mark.parametrize("text, sequence, interval", test_cases)
def test_input_converted_to_unicode(text, sequence, interval):
    sp = spinner(text, sequence, interval)

    assert isinstance(sp._sequence, str)
    assert isinstance(sp._text, str)


@pytest.mark.parametrize("text, sequence, interval", test_cases)
def test_output_converted_to_builtin_str(text, sequence, interval):
    sp = spinner(text, sequence, interval)

    for _ in range(20):             # test 20 frames
        out = sp.compose_frame()
        assert isinstance(out, builtin_str)


@pytest.mark.parametrize("text, sequence, interval", test_cases)
def test_repr(text, sequence, interval):
    sp = spinner(text, sequence, interval)

    assert isinstance(repr(sp), builtin_str)


@pytest.mark.parametrize("text, sequence, interval", test_cases)
def test_piping_output(text, sequence, interval):
    py_fname = "spin.py"
    fname = "out.txt"

    def teardown():
        os.remove(py_fname)
        os.remove(fname)

    code = """\
# -*- coding: utf-8 -*-

import time
from yaspin import spinner

with spinner('%s', '%s', %s):
    time.sleep(0.5)
"""

    with open(py_fname, 'wb') as f:
        text = to_unicode(text)
        sequence = to_unicode(sequence)
        interval = to_unicode(interval)
        code = to_unicode(code)
        res = code % (text, sequence, interval)
        f.write(to_bytes(res))

    try:
        # $ python spin.py > out.txt
        os.system("{0} {1} > {2}".format(sys.executable, py_fname, fname))
    except UnicodeEncodeError as err:
        pytest.fail(err)
    finally:
        teardown()
