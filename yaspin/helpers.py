# -*- coding: utf-8 -*-

"""
yaspin.helpers
~~~~~~~~~~~~~~

Helper functions.
"""

from __future__ import absolute_import

from .constants import ENCODING


def to_unicode(unicode_or_str, encoding=ENCODING):
    if isinstance(unicode_or_str, str):
        return unicode_or_str.decode(encoding)
    return unicode_or_str
