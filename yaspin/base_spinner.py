# :copyright: (c) 2021 by Pavlo Dmytrenko.
# :license: MIT, see LICENSE for more details.

"""
yaspin.base_spinner
~~~~~~~~~~~~~~~~~~~

Spinner class, used to construct other spinners.
"""
from dataclasses import dataclass


@dataclass
class Spinner:
    frames: str
    interval: int


default_spinner = Spinner("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏", 80)
