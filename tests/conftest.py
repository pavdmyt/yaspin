# -*- coding: utf-8 -*-

"""
tests.conftest
~~~~~~~~~~~~~~

Tests data.
"""

import signal
import sys

import pytest

from yaspin.compat import iteritems
from yaspin.constants import COLOR_MAP
from yaspin.signal_handlers import default_handler, fancy_handler


frame_cases = [
    # XXX: try byte strings
    # String types
    "",  # empty
    "+x*",  # ascii str
    "⢄⢂⢁⡁⡈⡐⡠",  # non-ascii in str
    u"⢹⢺⢼⣸",  # non-ascii in unicode str
    # Lists
    [],  # List[]
    [b"\xf0\x9f\x8c\xb2", b"\xf0\x9f\x8e\x84"],  # List[bytes]
    [u"🌲", u"🎄"],  # List[unicode]
    ["⢹", "⢺", "⢼", "⣸"],  # List[str], non-ascii
    # Tuples
    (),  # Tuple[]
    (b"\xf0\x9f\x8c\xb2", b"\xf0\x9f\x8e\x84"),  # Tuple[bytes]
    (u"🌲", u"🎄"),  # Tuple[unicode]
    ("⢹", "⢺", "⢼", "⣸"),  # Tuple[str], non-ascii
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
    "",  # empty
    "Loading",  # ascii str
    "ℙƴ☂ℌøἤ",  # non-ascii in str
    u"Загрузка",  # non-ascii in unicode str
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


@pytest.fixture(scope="session", params=["left", "right"])
def side(request):
    return request.param


@pytest.fixture(
    scope="session", params=[False, True], ids=["default", "reversal"]
)
def reversal(request):
    return request.param


def color_id_func(case):
    if isinstance(case, tuple):
        color, _ = case
    else:
        color = case

    if not color or callable(color):
        val = repr(color)
    else:
        val = color

    return val


def attrs_id_func(case):
    if isinstance(case, list):
        val = ", ".join(case)
    if isinstance(case, tuple):
        attrs, _ = case
        val = ", ".join(attrs)
    return val


@pytest.fixture(
    scope="session",
    ids=color_id_func,
    params=[
        # Empty values
        ("", ""),
        (None, None),
        # Supported text colors
        ("red", "red"),
        ("green", "green"),
        ("yellow", "yellow"),
        ("blue", "blue"),
        ("magenta", "magenta"),
        ("cyan", "cyan"),
        ("white", "white"),
        # Unsupported text colors
        ("Red", ValueError()),
        ("orange", ValueError()),
    ],
)
def color_test_cases(request):
    return request.param


@pytest.fixture(
    scope="session",
    ids=color_id_func,
    params=[
        # Empty values
        ("", ""),
        (None, None),
        # Supported highlights
        ("on_red", "on_red"),
        ("on_green", "on_green"),
        ("on_yellow", "on_yellow"),
        ("on_blue", "on_blue"),
        ("on_magenta", "on_magenta"),
        ("on_cyan", "on_cyan"),
        ("on_white", "on_white"),
        # Unsupported highlights
        ("on_foo", ValueError()),
    ],
)
def on_color_test_cases(request):
    return request.param


@pytest.fixture(
    scope="session",
    ids=attrs_id_func,
    params=[
        # Supported attrs
        (["bold"], ["bold"]),
        (["dark"], ["dark"]),
        (["underline"], ["underline"]),
        (["blink"], ["blink"]),
        (["reverse"], ["reverse"]),
        (["concealed"], ["concealed"]),
        # Multiple attrs
        (["bold", "dark"], ["bold", "dark"]),
        (["bold", "dark", "reverse"], ["bold", "dark", "reverse"]),
        # Unsupported attrs
        (["Dark"], ValueError()),
        (["bold", "bar"], ValueError()),
    ],
)
def attrs_test_cases(request):
    return request.param


@pytest.fixture(
    scope="session",
    ids=color_id_func,
    params=sorted([k for k, v in iteritems(COLOR_MAP) if v == "color"]),
)
def supported_colors(request):
    return request.param


@pytest.fixture(
    scope="session",
    ids=color_id_func,
    params=sorted([k for k, v in iteritems(COLOR_MAP) if v == "on_color"]),
)
def supported_highlights(request):
    return request.param


@pytest.fixture(
    scope="session",
    ids=attrs_id_func,
    params=sorted(
        [[k] for k, v in iteritems(COLOR_MAP) if v == "attrs"]
        + [
            ["bold", "dark"],
            ["blink", "concealed", "reverse"],
            ["underline", "concealed", "bold", "dark", "blink", "reverse"],
        ]
    ),
)
def supported_attrs(request):
    return request.param


@pytest.fixture(
    scope="session",
    params=[
        # Empty
        b"",
        u"",
        # Success
        b"OK",
        u"OK",
        b"\xe2\x9c\x94",
        u"✔",
        # Sun
        b"\xe2\x98\x80\xef\xb8\x8f",
        u"☀️",
        # Spark
        b"\xf0\x9f\x92\xa5",
        u"💥",
    ],
)
def final_text(request):
    return request.param


@pytest.fixture(
    scope="session",
    params=[
        None,
        {signal.SIGUSR1: signal.SIG_DFL},
        {signal.SIGTERM: signal.SIG_IGN},
        {signal.SIGTERM: signal.default_int_handler},
        {signal.SIGHUP: default_handler},
        {signal.SIGINT: fancy_handler},
        {signal.SIGINT: lambda signum, frame: sys.exit(1)},
        {
            signal.SIGUSR1: signal.SIG_DFL,
            signal.SIGTERM: signal.SIG_IGN,
            signal.SIGHUP: default_handler,
            signal.SIGINT: fancy_handler,
            signal.SIGINT: lambda signum, frame: sys.exit(1),
        },
    ],
    ids=[
        "no sigmap",
        "SIGUSR1 - SIG_DFL",
        "SIGTERM - SIG_IGN",
        "SIGTERM - default_int_handler",
        "SIGHUP - default_handler",
        "SIGINT - fancy_handler",
        "SIGINT - custom handler",
        "Multiple signals-handlers map",
    ],
)
def sigmap_test_cases(request):
    return request.param
