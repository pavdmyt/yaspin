"""
tests.conftest
~~~~~~~~~~~~~~

Tests data.
"""

import signal
import sys

from termcolor import ATTRIBUTES, COLORS, HIGHLIGHTS

import pytest

from yaspin.core import default_handler, fancy_handler

frame_cases = [
    # XXX: try byte strings
    # String types
    "",  # empty
    "+x*",  # ascii str
    "⢄⢂⢁⡁⡈⡐⡠",  # non-ascii in str
    "⢹⢺⢼⣸",  # non-ascii in unicode str
    # Lists
    [],  # List[]
    [b"\xf0\x9f\x8c\xb2", b"\xf0\x9f\x8e\x84"],  # List[bytes]
    ["🌲", "🎄"],  # List[unicode]
    ["⢹", "⢺", "⢼", "⣸"],  # List[str], non-ascii
    # Tuples
    (),  # Tuple[]
    (b"\xf0\x9f\x8c\xb2", b"\xf0\x9f\x8e\x84"),  # Tuple[bytes]
    ("🌲", "🎄"),  # Tuple[unicode]
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
    "Загрузка",  # non-ascii in unicode str
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


@pytest.fixture(scope="session", params=[False, True], ids=["default", "reversal"])
def reversal(request):
    return request.param


@pytest.fixture(scope="session", params=[True, False], ids=["terminal", "jupyter"])
def isatty_fixture(request):
    return request.param


@pytest.fixture(autouse=True)
def isatty_true(monkeypatch):
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)


def color_id_func(case):
    if isinstance(case, tuple):
        color, _ = case
    else:
        color = case

    val = repr(color) if not color or callable(color) else color

    return val


def attrs_id_func(case):
    if isinstance(case, list):
        val = ", ".join(case)
    if isinstance(case, tuple):
        attrs, _ = case
        val = ", ".join(attrs)
    return val


def _sig(name):
    """Return the signal by name, or None on platforms that lack it (e.g. Windows)."""
    return getattr(signal, name, None)


SIGUSR1 = _sig("SIGUSR1")
SIGUSR2 = _sig("SIGUSR2")
SIGHUP = _sig("SIGHUP")
SIGINT = _sig("SIGINT")
SIGTERM = _sig("SIGTERM")


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
        # New highlights (from termcolor v2.2.0)
        ("black", "black"),
        ("dark_grey", "dark_grey"),
        ("light_grey", "light_grey"),
        ("light_red", "light_red"),
        ("light_green", "light_green"),
        ("light_yellow", "light_yellow"),
        ("light_blue", "light_blue"),
        ("light_magenta", "light_magenta"),
        ("light_cyan", "light_cyan"),
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
        # New highlights (from termcolor v2.2.0)
        ("on_black", "on_black"),
        ("on_dark_grey", "on_dark_grey"),
        ("on_light_grey", "on_light_grey"),
        ("on_light_red", "on_light_red"),
        ("on_light_green", "on_light_green"),
        ("on_light_yellow", "on_light_yellow"),
        ("on_light_blue", "on_light_blue"),
        ("on_light_magenta", "on_light_magenta"),
        ("on_light_cyan", "on_light_cyan"),
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
    params=sorted(COLORS.keys()),
)
def supported_colors(request):
    return request.param


@pytest.fixture(
    scope="session",
    ids=color_id_func,
    params=sorted(HIGHLIGHTS.keys()),
)
def supported_highlights(request):
    return request.param


@pytest.fixture(
    scope="session",
    ids=attrs_id_func,
    params=sorted(
        [[a] for a in ATTRIBUTES]
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
        "",
        # Success
        b"OK",
        "OK",
        b"\xe2\x9c\x94",
        "✔",
        # Sun
        b"\xe2\x98\x80\xef\xb8\x8f",
        "☀️",
        # Spark
        b"\xf0\x9f\x92\xa5",
        "💥",
    ],
)
def final_text(request):
    return request.param


# Build the sigmap test cases at module level, dropping cases that rely on
# signals unavailable on the current platform (SIGUSR1/SIGUSR2/SIGHUP on Windows).
_sigmap_params = [None]
_sigmap_ids = ["no sigmap"]
if SIGUSR1 is not None:
    _sigmap_params.append({SIGUSR1: signal.SIG_DFL})
    _sigmap_ids.append("SIGUSR1 - SIG_DFL")
if SIGTERM is not None:
    _sigmap_params.append({SIGTERM: signal.SIG_IGN})
    _sigmap_ids.append("SIGTERM - SIG_IGN")
    _sigmap_params.append({SIGTERM: signal.default_int_handler})
    _sigmap_ids.append("SIGTERM - default_int_handler")
if SIGHUP is not None:
    _sigmap_params.append({SIGHUP: default_handler})
    _sigmap_ids.append("SIGHUP - default_handler")
if SIGINT is not None:
    _sigmap_params.append({SIGINT: fancy_handler})
    _sigmap_ids.append("SIGINT - fancy_handler")
    _sigmap_params.append({SIGINT: lambda signum, frame: sys.exit(1)})
    _sigmap_ids.append("SIGINT - custom handler")
_multi = {}
if SIGUSR1 is not None:
    _multi[SIGUSR1] = signal.SIG_DFL
if SIGTERM is not None:
    _multi[SIGTERM] = signal.SIG_IGN
if SIGHUP is not None:
    _multi[SIGHUP] = default_handler
if SIGUSR2 is not None:
    _multi[SIGUSR2] = fancy_handler
if SIGINT is not None:
    _multi[SIGINT] = lambda signum, frame: sys.exit(1)
if len(_multi) > 1:
    _sigmap_params.append(_multi)
    _sigmap_ids.append("Multiple signals-handlers map")


@pytest.fixture(
    scope="session",
    params=_sigmap_params,
    ids=_sigmap_ids,
)
def sigmap_test_cases(request):
    return request.param
