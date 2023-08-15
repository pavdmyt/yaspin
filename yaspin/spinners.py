# :copyright: (c) 2021 by Pavlo Dmytrenko.
# :license: MIT, see LICENSE for more details.

"""
yaspin.spinners
~~~~~~~~~~~~~~~

A collection of cli spinners.
"""

import json
import pkgutil
from collections import namedtuple
from typing import Any

spinners_json = pkgutil.get_data(__name__, "data/spinners.json")
if spinners_json is not None:
    SPINNERS_DATA = spinners_json.decode("utf-8")
else:
    raise RuntimeError("Cannot load spinners.json")


def _hook(dct: dict[str, Any]) -> Any:
    return namedtuple("Spinner", dct.keys())(*dct.values())


Spinners = json.loads(SPINNERS_DATA, object_hook=_hook)
