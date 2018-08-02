# -*- coding: utf-8 -*-

"""
tests.test_pipes
~~~~~~~~~~~~~~~~

Checks that scripts with yaspin are safe
for pipes and redirects:

  $ python script_that_uses_yaspin.py > script.log
  $ python script_that_uses_yaspin.py | grep ERROR

"""

import os
import sys
import uuid

import pytest

from yaspin.compat import basestring, str
from yaspin.constants import ENCODING


TEST_CODE = """\
# -*- coding: utf-8 -*-

import time
from yaspin import yaspin, Spinner

with yaspin(Spinner(%s, %s), '%s') as sp:
    time.sleep(0.5)
    sp.fail('🙀')
"""


def to_bytes(str_or_bytes, encoding=ENCODING):
    if isinstance(str_or_bytes, str):
        return str_or_bytes.encode(encoding)
    return str_or_bytes


def to_unicode(str_or_bytes, encoding=ENCODING):
    if isinstance(str_or_bytes, bytes):
        return str_or_bytes.decode(encoding)
    return str_or_bytes


@pytest.fixture()
def case_id():
    return str(uuid.uuid4())


def test_piping_output(text, frames, interval, case_id):
    py_fname = "spin-{0}.py".format(case_id)
    fname = "out-{0}.txt".format(case_id)

    def teardown():
        os.remove(py_fname)
        os.remove(fname)

    with open(py_fname, "wb") as f:
        if isinstance(frames, basestring):
            # enclosing characters in quotes
            # for basestring entries
            # to avoid SyntaxError
            frames = repr(to_unicode(frames))

        text = to_unicode(text)
        interval = to_unicode(interval)
        code = to_unicode(TEST_CODE)
        res = code % (frames, interval, text)
        f.write(to_bytes(res))

    try:
        # $ python spin.py > out.txt
        os.system("{0} {1} > {2}".format(sys.executable, py_fname, fname))
    except UnicodeEncodeError as err:
        pytest.fail(err)
    finally:
        teardown()
