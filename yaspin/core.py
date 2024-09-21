# :copyright: (c) 2021 by Pavlo Dmytrenko.
# :license: MIT, see LICENSE for more details.

"""
yaspin.yaspin
~~~~~~~~~~~~~

A lightweight terminal spinner.
"""
from __future__ import annotations

import functools
import itertools
import shutil
import signal
import sys
import threading
import time
import warnings
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import timedelta
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Final,
    Generator,
    Iterator,
    Optional,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
    runtime_checkable,
)

from termcolor import ATTRIBUTES, COLORS, HIGHLIGHTS, colored

from .constants import SPINNER_ATTRS

if TYPE_CHECKING:
    from types import FrameType, TracebackType

    SignalHandlers = Union[Callable[[int, Optional[FrameType]], Any], int, None]

Fn = TypeVar("Fn", bound=Callable[..., Any])

ENCODING: Final[str] = "utf-8"


def to_unicode(text_type: Union[str, bytes], encoding: str = ENCODING) -> str:
    if isinstance(text_type, bytes):
        return text_type.decode(encoding)
    return text_type


@dataclass
class Spinner:
    frames: str
    interval: int


default_spinner = Spinner("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏", 80)


@runtime_checkable
class SignalHandlerProtocol(Protocol):
    def __call__(self, signum: int, frame: Any, spinner: Yaspin) -> None: ...


def default_handler(signum: int, frame: Any, spinner: Yaspin) -> None:  # pylint: disable=unused-argument
    """Signal handler, used to gracefully shut down the ``spinner`` instance
    when specified signal is received by the process running the ``spinner``.

    ``signum`` and ``frame`` are mandatory arguments. Check ``signal.signal``
    function for more details.
    """
    spinner.fail()
    spinner.stop()
    sys.exit(0)


def fancy_handler(signum: int, frame: Any, spinner: Yaspin) -> None:  # pylint: disable=unused-argument
    """Signal handler, used to gracefully shut down the ``spinner`` instance
    when specified signal is received by the process running the ``spinner``.

    ``signum`` and ``frame`` are mandatory arguments. Check ``signal.signal``
    function for more details.
    """
    spinner.red.fail("✘")
    spinner.stop()
    sys.exit(0)


class Yaspin:  # pylint: disable=too-many-instance-attributes
    """Implements a context manager that spawns a thread
    to write spinner frames into a tty (stdout) during
    context execution.
    """

    # When Python finds its output attached to a terminal,
    # it sets the sys.stdout.encoding attribute to the terminal's encoding.
    # The print statement's handler will automatically encode unicode
    # arguments into bytes.
    def __init__(  # pylint: disable=too-many-arguments
        self,
        spinner: Spinner = default_spinner,
        text: str = "",
        color: Optional[str] = None,
        on_color: Optional[str] = None,
        attrs: Optional[Sequence[str]] = None,
        reversal: bool = False,
        side: str = "left",
        sigmap: Optional[dict[signal.Signals, SignalHandlers]] = None,
        timer: bool = False,
        ellipsis: str = "",
    ) -> None:
        # Spinner
        self._spinner = self._set_spinner(spinner)
        self._frames = self._set_frames(self._spinner, reversal)
        self._interval = self._set_interval(self._spinner)
        self._cycle = self._set_cycle(self._frames)

        # Color Specification
        self._color = self._set_color(color) if color else color
        self._on_color = self._set_on_color(on_color) if on_color else on_color
        self._attrs = self._set_attrs(attrs) if attrs else set()
        self._color_func = self._compose_color_func()

        # Other
        self._text = text
        self._side = self._set_side(side)
        self._reversal = reversal
        self._timer = timer
        self._ellipsis = ellipsis
        self._terminal_width: int = shutil.get_terminal_size().columns
        self._start_time: Optional[float] = None
        self._stop_time: Optional[float] = None

        # Helper flags
        self._stop_spin: Optional[threading.Event] = None
        self._hide_spin: Optional[threading.Event] = None
        self._spin_thread: Optional[threading.Thread] = None
        self._last_frame: Optional[str] = None
        self._stdout_lock = threading.Lock()
        self._hidden_level = 0
        self._cur_line_len = 0

        # Signals
        self._sigmap = sigmap if sigmap else {}
        # Maps signals to their default handlers in order to reset
        # custom handlers set by ``sigmap`` at the cleanup phase.
        self._dfl_sigmap: dict[signal.Signals, SignalHandlers] = {}

    # Dunders
    #
    def __repr__(self) -> str:
        return f"<Yaspin frames={self._frames!s}>"

    def __enter__(self) -> Yaspin:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self._spin_thread is None:
            raise RuntimeError("spin thread is None")
        # Avoid stop() execution for the 2nd time
        if self._spin_thread.is_alive():
            self.stop()

    def __call__(self, fn: Fn) -> Fn:
        @functools.wraps(fn)
        def inner(*args: Any, **kwargs: Any) -> Fn:
            with self:
                return fn(*args, **kwargs)

        return cast(Fn, inner)

    def __getattr__(self, name: str) -> Yaspin:
        # CLI spinners
        if name in SPINNER_ATTRS:
            from .spinners import Spinners  # pylint: disable=import-outside-toplevel

            sp = getattr(Spinners, name)
            self.spinner = sp
        # Color Attributes: "color", "on_color", "attrs"
        elif name in set(key for d in [ATTRIBUTES, COLORS, HIGHLIGHTS] for key in d):
            # Call appropriate property setters;
            # _color_func is updated automatically by setters.
            if name in ATTRIBUTES:
                self.attrs = [name]  # calls property setter
            if name in COLORS:
                setattr(self, "color", name)  # calls property setter
            if name in HIGHLIGHTS:
                setattr(self, "on_color", name)  # calls property setter
        # Side: "left" or "right"
        elif name in ("left", "right"):
            self.side = name  # calls property setter
        # Common error for unsupported attributes
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute: '{name}'")
        return self

    # Properties
    #
    @property
    def spinner(self) -> Spinner:
        return self._spinner

    @spinner.setter
    def spinner(self, sp: Spinner) -> None:
        self._spinner = self._set_spinner(sp)
        self._frames = self._set_frames(self._spinner, self._reversal)
        self._interval = self._set_interval(self._spinner)
        self._cycle = self._set_cycle(self._frames)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, txt: str) -> None:
        self._text = txt

    @property
    def color(self) -> Optional[str]:
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        self._color = self._set_color(value) if value else value
        self._color_func = self._compose_color_func()  # update

    @property
    def on_color(self) -> Optional[str]:
        return self._on_color

    @on_color.setter
    def on_color(self, value: str) -> None:
        self._on_color = self._set_on_color(value) if value else value
        self._color_func = self._compose_color_func()  # update

    @property
    def attrs(self) -> Sequence[str]:
        return list(self._attrs)

    @attrs.setter
    def attrs(self, value: Sequence[str]) -> None:
        new_attrs = self._set_attrs(value) if value else set()
        self._attrs = self._attrs.union(new_attrs)
        self._color_func = self._compose_color_func()  # update

    @property
    def side(self) -> str:
        return self._side

    @side.setter
    def side(self, value: str) -> None:
        self._side = self._set_side(value)

    @property
    def ellipsis(self) -> str:
        return self._ellipsis

    @ellipsis.setter
    def ellipsis(self, value: str) -> None:
        self._ellipsis = value

    @property
    def reversal(self) -> bool:
        return self._reversal

    @reversal.setter
    def reversal(self, value: bool) -> None:
        self._reversal = value
        self._frames = self._set_frames(self._spinner, self._reversal)
        self._cycle = self._set_cycle(self._frames)

    @property
    def elapsed_time(self) -> float:
        if self._start_time is None:
            return 0
        if self._stop_time is None:
            return time.time() - self._start_time
        return self._stop_time - self._start_time

    # Public
    #
    def start(self) -> None:
        if self._sigmap:
            self._register_signal_handlers()

        self._hide_cursor()
        self._start_time = time.time()
        # Reset value to properly calculate subsequent spinner starts (if any)
        self._stop_time = None
        self._stop_spin = threading.Event()
        self._hide_spin = threading.Event()
        self._spin_thread = threading.Thread(target=self._spin)
        try:
            self._spin_thread.start()
        finally:
            # Ensure cursor is not hidden if any failure occurs that prevents
            # getting it back
            self._show_cursor()

    def stop(self) -> None:
        self._stop_time = time.time()

        if self._dfl_sigmap:
            # Reset registered signal handlers to default ones
            self._reset_signal_handlers()

        if self._spin_thread is not None:
            if self._stop_spin is None:
                raise RuntimeError("stop_spin event is None")
            self._stop_spin.set()
            self._spin_thread.join()

        self._clear_line()
        self._show_cursor()

    def hide(self) -> None:
        """Hide the spinner to allow for custom writing to the terminal."""
        thr_is_alive = self._spin_thread and self._spin_thread.is_alive()
        if self._hide_spin is None:
            raise RuntimeError("hide_spin is None")

        if thr_is_alive and not self._hide_spin.is_set():
            with self._stdout_lock:
                # set the hidden spinner flag
                self._hide_spin.set()
                self._clear_line()

                # flush the stdout buffer so the current line
                # can be rewritten to
                sys.stdout.flush()

    @contextmanager
    def hidden(self) -> Generator[None, None, None]:
        """Hide the spinner within a block, can be nested"""
        if self._hidden_level == 0:
            self.hide()
        self._hidden_level += 1
        try:
            yield
        finally:
            self._hidden_level -= 1
            if self._hidden_level == 0:
                self.show()

    def show(self) -> None:
        """Show the hidden spinner."""
        thr_is_alive = self._spin_thread and self._spin_thread.is_alive()
        if self._hide_spin is None:
            raise RuntimeError("hide_spin is None")

        if thr_is_alive and self._hide_spin.is_set():
            with self._stdout_lock:
                # clear the hidden spinner flag
                self._hide_spin.clear()
                # clear the current line so the spinner is not appended to it
                self._clear_line()

    def write(self, text: str) -> None:
        """Write text in the terminal without breaking the spinner."""
        # similar to tqdm.write()
        # https://pypi.python.org/pypi/tqdm#writing-messages
        with self._stdout_lock:
            self._clear_line()
            if isinstance(text, (str, bytes)):
                _text = to_unicode(text)
            else:
                _text = str(text)
            sys.stdout.write(f"{_text}\n")
            self._cur_line_len = 0

    def ok(self, text: str = "OK") -> None:
        """Set Ok (success) finalizer to a spinner."""
        _text = text if text else "OK"
        self._freeze(_text)

    def fail(self, text: str = "FAIL") -> None:
        """Set fail finalizer to a spinner."""
        _text = text if text else "FAIL"
        self._freeze(_text)

    # Protected
    #
    @staticmethod
    def _warn_color_disabled() -> None:
        warnings.warn(
            "color, on_color and attrs are not supported when running in jupyter",
            stacklevel=3,
        )

    def _freeze(self, final_text: str) -> None:
        """Stop spinner, compose last frame and 'freeze' it."""
        text = to_unicode(final_text)
        self._last_frame = self._compose_out(text, mode="last")

        # Should be stopped here, otherwise prints after
        # self._freeze call will mess up the spinner
        self.stop()
        with self._stdout_lock:
            if self._last_frame is None:
                raise RuntimeError("last_frame is None")
            sys.stdout.write(self._last_frame)
            self._cur_line_len = 0

    def _spin(self) -> None:
        if self._stop_spin is None:
            raise RuntimeError("stop_spin is None")

        while not self._stop_spin.is_set():
            if self._hide_spin is not None and self._hide_spin.is_set():
                # Wait a bit to avoid wasting cycles
                time.sleep(self._interval)
                continue

            # Compose output
            spin_phase = next(self._cycle)
            out = self._compose_out(spin_phase)

            # Write
            with self._stdout_lock:
                self._clear_line()
                sys.stdout.write(out)
                sys.stdout.flush()
                self._cur_line_len = max(self._cur_line_len, len(out))

            # Wait
            self._stop_spin.wait(self._interval)

    def _compose_color_func(self) -> Optional[Callable[..., str]]:
        if self.is_jupyter():
            # ANSI Color Control Sequences are problematic in Jupyter
            return None

        return functools.partial(
            colored,
            color=self._color,
            on_color=self._on_color,
            attrs=list(self._attrs),
        )

    def _compose_out(self, frame: str, mode: Optional[str] = None) -> str:
        text = str(self._text)

        # Timer
        if self._timer:
            sec, fsec = divmod(round(100 * self.elapsed_time), 100)
            timer = " ({}.{:02.0f})".format(  # pylint: disable=consider-using-f-string
                timedelta(seconds=sec), fsec
            )
        else:
            timer = ""

        # Truncate
        max_text_len = self._get_max_text_length(len(frame), len(timer))
        if max_text_len < 1:
            raise ValueError(
                f"Terminal size {self._terminal_width} is too small to display spinner with the given settings."
            )
        text = text[:max_text_len] + self._ellipsis if len(text) > max_text_len else text

        # Colors
        if self._color_func is not None:
            frame = self._color_func(frame)

        # Position
        if self._side == "right":
            frame, text = text, frame

        # Mode
        if mode is None:
            out = f"\r{frame} {text}{timer}"
        else:
            out = f"{frame} {text}{timer}\n"

        return out

    def _get_max_text_length(self, frame_width: int, timer_width: int) -> int:
        ellipsis_width = len(self._ellipsis)
        # There is always a space between frame and text
        frame_width += 1

        return self._terminal_width - frame_width - timer_width - ellipsis_width

    def _register_signal_handlers(self) -> None:
        # SIGKILL cannot be caught or ignored, and the receiving
        # process cannot perform any clean-up upon receiving this
        # signal.
        if signal.SIGKILL in self._sigmap:
            raise ValueError(
                "Trying to set handler for SIGKILL signal. "
                "SIGKILL cannot be caught or ignored in POSIX systems."
            )
        for sig, sig_handler in self._sigmap.items():
            # A handler for a particular signal, once set, remains
            # installed until it is explicitly reset. Store default
            # signal handlers for subsequent reset at cleanup phase.
            dfl_handler = signal.getsignal(sig)
            self._dfl_sigmap[sig] = dfl_handler

            # ``signal.SIG_DFL`` and ``signal.SIG_IGN`` are also valid
            # signal handlers and are not callables.
            if callable(sig_handler) and isinstance(sig_handler, SignalHandlerProtocol):
                # ``signal.signal`` accepts handler function which is
                # called with two arguments: signal number and the
                # interrupted stack frame. ``functools.partial`` solves
                # the problem of passing spinner instance into the handler
                # function.
                sig_handler = functools.partial(sig_handler, spinner=self)

            signal.signal(sig, sig_handler)

    def _reset_signal_handlers(self) -> None:
        for sig, sig_handler in self._dfl_sigmap.items():
            signal.signal(sig, sig_handler)

    # Static
    #
    @staticmethod
    def is_jupyter() -> bool:
        return not sys.stdout.isatty()

    @staticmethod
    def _set_color(value: str) -> str:
        if Yaspin.is_jupyter():
            Yaspin._warn_color_disabled()

        if value not in COLORS:
            raise ValueError(
                "'{0}': unsupported color value. Use one of the: {1}".format(  # pylint: disable=consider-using-f-string
                    value, ", ".join(COLORS.keys())
                )
            )
        return value

    @staticmethod
    def _set_on_color(value: str) -> str:
        if Yaspin.is_jupyter():
            Yaspin._warn_color_disabled()

        if value not in HIGHLIGHTS:
            raise ValueError(
                "'{0}': unsupported on_color value. "  # pylint: disable=consider-using-f-string
                "Use one of the: {1}".format(value, ", ".join(HIGHLIGHTS.keys()))
            )
        return value

    @staticmethod
    def _set_attrs(attrs: Sequence[str]) -> set[str]:
        if Yaspin.is_jupyter():
            Yaspin._warn_color_disabled()

        for attr in attrs:
            if attr not in ATTRIBUTES:
                raise ValueError(
                    "'{0}': unsupported attribute value. "  # pylint: disable=consider-using-f-string
                    "Use one of the: {1}".format(attr, ", ".join(ATTRIBUTES.keys()))
                )
        return set(attrs)

    @staticmethod
    def _set_spinner(spinner: Spinner) -> Spinner:
        if hasattr(spinner, "frames") and hasattr(spinner, "interval"):
            if not spinner.frames or not spinner.interval:
                sp = default_spinner
            else:
                sp = spinner
        else:
            sp = default_spinner

        return sp

    @staticmethod
    def _set_side(side: str) -> str:
        if side not in ("left", "right"):
            raise ValueError("'{0}': unsupported side value. Use either 'left' or 'right'.")
        return side

    @staticmethod
    def _set_frames(spinner: Spinner, reversal: bool) -> Union[str, Sequence[str]]:
        uframes = None  # unicode frames
        uframes_seq = None  # sequence of unicode frames

        if isinstance(spinner.frames, str):
            uframes = spinner.frames

        # TODO (pavdmyt): support any type that implements iterable
        if isinstance(spinner.frames, (list, tuple)):
            # Empty ``spinner.frames`` is handled by ``Yaspin._set_spinner``
            if spinner.frames and isinstance(spinner.frames[0], bytes):
                uframes_seq = [to_unicode(frame) for frame in spinner.frames]
            else:
                uframes_seq = spinner.frames

        _frames = uframes or uframes_seq
        if not _frames:
            # Empty ``spinner.frames`` is handled by ``Yaspin._set_spinner``.
            # This code is very unlikely to be executed. However, it's still
            # here to be on a safe side.
            raise ValueError(f"{spinner!r}: no frames found in spinner")

        # Builtin ``reversed`` returns reverse iterator,
        # which adds unnecessary difficulty for returning
        # unicode value;
        # Hence using [::-1] syntax
        frames = _frames[::-1] if reversal else _frames

        return frames

    @staticmethod
    def _set_interval(spinner: Spinner) -> float:
        # Milliseconds to Seconds
        return spinner.interval * 0.001

    @staticmethod
    def _set_cycle(frames: Union[str, Sequence[str]]) -> Iterator[str]:
        return itertools.cycle(frames)

    @staticmethod
    def _hide_cursor() -> None:
        if sys.stdout.isatty():
            # ANSI Control Sequence DECTCEM 1 does not work in Jupyter
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

    @staticmethod
    def _show_cursor() -> None:
        if sys.stdout.isatty():
            # ANSI Control Sequence DECTCEM 2 does not work in Jupyter
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

    def _clear_line(self) -> None:
        if sys.stdout.isatty():
            # ANSI Control Sequence EL does not work in Jupyter
            sys.stdout.write("\r\033[K")
        else:
            fill = " " * self._cur_line_len
            sys.stdout.write(f"\r{fill}\r")
