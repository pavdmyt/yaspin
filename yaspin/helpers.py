# -*- coding: utf-8 -*-

"""
yaspin.helpers
~~~~~~~~~~~~~~

Helper functions.
"""

from __future__ import absolute_import

from .compat import PY2, builtin_str, bytes, str
from .constants import ENCODING


def to_unicode(text_type, encoding=ENCODING):
    if isinstance(text_type, bytes):
        return text_type.decode(encoding)
    return text_type


def to_printable_text(obj):
    obj = to_unicode(obj)
    if not isinstance(obj, builtin_str):
        obj = str(obj)

    if PY2 and isinstance(obj, str):
        obj = obj.encode(ENCODING)

    return obj
