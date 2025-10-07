"""
tests.test_stream
~~~~~~~~~~~~~~~~~

Tests for the stream parameter functionality in yaspin.
"""

import io
import sys
import threading
import time
import warnings

import pytest

from yaspin import yaspin


def test_stream_parameter_default():
    """Test that default stream parameter uses sys.stdout"""
    sp = yaspin()
    assert sp._stream._stream == sys.stdout  # Check underlying stream
    assert sp._stream_lock is not None


def test_stream_parameter_explicit_stdout():
    """Test explicit sys.stdout stream parameter."""
    sp = yaspin(stream=sys.stdout)
    assert sp._stream._stream == sys.stdout


def test_stream_parameter_explicit_stderr():
    """Test explicit sys.stderr stream parameter."""
    sp = yaspin(stream=sys.stderr)
    assert sp._stream._stream == sys.stderr


def test_stream_parameter_custom_stringio():
    """Test custom StringIO stream parameter."""
    custom_stream = io.StringIO()
    sp = yaspin(stream=custom_stream)
    assert sp._stream._stream == custom_stream


def test_stream_parameter_none():
    """Test that None stream parameter defaults to sys.stdout"""
    sp = yaspin(stream=None)
    assert sp._stream._stream == sys.stdout


def test_stream_write_method_uses_custom_stream():
    """Test that write() method uses the custom stream."""
    custom_stream = io.StringIO()

    with yaspin(stream=custom_stream, text="Test") as sp:
        sp.write("Test message")

    output = custom_stream.getvalue()
    assert "Test message" in output


def test_stream_spinner_output_uses_custom_stream():
    """Test that spinner frames use the custom stream."""
    custom_stream = io.StringIO()
    text = "Test"

    with yaspin(stream=custom_stream, text=text):
        time.sleep(0.1)  # Allow some spinner frames

    output = custom_stream.getvalue()
    # Should contain spinner characters and text
    assert text in output
    assert len(output) > len(text)


def test_stream_ok_method_use_custom_stream():
    """Test that ok() method use the custom stream."""
    custom_stream = io.StringIO()
    sp = yaspin(stream=custom_stream)
    sp.start()
    sp.ok("Success")

    output = custom_stream.getvalue()
    assert "Success" in output


def test_stream_fail_method_use_custom_stream():
    """Test that fail() method use the custom stream."""
    custom_stream = io.StringIO()
    sp = yaspin(stream=custom_stream)
    sp.start()
    sp.fail("Failed")

    output = custom_stream.getvalue()
    assert "Failed" in output


def test_stream_cursor_methods_respect_tty():
    """Test that cursor hide/show methods respect stream's tty status."""
    # With StringIO (not a tty), cursor methods should be safe
    custom_stream = io.StringIO()

    sp = yaspin(stream=custom_stream)
    sp._hide_cursor()  # Should not write ANSI codes to non-tty
    sp._show_cursor()  # Should not write ANSI codes to non-tty

    output = custom_stream.getvalue()
    assert "\033[?25l" not in output  # Hide cursor ANSI code
    assert "\033[?25h" not in output  # Show cursor ANSI code


def test_stream_clear_line_method():
    """Test that _clear_line() method works with custom streams."""
    custom_stream = io.StringIO()

    sp = yaspin(stream=custom_stream)
    sp._cur_line_len = 10
    sp._clear_line()

    output = custom_stream.getvalue()
    # For non-tty streams, should use space clearing method
    assert " " * 10 in output or "\r" in output


def test_stream_thread_safety():
    """Test that stream operations are thread-safe with multiple threads."""
    custom_stream = io.StringIO()
    results = []
    errors = []

    def worker(worker_id):
        try:
            with yaspin(stream=custom_stream, text=f"Worker {worker_id}"):
                time.sleep(0.05)
                results.append(worker_id)
        except Exception as e:
            errors.append((worker_id, str(e)))

    # Start multiple threads
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    # Verify no errors occurred
    assert len(errors) == 0, f"Thread safety errors: {errors}"
    assert len(results) == 5, f"Expected 5 results, got {len(results)}"


@pytest.mark.parametrize(
    "kwargs",
    [
        {"text": "Test"},
        {"text": "Test", "color": "red"},
        {"text": "Test", "timer": True},
        {"text": "Test", "side": "right"},
    ],
)
def test_stream_parameter_with_other_parameters(kwargs):
    """Test that stream parameter works correctly with other yaspin parameters."""
    custom_stream = io.StringIO()
    kwargs["stream"] = custom_stream

    sp = yaspin(**kwargs)
    assert sp._stream._stream == custom_stream

    # Test that it can start and stop without issues
    assert sp._spin_thread is None
    sp.start()
    assert sp._spin_thread is not None
    assert sp._spin_thread.is_alive()
    time.sleep(0.01)
    sp.stop()
    assert not sp._spin_thread.is_alive()

    # Verify that output was written to the custom stream
    output = custom_stream.getvalue()
    assert len(output) > 0, "Expected output to be written to custom stream"


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"text": "Test"},
        {"text": "Test", "color": "green"},
        {"text": "Test", "timer": True},
    ],
)
def test_stream_backward_compatibility(kwargs):
    """Test that existing code without stream parameter still works."""
    sp = yaspin(**kwargs)
    assert sp._stream._stream == sys.stdout  # Should default to stdout

    # Should be able to start and stop
    assert sp._spin_thread is None
    sp.start()
    assert sp._spin_thread is not None
    assert sp._spin_thread.is_alive()
    time.sleep(0.01)
    sp.stop()
    assert not sp._spin_thread.is_alive()


@pytest.mark.parametrize(
    "stream_obj",
    [
        sys.stdout,
        sys.stderr,
        io.StringIO(),
    ],
)
def test_stream_parameter_types(stream_obj):
    """Test that different stream types work correctly."""
    sp = yaspin(stream=stream_obj)
    assert sp._stream._stream == stream_obj

    # Should be able to use basic functionality
    with sp:
        time.sleep(0.01)


def test_warn_on_closed_stream_disabled():
    # Test with warnings disabled (default)
    custom_stream = io.StringIO()
    sp = yaspin(stream=custom_stream, warn_on_closed_stream=False)
    custom_stream.close()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sp.write("test message")
        # Should not emit any warnings
        assert len(w) == 0


def test_warn_on_closed_stream_enabled():
    # Test with warnings enabled
    custom_stream = io.StringIO()
    sp = yaspin(stream=custom_stream, warn_on_closed_stream=True)
    custom_stream.close()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sp.write("test message")
        # Should emit exactly one warning
        assert len(w) == 1
        assert issubclass(w[0].category, UserWarning)
        assert "closed stream" in str(w[0].message)

        # Second write should not emit another warning (rate limiting)
        sp.write("second message")
        assert len(w) == 1  # Still just one warning
