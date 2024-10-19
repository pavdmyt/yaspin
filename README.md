![logo](https://raw.githubusercontent.com/pavdmyt/yaspin/master/static/logo_80.png)

# `yaspin`: Yet Another Terminal Spinner for Python

---

[![Coverage](https://codecov.io/gh/pavdmyt/yaspin/branch/master/graph/badge.svg)](https://codecov.io/gh/pavdmyt/yaspin)
[![pypi](https://img.shields.io/pypi/v/yaspin.svg)](https://pypi.org/project/yaspin/)
[![Versions](https://img.shields.io/pypi/pyversions/yaspin.svg)](https://pypi.org/project/yaspin/)

[![Wheel](https://img.shields.io/pypi/wheel/yaspin.svg)](https://pypi.org/project/yaspin/)
[![Examples](https://img.shields.io/badge/learn%20by-examples-0077b3.svg)](https://github.com/pavdmyt/yaspin/tree/master/examples)
[![DownloadsTot](https://static.pepy.tech/badge/yaspin)](https://pepy.tech/project/yaspin)
[![DownloadsW](https://static.pepy.tech/badge/yaspin/week)](https://pepy.tech/project/yaspin)

`Yaspin` provides a full-featured terminal spinner to show the progress during long-hanging operations.

![demo](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/demo.gif)

It is easy to integrate into existing codebase by using it as a [context manager](https://docs.python.org/3/reference/datamodel.html#context-managers)
or as a function [decorator](https://www.thecodeship.com/patterns/guide-to-python-function-decorators/):

```python
import time
from yaspin import yaspin

# Context manager:
with yaspin():
    time.sleep(3)  # time consuming code

# Function decorator:
@yaspin(text="Loading...")
def some_operations():
    time.sleep(3)  # time consuming code

some_operations()
```

**Yaspin** also provides an intuitive and powerful API. For example, you can easily summon a shark:

```python
import time
from yaspin import yaspin

with yaspin().white.bold.shark.on_blue as sp:
    sp.text = "White bold shark in a blue sea"
    time.sleep(5)
```

![shark](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/shark.gif)

## Features

- Runs at all major **CPython** versions (*3.9*, *3.10*, *3.11*, *3.12*, *3.13*), **PyPy**
- Supports all (70+) spinners from [cli-spinners](https://github.com/sindresorhus/cli-spinners)
- Supports all *colors*, *highlights*, *attributes* and their mixes from [termcolor](https://pypi.org/project/termcolor/) library
- Easy to combine with other command-line libraries, e.g. [prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit/)
- Flexible API, easy to integrate with existing code
- User-friendly API for handling POSIX [signals](https://www.computerhope.com/unix/signals.htm)
- Safe **pipes** and **redirects**:

```bash
$ python script_that_uses_yaspin.py > script.log
$ python script_that_uses_yaspin.py | grep ERROR
```

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Basic Example](#basic-example)
  - [Spinners from cli-spinners](#run-any-spinner-from-cli-spinners)
  - [Colors](#any-colour-you-like-)
  - [Advanced colors usage](#advanced-colors-usage)
  - [Building custom spinners](#run-any-spinner-you-want)
  - [Changing spinner properties on the fly](#change-spinner-properties-on-the-fly)
  - [Timer](#spinner-with-timer)
  - [Custom Ellipsis](#custom-ellipsis)
  - [Dynamic text](#dynamic-text)
  - [Writing messages](#writing-messages)
  - [Integration with other libraries](#integration-with-other-libraries)
  - [Handling POSIX signals](#handling-posix-signals)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Installation

From [PyPI](https://pypi.org/) using `pip` package manager:

```bash
pip install --upgrade yaspin
```

Or install the latest sources from GitHub:

```bash
pip install https://github.com/pavdmyt/yaspin/archive/master.zip
```

## Usage

### Basic Example

![basic_example](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/basic_example.gif)

```python
import time
from random import randint
from yaspin import yaspin

with yaspin(text="Loading", color="yellow") as spinner:
    time.sleep(2)  # time consuming code

    success = randint(0, 1)
    if success:
        spinner.ok("✅ ")
    else:
        spinner.fail("💥 ")
```

It is also possible to control spinner manually:

```python
import time
from yaspin import yaspin

spinner = yaspin()
spinner.start()

time.sleep(3)  # time consuming tasks

spinner.stop()
```

### Run any spinner from [cli-spinners](https://github.com/sindresorhus/cli-spinners)

![cli_spinners](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/cli_spinners.gif)

```python
import time
from yaspin import yaspin
from yaspin.spinners import Spinners

with yaspin(Spinners.earth, text="Earth") as sp:
    time.sleep(2)                # time consuming code

    # change spinner
    sp.spinner = Spinners.moon
    sp.text = "Moon"

    time.sleep(2)                # time consuming code
```

### Any Colour You Like [🌈](https://en.wikipedia.org/wiki/Any_Colour_You_Like)

![basic_colors](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/basic_colors.gif)

```python
import time
from yaspin import yaspin

with yaspin(text="Colors!") as sp:
    # Support all basic termcolor text colors
    colors = ("red", "green", "yellow", "blue", "magenta", "cyan", "white")

    for color in colors:
        sp.color, sp.text = color, color
        time.sleep(1)
```

### Advanced colors usage

![advanced_colors](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/advanced_colors.gif)

```python
import time
from yaspin import yaspin
from yaspin.spinners import Spinners

text = "Bold blink magenta spinner on cyan color"
with yaspin().bold.blink.magenta.bouncingBall.on_cyan as sp:
    sp.text = text
    time.sleep(3)

# The same result can be achieved by passing arguments directly
with yaspin(
    Spinners.bouncingBall,
    color="magenta",
    on_color="on_cyan",
    attrs=["bold", "blink"],
) as sp:
    sp.text = text
    time.sleep(3)
```

### Run any spinner you want

![custom_spinners](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/custom_spinners.gif)

```python
import time
from yaspin import yaspin, Spinner

# Compose new spinners with custom frame sequence and interval value
sp = Spinner(["😸", "😹", "😺", "😻", "😼", "😽", "😾", "😿", "🙀"], 200)

with yaspin(sp, text="Cat!"):
    time.sleep(3)  # cat consuming code :)
```

### Change spinner properties on the fly

![sp_properties](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/sp_properties.gif)

```python
import time
from yaspin import yaspin
from yaspin.spinners import Spinners

with yaspin(Spinners.noise, text="Noise spinner") as sp:
    time.sleep(2)

    sp.spinner = Spinners.arc  # spinner type
    sp.text = "Arc spinner"    # text along with spinner
    sp.color = "green"         # spinner color
    sp.side = "right"          # put spinner to the right
    sp.reversal = True         # reverse spin direction

    time.sleep(2)
```

### Spinner with timer

```python
import time
from yaspin import yaspin

with yaspin(text="elapsed time", timer=True) as sp:
    time.sleep(3.1415)
    sp.ok()
```

### Custom Ellipsis

If the text does not fit in the terminal it gets truncated, you can set a custom ellipsis to signal truncation.

```python
import time
from yaspin import yaspin

with yaspin(text="some long text", ellipsis="...") as sp:
     time.sleep(2)
```

### Dynamic text

```python
import time
from datetime import datetime
from yaspin import yaspin

class TimedText:
    def __init__(self, text):
        self.text = text
        self._start = datetime.now()

    def __str__(self):
        now = datetime.now()
        delta = now - self._start
        return f"{self.text} ({round(delta.total_seconds(), 1)}s)"

with yaspin(text=TimedText("time passed:")):
    time.sleep(3)
```

### Writing messages

![write_text](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/write_text.gif)

You should not write any message in the terminal using `print` while spinner is open.
To write messages in the terminal without any collision with `yaspin` spinner, a `.write()` method is provided:

```python
import time
from yaspin import yaspin

with yaspin(text="Downloading images", color="cyan") as sp:
    # task 1
    time.sleep(1)
    sp.write("> image 1 download complete")

    # task 2
    time.sleep(2)
    sp.write("> image 2 download complete")

    # finalize
    sp.ok("✔")
```

### Integration with other libraries

![hide_show](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/hide_show.gif)

Utilizing `hidden` context manager it is possible to toggle the display of
the spinner in order to call custom methods that write to the terminal. This is
helpful for allowing easy usage in other frameworks like [prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit/).
Using the powerful `print_formatted_text` function allows you even to apply
HTML formats and CSS styles to the output:

```python
import sys
import time

from yaspin import yaspin
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style

# override print with feature-rich ``print_formatted_text`` from prompt_toolkit
print = print_formatted_text

# build a basic prompt_toolkit style for styling the HTML wrapped text
style = Style.from_dict({
    'msg': '#4caf50 bold',
    'sub-msg': '#616161 italic'
})


with yaspin(text='Downloading images') as sp:
    # task 1
    time.sleep(1)
    with sp.hidden():
        print(HTML(
            u'<b>></b> <msg>image 1</msg> <sub-msg>download complete</sub-msg>'
        ), style=style)

    # task 2
    time.sleep(2)
    with sp.hidden():
        print(HTML(
            u'<b>></b> <msg>image 2</msg> <sub-msg>download complete</sub-msg>'
        ), style=style)

    # finalize
    sp.ok()
```

### Handling POSIX [signals](https://www.computerhope.com/unix/signals.htm)

Handling keyboard interrupts (pressing Control-C):

```python
import time

from yaspin import kbi_safe_yaspin


with kbi_safe_yaspin(text="Press Control+C to send SIGINT (Keyboard Interrupt) signal"):
    time.sleep(5)  # time consuming code
```

Handling other types of signals:

```python
import os
import time
from signal import SIGTERM, SIGUSR1

from yaspin import yaspin
from yaspin.signal_handlers import default_handler, fancy_handler


sigmap = {SIGUSR1: default_handler, SIGTERM: fancy_handler}
with yaspin(sigmap=sigmap, text="Handling SIGUSR1 and SIGTERM signals") as sp:
    sp.write("Send signals using `kill` command")
    sp.write("E.g. $ kill -USR1 {0}".format(os.getpid()))
    time.sleep(20)  # time consuming code
```

More [examples](https://github.com/pavdmyt/yaspin/tree/master/examples).

## Development

Clone the repository:

```bash
git clone https://github.com/pavdmyt/yaspin.git
```

Install dev dependencies:

```bash
poetry install

# if you don't have poetry installed:
pip install -r requirements.txt
```

Lint code:

```bash
make lint
```

Format code:

```bash
make fmt
```

Run tests:

```bash
make test
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
6. Make sure tests are passing

## License

* MIT - Pavlo Dmytrenko; https://twitter.com/pavdmyt
* Contains data from [cli-spinners](https://github.com/sindresorhus/cli-spinners): MIT License, Copyright (c) Sindre Sorhus sindresorhus@gmail.com (sindresorhus.com)
