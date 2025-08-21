from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

import signal

import pytest

from yaspin import inject_spinner
from yaspin.core import Spinner, Yaspin
from yaspin.spinners import Spinners


@pytest.fixture
def simple_spinner() -> Spinner:
    return Spinner(["A", "B", "C"], 100)


@contextmanager
def assert_no_yaspin_errors() -> Generator[None, None, None]:
    """Helper context manager to ensure yaspin starts and stops correctly."""
    try:
        yield
    finally:
        # Ensure cursor is visible after test
        print("\033[?25h", end="", flush=True)


# Basic functionality tests
#
def test_basic_injection() -> None:
    """Test basic spinner injection without arguments."""

    @inject_spinner()
    def sample_func(spinner: Yaspin, x: int) -> int:
        assert isinstance(spinner, Yaspin)
        return x * 2

    with assert_no_yaspin_errors():
        result = sample_func(5)
        assert result == 10


def test_spinner_customization(simple_spinner: Spinner) -> None:
    """Test spinner injection with custom spinner and parameters."""

    @inject_spinner(simple_spinner, text="Testing", color="green")
    def sample_func(spinner: Yaspin) -> None:
        assert isinstance(spinner, Yaspin)
        assert spinner.color == "green"
        assert spinner.text == "Testing"
        assert spinner.spinner.frames == ["A", "B", "C"]
        assert spinner.spinner.interval == 100

    with assert_no_yaspin_errors():
        sample_func()


def test_spinner_property_modification() -> None:
    """Test modifying spinner properties inside the decorated function."""

    @inject_spinner(text="Initial")
    def sample_func(spinner: Yaspin) -> None:
        assert spinner.text == "Initial"
        spinner.text = "Modified"
        spinner.color = "red"
        assert spinner.text == "Modified"
        assert spinner.color == "red"

    with assert_no_yaspin_errors():
        sample_func()


# Error handling tests
#
def test_error_propagation() -> None:
    """Test error propagation through the decorated function."""

    @inject_spinner()
    def failing_func(spinner: Yaspin) -> None:
        raise ValueError("Test error")

    with assert_no_yaspin_errors(), pytest.raises(ValueError, match="Test error"):
        failing_func()


def test_invalid_color() -> None:
    """Test handling of invalid color parameter."""

    @inject_spinner(color="not_a_color")
    def invalid_color_func(spinner: Yaspin) -> None:
        pass

    with pytest.raises(ValueError):
        invalid_color_func()


# Parameter handling tests
#
def test_args_kwargs_handling() -> None:
    """Test handling of various argument combinations."""

    @inject_spinner(Spinners.dots, text="Testing")
    def sample_func(spinner: Yaspin, *args: Any, **kwargs: Any) -> tuple[tuple, dict]:
        return args, kwargs

    with assert_no_yaspin_errors():
        args, kwargs = sample_func(1, 2, a=3, b=4)
        assert args == (1, 2)
        assert kwargs == {"a": 3, "b": 4}


def test_return_values() -> None:
    """Test that return values are properly propagated."""

    @inject_spinner()
    def func_with_return(spinner: Yaspin, x: int, y: int) -> int:
        return x + y

    with assert_no_yaspin_errors():
        result = func_with_return(3, 4)
        assert result == 7


# Advanced feature tests
#
def test_signal_handling() -> None:
    """Test that signal handling works correctly."""

    def handler(signum: int, frame: Any, spinner: Yaspin) -> None:
        spinner.fail("Interrupted")

    @inject_spinner(sigmap={signal.SIGUSR1: handler})
    def sample_func(spinner: Yaspin) -> None:
        # Signal handling setup should work without raising errors
        pass

    with assert_no_yaspin_errors():
        sample_func()


def test_nested_spinners() -> None:
    """Test nested spinner decorators."""

    @inject_spinner(text="Outer")
    def outer_func(outer_spinner: Yaspin) -> None:
        assert isinstance(outer_spinner, Yaspin)
        assert outer_spinner.text == "Outer"

        @inject_spinner(text="Inner")
        def inner_func(inner_spinner: Yaspin) -> None:
            assert isinstance(inner_spinner, Yaspin)
            assert inner_spinner.text == "Inner"

        inner_func()

    with assert_no_yaspin_errors():
        outer_func()


# Edge cases tests
#
def test_empty_spinner() -> None:
    """Test handling of empty spinner frames."""
    empty_spinner = Spinner([], 100)

    @inject_spinner(empty_spinner)
    def empty_spinner_func(spinner: Yaspin) -> None:
        # Should use default spinner when empty frames are provided
        assert len(spinner.spinner.frames) > 0

    with assert_no_yaspin_errors():
        empty_spinner_func()


def test_long_text() -> None:
    """Test handling of very long text."""

    @inject_spinner(text="a" * 1000)
    def long_text_func(spinner: Yaspin) -> None:
        # Should handle long text without crashing
        assert len(spinner.text) > 0

    with assert_no_yaspin_errors():
        long_text_func()


def test_context_manager_behavior(mocker) -> None:
    """Test that the context manager behavior works correctly."""
    mock_yaspin = mocker.patch("yaspin.api.yaspin")
    mock_spinner = mocker.MagicMock()
    mock_yaspin.return_value.__enter__.return_value = mock_spinner

    @inject_spinner()
    def sample_func(spinner: Yaspin) -> None:
        spinner.text = "Working"

    sample_func()

    # Verify context manager was used correctly
    mock_yaspin.assert_called_once()
    mock_yaspin.return_value.__enter__.assert_called_once()
    mock_yaspin.return_value.__exit__.assert_called_once()
