# -*- coding: utf-8 -*-
#
# :copyright: (c) 2020 by Pavlo Dmytrenko.
# :license: MIT, see LICENSE for more details.

"""
yaspin.compat
~~~~~~~~~~~~~

Compatibility layer.
"""

import sys


PY2 = sys.version_info[0] == 2


if PY2:
    builtin_str = str
    str = unicode  # noqa
    basestring = basestring  # noqa
else:
    builtin_str = str
    str = str
    basestring = (str, bytes)
