# -*- coding: utf-8 -*-
#
# :copyright: (c) 2021 by Pavlo Dmytrenko.
# :license: MIT, see LICENSE for more details.

"""
yaspin.helpers
~~~~~~~~~~~~~~

Helper functions.
"""

from __future__ import absolute_import

from .compat import bytes  # pylint: disable=redefined-builtin
from .constants import ENCODING


def to_unicode(text_type, encoding=ENCODING):
    if isinstance(text_type, bytes):
        return text_type.decode(encoding)
    return text_type
