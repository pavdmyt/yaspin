# -*- coding: utf-8 -*-

"""
tests.conftest
~~~~~~~~~~~~~~

Tests data.
"""

import pytest


frame_cases = [
    # XXX: try byte strings
    # String types
    "",                                            # empty
    "+x*",                                         # ascii str
    "⢄⢂⢁⡁⡈⡐⡠",                                     # non-ascii in str
    u"⢹⢺⢼⣸",                                       # non-ascii in unicode str

    # Lists
    [],                                            # List[]
    [b"\xf0\x9f\x8c\xb2", b"\xf0\x9f\x8e\x84"],    # List[bytes]
    [u"🌲", u"🎄"],                                # List[unicode]
    ["⢹", "⢺", "⢼", "⣸"],                          # List[str], non-ascii

    # Tuples
    (),                                            # Tuple[]
    (b"\xf0\x9f\x8c\xb2", b"\xf0\x9f\x8e\x84"),    # Tuple[bytes]
    (u"🌲", u"🎄"),                                # Tuple[unicode]
    ("⢹", "⢺", "⢼", "⣸"),                          # Tuple[str], non-ascii
]


frame_ids = [
    # String types
    "'empty str'",
    "'ascii str'",
    "'non-ascii str'",
    "'non-ascii unicode str'",

    # Lists
    "'List[]'",
    "'List[bytes]'",
    "'List[unicode]'",
    "'List[str] non-ascii'",

    # Tuples
    "'Tuple[]'",
    "'Tuple[bytes]'",
    "'Tuple[unicode]'",
    "'Tuple[str] non-ascii'",
]


text_cases = [
    # XXX: try byte strings

    "",             # empty
    "Loading",      # ascii str
    "ℙƴ☂ℌøἤ",       # non-ascii in str
    u"Загрузка",    # non-ascii in unicode str
]


text_ids = [
    "'empty'",
    "'ascii str'",
    "'non-ascii str'",
    "'non-ascii unicode str'",
]


@pytest.fixture(scope="session")
def interval():
    return 80


@pytest.fixture(scope="session", params=frame_cases, ids=frame_ids)
def frames(request):
    return request.param


@pytest.fixture(scope="session", params=text_cases, ids=text_ids)
def text(request):
    return request.param


@pytest.fixture(
    scope="session",
    params=[False, True],
    ids=["'left'", "'right'"]
)
def right(request):
    return request.param


@pytest.fixture(
    scope="session",
    params=[False, True],
    ids=["default", "reverse"]
)
def reverse(request):
    return request.param
