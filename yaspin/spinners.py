# -*- coding: utf-8 -*-

"""
yaspin.spinners
~~~~~~~~~~~~~~~

A collection of cli spinners.
"""

import codecs
import os
from collections import namedtuple

try:
    import simplejson as json
except ImportError:
    import json


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
SPINNERS_PATH = os.path.join(THIS_DIR, "data/spinners.json")


def _get_attrs(spinners):
    """Get names of the spinners available in ``Spinners``.

    Arguments:
        spinners (Spinners): namedtuple containing spinners
            parsed from ``spinners.json``.

    Returns:
        generator

    """
    attrs = (
        attr
        for attr in dir(spinners)
        if not callable(getattr(spinners, attr))
        if not attr.startswith("_")
    )
    return attrs


def _hook(dct):
    return namedtuple("Spinner", dct.keys())(*dct.values())


with codecs.open(SPINNERS_PATH, encoding="utf-8") as f:
    Spinners = json.load(f, object_hook=_hook)
