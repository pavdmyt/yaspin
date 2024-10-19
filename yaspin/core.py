# :copyright: (c) 2021 by Pavlo Dmytrenko.
# :license: MIT, see LICENSE for more details.

"""
yaspin.core
~~~~~~~~~~~

A lightweight terminal spinner.
"""

from __future__ import annotations

from collections.abc import Generator, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import timedelta
from typing import (
    Any,
    Callable,
    cast,
    Final,
    Optional,
    Protocol,
    runtime_checkable,
    TYPE_CHECKING,
    TypeVar,
    Union,
)

import functools
import itertools
import shutil
import signal
import sys
import threading
import time
import warnings

from termcolor import ATTRIBUTES, colored, COLORS, HIGHLIGHTS

from .constants import SPINNER_ATTRS

if TYPE_CHECKING:
    from types import FrameType, TracebackType

    SignalHandlers = Union[Callable[[int, Optional[FrameType]], Any], int, None]

Fn = TypeVar("Fn", bound=Callable[..., Any])

ENCODING: Final[str] = "utf-8"


def to_unicode(text_type: str | bytes, encoding: str = ENCODING) -> str:
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


def default_handler(signum: int, frame: Any, spinner: Yaspin) -> None:
    """Signal handler, used to gracefully shut down the ``spinner`` instance
    when specified signal is received by the process running the ``spinner``.

    ``signum`` and ``frame`` are mandatory arguments. Check ``signal.signal``
    function for more details.
    """
    spinner.fail()
    spinner.stop()
    sys.exit(0)


def fancy_handler(signum: int, frame: Any, spinner: Yaspin) -> None:
    """Signal handler, used to gracefully shut down the ``spinner`` instance
    when specified signal is received by the process running the ``spinner``.

    ``signum`` and ``frame`` are mandatory arguments. Check ``signal.signal``
    function for more details.
    """
    spinner.red.fail("✘")
    spinner.stop()
    sys.exit(0)


class Yaspin:
    """Implements a context manager that spawns a thread
    to write spinner frames into a tty (stdout) during
    context execution.
    """

    # When Python finds its output attached to a terminal,
    # it sets the sys.stdout.encoding attribute to the terminal's encoding.
    # The print statement's handler will automatically encode unicode
    # arguments into bytes.
    def __init__(
        self,
        spinner: Spinner = default_spinner,
        text: str = "",
        color: str | None = None,
        on_color: str | None = None,
        attrs: Sequence[str] | None = None,
        reversal: bool = False,
        side: str = "left",
        sigmap: dict[signal.Signals, SignalHandlers] | None = None,
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
        self._start_time: float | None = None
        self._stop_time: float | None = None

        # Helper flags
        self._stop_spin: threading.Event | None = None
        self._hide_spin: threading.Event | None = None
        self._spin_thread: threading.Thread | None = None
        self._last_frame: str | None = None
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
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
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
            from .spinners import Spinners

            sp = getattr(Spinners, name)
            self.spinner = sp
        # Color Attributes: "color", "on_color", "attrs"
        elif name in set(key for d in [ATTRIBUTES, COLORS, HIGHLIGHTS] for key in d):
            # Call appropriate property setters;
            # _color_func is updated automatically by setters.
            if name in ATTRIBUTES:
                self.attrs = [name]  # calls property setter
            if name in COLORS:
                self.color = name  # calls property setter
            if name in HIGHLIGHTS:
                self.on_color = name  # calls property setter
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
    def color(self) -> str | None:
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        self._color = self._set_color(value) if value else value
        self._color_func = self._compose_color_func()  # update

    @property
    def on_color(self) -> str | None:
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
        """
        Start the spinner animation in a separate thread.

        Initializes and starts the spinner animation by hiding the cursor, recording
        the start time, and creating a new thread to run the spinner. It also
        sets up necessary threading events to control the spinner's behavior.

        If signal handlers are registered, they will be set up before starting the spinner.

        In case of any failure that prevents the spinner from starting, the cursor will
        be shown to ensure it is not left hidden.
        """
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
        """
        Stops the spinner and performs necessary cleanup.

        Records the stop time, resets signal handlers to their default if
        they were modified, stops the spinning thread, clears the spinner
        line, and shows the cursor.

        Raises:
            RuntimeError: If the stop_spin event is None.
        """
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
        """
        Hide the spinner to allow for custom writing to the terminal.

        Sets a flag to indicate that the spinner should be hidden, clears
        the current line in the terminal, and flushes the stdout buffer.
        It ensures that the spinner thread is alive and the hide flag is
        not already set before performing these actions.

        Raises:
            RuntimeError: If the hide_spin attribute is None.
        """
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
        """
        Temporarily hides the spinner within a context block. This method can be nested.

        When the context is entered, the spinner is hidden if it is not already hidden.
        When the context is exited, the spinner is shown again if it was hidden by this method.

        Yields:
            None: This method is a generator that yields control back to the caller.
        """
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
        """
        Show the hidden spinner.

        Checks if the spinner thread is alive and if the spinner is currently
        hidden. If both conditions are met, it clears the hidden spinner
        flag and clears the current line to ensure the spinner is not
        appended to it.

        Raises:
            RuntimeError: If the `_hide_spin` attribute is `None`.
        """
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
        """
        Write text in the terminal without breaking the spinner.

        Ensures that the spinner is temporarily cleared, the text
        is written to the terminal, and then the spinner is restored.

        Args:
            text (str): The text to be written to the terminal.
        """
        # similar to tqdm.write()
        # https://pypi.python.org/pypi/tqdm#writing-messages
        with self._stdout_lock:
            self._clear_line()
            _text = to_unicode(text) if isinstance(text, (str, bytes)) else str(text)
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
        """
        Stop the spinner and display the final frame.

        Stops the spinner, composes the last frame with the provided final text,
        and 'freezes' it by writing the final frame to the standard output.

        Args:
            final_text (str): The final text to be displayed when the spinner stops.

        Raises:
            RuntimeError: If the last frame is None.
        """
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
        """
        Handles the spinning animation.

        Continuously updates the spinner's output on the terminal until
        the `_stop_spin` event is set. If the `_hide_spin` event is set,
        it temporarily pauses the spinning.

        Raises:
            RuntimeError: If `_stop_spin` is None.
        """
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

    def _compose_color_func(self) -> Callable[..., str] | None:
        """
        Compose a color function based on the current environment.

        If the environment is Jupyter, returns None as ANSI color control sequences
        are problematic in Jupyter notebooks. Otherwise, returns a partial function
        that applies the specified color, background color, and attributes to text.
        """
        if self.is_jupyter():
            # ANSI Color Control Sequences are problematic in Jupyter
            return None

        return functools.partial(
            colored,
            color=self._color,
            on_color=self._on_color,
            attrs=list(self._attrs),
        )

    def _compose_out(self, frame: str, mode: str | None = None) -> str:
        """
        Compose the output string for the spinner.

        Args:
            frame (str): The current frame of the spinner animation.
            mode (str, optional): The mode in which the output is generated. If None,
                                  the output is generated on the same line with a carriage
                                  return. If a value is provided, the output is generated
                                  on a new line.

        Returns:
            str: The composed output string including the spinner frame, text, timer,
                 and any specified colors and positions.

        Raises:
            ValueError: If the terminal size is too small to display the spinner with
                        the given settings.
        """
        text = str(self._text)

        # Timer
        if self._timer:
            sec, fsec = divmod(round(100 * self.elapsed_time), 100)
            timer = f" ({timedelta(seconds=sec)}.{fsec:02.0f})"
        else:
            timer = ""

        # Truncate
        max_text_len = self._get_max_text_length(len(frame), len(timer))
        if max_text_len < 1:
            raise ValueError(
                f"Terminal size {self._terminal_width} is too small to display spinner "
                "with the given settings."
            )
        text = text[:max_text_len] + self._ellipsis if len(text) > max_text_len else text

        # Colors
        if self._color_func is not None:
            frame = self._color_func(frame)

        # Position
        if self._side == "right":
            frame, text = text, frame

        # Mode
        out = f"\r{frame} {text}{timer}" if mode is None else f"{frame} {text}{timer}\n"

        return out

    def _get_max_text_length(self, frame_width: int, timer_width: int) -> int:
        """
        Calculate the maximum length of text that can be displayed within the terminal width.

        Args:
            frame_width (int): The width of the frame.
            timer_width (int): The width of the timer.

        Returns:
            int: The maximum length of text that can be displayed.
        """
        ellipsis_width = len(self._ellipsis)
        # There is always a space between frame and text
        frame_width += 1

        return self._terminal_width - frame_width - timer_width - ellipsis_width

    def _register_signal_handlers(self) -> None:
        """
        Registers custom signal handlers for the spinner.

        Sets up signal handlers defined in the `_sigmap` attribute.
        It ensures that SIGKILL is not included. For each signal in
        `_sigmap`, stores the default signal handler for later restoration
        during the cleanup phase.

        Raises:
            ValueError: If an attempt is made to set a handler for the SIGKILL signal.
        """
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
        """Resets the signal handlers to their default values."""
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
                "'{}': unsupported color value. Use one of the: {}".format(value, ", ".join(COLORS.keys()))
            )
        return value

    @staticmethod
    def _set_on_color(value: str) -> str:
        if Yaspin.is_jupyter():
            Yaspin._warn_color_disabled()

        if value not in HIGHLIGHTS:
            raise ValueError(
                "'{}': unsupported on_color value. " "Use one of the: {}".format(
                    value, ", ".join(HIGHLIGHTS.keys())
                )
            )
        return value

    @staticmethod
    def _set_attrs(attrs: Sequence[str]) -> set[str]:
        if Yaspin.is_jupyter():
            Yaspin._warn_color_disabled()

        for attr in attrs:
            if attr not in ATTRIBUTES:
                raise ValueError(
                    "'{}': unsupported attribute value. " "Use one of the: {}".format(
                        attr, ", ".join(ATTRIBUTES.keys())
                    )
                )
        return set(attrs)

    @staticmethod
    def _set_spinner(spinner: Spinner) -> Spinner:
        if hasattr(spinner, "frames") and hasattr(spinner, "interval"):
            sp = default_spinner if not spinner.frames or not spinner.interval else spinner
        else:
            sp = default_spinner

        return sp

    @staticmethod
    def _set_side(side: str) -> str:
        if side not in ("left", "right"):
            raise ValueError("'{0}': unsupported side value. Use either 'left' or 'right'.")
        return side

    @staticmethod
    def _set_frames(spinner: Spinner, reversal: bool) -> str | Sequence[str]:
        """
        Set the frames for the spinner, optionally reversing them.

        Args:
            spinner (Spinner): The spinner object containing the frames.
            reversal (bool): If True, the frames will be reversed.

        Returns:
            Union[str, Sequence[str]]: The frames to be used for the spinner.
            This can be a single string of frames or a sequence of frame strings.

        Raises:
            ValueError: If no frames are found in the spinner.
        """
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
    def _set_cycle(frames: str | Sequence[str]) -> Iterator[str]:
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
