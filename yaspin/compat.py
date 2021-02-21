# -*- coding: utf-8 -*-
#
# :copyright: (c) 2021 by Pavlo Dmytrenko.
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
    bytes = str  # pylint: disable=redefined-builtin
    str = unicode  # pylint: disable=redefined-builtin,undefined-variable
    basestring = basestring  # pylint: disable=undefined-variable,self-assigning-variable

    def iteritems(dct):
        return dct.iteritems()


else:
    builtin_str = str
    bytes = bytes  # pylint: disable=self-assigning-variable
    str = str  # pylint: disable=self-assigning-variable
    basestring = (str, bytes)

    def iteritems(dct):
        return dct.items()
