# -*- coding: utf-8 -*-

"""
yaspin.spinners
~~~~~~~~~~~~~~~

A collection of cli spinners.
"""

import pkgutil
from collections import namedtuple

try:
    import simplejson as json
except ImportError:
    import json


SPINNERS_DATA = pkgutil.get_data(__name__, "data/spinners.json").decode("utf-8")


def _hook(dct):
    return namedtuple("Spinner", dct.keys())(*dct.values())


Spinners = json.loads(SPINNERS_DATA, object_hook=_hook)
