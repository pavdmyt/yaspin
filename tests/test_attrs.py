# -*- coding: utf-8 -*-

"""
tests.test_attrs
~~~~~~~~~~~~~~~~

Test Yaspin attributes magic hidden in __getattr__.
"""

from __future__ import absolute_import

import pytest

from yaspin import yaspin
from yaspin.spinners import Spinners, _get_attrs


@pytest.mark.parametrize("attr_name", list(_get_attrs(Spinners)))
def test_set_spinner_by_name(attr_name):
    sp = getattr(yaspin(), attr_name)
    assert sp.spinner == getattr(Spinners, attr_name)
