# AGENTS.md

This file provides guidance to AI agents when working with code in this repository.

## Commands

All development goes through Poetry + the Makefile:

```bash
poetry install         # install dev dependencies
make test              # pytest -n auto -v (clears .pyc first; verbose output)
make coverage          # term + html + xml coverage reports
make lint              # ruff check --fix
make check-lint        # ruff check --diff (what CI runs)
make fmt               # ruff format
make check-fmt         # ruff format --check (what CI runs)
make mypy              # mypy yaspin/
make semgrep           # p/secrets + p/bandit rulesets
make spellcheck        # cspell (needs cspell installed globally, not via poetry)
make build             # poetry build
make bump / bump-minor # poetry version patch/minor
```

Run the full suite with compact output to avoid filling the context window:

```bash
poetry run py.test -n auto
```

If a test fails, probe the relevant subset with pytest's `-k` expression:

```bash
poetry run py.test -k "ellipsis"
```

`-k EXPRESSION` only runs tests whose names match the given substring.

Note `make test` uses `pytest-xdist` (`-n auto`); drop `-n` when debugging with breakpoints or when
test ordering matters. CI sets `PYTHONHASHSEED=0`.

Supported Python: 3.10–3.14 plus PyPy 3.11. `ruff` targets py310 with `line-length = 110`; do not use
syntax newer than 3.10.

## Commits

Every commit message must use a descriptive prefix followed by a colon, for example
`deps: update`. Use the `ai:` prefix for commits that update this `AGENTS.md` file.

Keep the subject concise. Put motivation and relevant context in a multi-line commit body, with
each line wrapped to 90 characters or fewer.

## Architecture

A single-purpose library: a threaded terminal spinner. Four modules under `yaspin/`.

**`core.py` — everything real lives here.** `Yaspin` is the whole implementation (~800 lines):

- **Threading model.** `start()` spawns a daemon-less `threading.Thread` running `_spin()`, which loops
  until the `_stop_spin` `threading.Event` is set, composing a frame and writing it each `_interval`.
  A second event, `_hide_spin`, pauses drawing without stopping the thread. All writes to the stream go
  through `self._stream_lock`, so any new code that writes output must take that lock or it will
  interleave with spinner frames.
- **Rendering.** `_compose_out()` builds `\r{frame} {text}{timer}` for live frames and
  `{frame} {text}{timer}\n` for the frozen final frame (`mode="last"`). Text is truncated to
  `_get_max_text_length()` based on `shutil.get_terminal_size()` captured once at `__init__`, with the
  configurable `ellipsis` appended. `side="right"` simply swaps `frame` and `text`.
- **Stream abstraction.** `SafeStreamWrapper` wraps the target stream (default `sys.stdout`) and makes
  every operation safe against a closed stream — `write`/`flush` become no-ops, `isatty()` returns
  False, and unknown attributes are delegated via `__getattr__`. Warning on closed-stream writes is
  opt-in via `warn_on_closed_stream=True`.
- **TTY-conditional behavior.** `_supports_ansi_codes()` (i.e.  `stream.isatty()`) gates cursor hide/show,
  the `\r\033[K` clear sequence, and coloring. On a non-TTY stream `_clear_line()` falls back to overwriting
  with spaces tracked in `_cur_line_len`, `_compose_color_func()` returns `None` (no color at all), and the
  color setters emit a warning. Any change to output composition must be verified against both branches;
  `tests/test_stream.py` covers the non-TTY path with `io.StringIO`.
- **Fluent attribute API.** `__getattr__` turns unknown attribute access into configuration and returns
  `self`, so `sp.red.bold.dots.right` works. It dispatches against `SPINNER_ATTRS` (from
  `constants.py`), termcolor's `COLORS`/`HIGHLIGHTS`/`ATTRIBUTES` dicts, and `"left"`/`"right"`, by
  calling the corresponding property setters. Adding a new configurable name means adding it to that
  dispatch chain *and* giving it a property setter that refreshes derived state (`_frames`, `_cycle`,
  `_color_func`).
- **Signals.** `sigmap` maps signals to handlers; `_register_signal_handlers()` stores the previous
  handler in `_dfl_sigmap` for restoration in `stop()`, rejects `SIGKILL`, and uses
  `functools.partial(handler, spinner=self)` for handlers matching `SignalHandlerProtocol` (the
  three-arg `signum, frame, spinner` form). Non-callable handlers (`SIG_DFL`, `SIG_IGN`) pass through.

**`api.py` — the public surface.** `yaspin()` (context manager / decorator factory), `kbi_safe_yaspin()`
(same but forces `{SIGINT: default_handler}`), and `inject_spinner()` (decorator that passes the live
spinner as the first positional argument). The user-facing docstring for every option lives on
`yaspin()`; keep it in sync with `Yaspin.__init__` when adding parameters. Note the
`if yaspin.__doc__:` guard at the bottom — code must tolerate `PYTHONOPTIMIZE=2` stripping docstrings.

**`spinners.py` / `data/spinners.json`.** The cli-spinners dataset is vendored as JSON and parsed at
import time into namedtuples via a `json` `object_hook`, exposed as `Spinners.<name>`. `constants.py`
holds `SPINNER_ATTRS`, a hand-maintained list of those names used by `__getattr__`; regenerate it with
`jq '. | keys' yaspin/data/spinners.json` when the dataset is updated.

## Testing conventions

`tests/conftest.py` holds parametrized session-scoped fixtures covering the hard cases (empty/ascii/
non-ascii/bytes frames and text, every termcolor color and highlight, valid and invalid values, all
sigmap shapes). Prefer extending those fixture parameter lists over writing one-off tests — most test
modules just consume `frames`, `text`, `side`, `reversal`, `final_text`, `sigmap_test_cases`.

An autouse fixture monkeypatches `sys.stdout.isatty` to return `True`, so the default test environment
behaves like a terminal; tests that need the non-TTY path must pass an explicit `io.StringIO` stream
or patch `isatty` themselves.

## Release

Version lives only in `pyproject.toml` (`make bump`). Add an entry to `HISTORY.rst` in the existing
`X.Y.Z / YYYY-MM-DD` format. Publishing to PyPI is handled by `.github/workflows/publish-to-pypi.yml`.

New user-facing features conventionally get a runnable example in `examples/` and a README section.
`make spellcheck` runs cspell over `yaspin/`, `tests/`, `examples/`, `README.md`, `HISTORY.rst`,
`pyproject.toml`, and `Makefile` — add project-specific words to `yaspin-spellcheck-dict.txt`.
