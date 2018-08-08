# -*- coding: utf-8 -*-

"""
tests.test_attrs
~~~~~~~~~~~~~~~~

Test Yaspin attributes magic hidden in __getattr__.
"""

from __future__ import absolute_import

import pytest

from yaspin import yaspin
from yaspin.constants import SPINNER_ATTRS
from yaspin.spinners import Spinners


@pytest.mark.parametrize("attr_name", SPINNER_ATTRS)
def test_set_spinner_by_name(attr_name):
    sp = getattr(yaspin(), attr_name)
    assert sp.spinner == getattr(Spinners, attr_name)
