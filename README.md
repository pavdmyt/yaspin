# yaspin

[![travis][travis-image]][travis-url] [![cov][cov-image]][cov-url] [![codacy][codacy-image]][codacy-url]

[![pypi][pypi-image]][pypi-url] [![pyver][pyver-image]][pyver-url]

[![examples][examples-image]][examples-url]

**Y**et **A**nother Terminal **Spin**ner for Python.

**Yaspin** provides a full-featured terminal spinner to show the progress during long-hanging operations.

![demo](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/demo.gif)

It is easy to integrate into existing codebase by using it as a [context manager](https://docs.python.org/3/reference/datamodel.html#context-managers) or as a function [decorator](https://www.thecodeship.com/patterns/guide-to-python-function-decorators/):

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


## Features

* No external dependencies
* Runs at all major __CPython__ versions (_2.6_, _2.7_, _3.3_, _3.4_, _3.5_, _3.6_), __PyPy__ and __PyPy3__
* Supports all (60+) spinners from [cli-spinners](https://github.com/sindresorhus/cli-spinners)
* Supports all _colors_, _highlights_, _attributes_ and their mixes from [termcolor](https://pypi.python.org/pypi/termcolor) library
* Flexible API, easy to integrate with existing code
* Safe __pipes__ and __redirects__:

```
$ python script_that_uses_yaspin.py > script.log
$ python script_that_uses_yaspin.py | grep ERROR
```


## Installation

From [PyPI](https://pypi.python.org/pypi) using `pip` package manager:

```
pip install --upgrade yaspin
```

Or install the latest sources from GitHub:

```
pip install https://github.com/pavdmyt/yaspin/archive/master.zip
```


## Usage

### Basic example:

![basic](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/basic_example.gif)

```python
# -*- coding: utf-8 -*-
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
# -*- coding: utf-8 -*-
import time
from yaspin import yaspin

spinner = yaspin()
spinner.start()

time.sleep(3)  # time consuming tasks

spinner.stop()
```

### Run any spinner from [cli-spinners](https://github.com/sindresorhus/cli-spinners):

![cli-sp](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/cli_spinners.gif)

```python
# -*- coding: utf-8 -*-
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

### Any Colour You Like [🌈](https://en.wikipedia.org/wiki/Any_Colour_You_Like):

![colors](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/basic_colors.gif)

```python
# -*- coding: utf-8 -*-
import time
from yaspin import yaspin

with yaspin(text="Colors!") as sp:
    # Support all basic termcolor text colors
    colors = ("red", "green", "yellow", "blue", "magenta", "cyan", "white")

    for color in colors:
        sp.color, sp.text = color, color
        time.sleep(1)
```

### Advanced colors usage:

![adv-colors](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/advanced_colors.gif)

```python
# -*- coding: utf-8 -*-
import time
from yaspin import yaspin
from yaspin.spinners import Spinners
from yaspin.termcolor import colored

text = "Bold blink magenta spinner on cyan color"
# Support all termcolor features via simple closure
color_fn = lambda frame: colored(frame, "magenta", "on_cyan", attrs=["bold", "blink"])

with yaspin(Spinners.bouncingBall, text=text, color=color_fn):
    time.sleep(3)
```

### Run any spinner you want:

![custom](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/custom_spinners.gif)

```python
# -*- coding: utf-8 -*-
import time
from yaspin import yaspin, Spinner

# Compose new spinners with custom frame sequence and interval value
sp = Spinner(["😸", "😹", "😺", "😻", "😼", "😽", "😾", "😿", "🙀"], 200)

with yaspin(sp, text="Cat!"):
    time.sleep(3)  # cat consuming code :)
```

### Change spinner properties on the fly:

![properties](https://raw.githubusercontent.com/pavdmyt/yaspin/master/gifs/sp_properties.gif)

```python
# -*- coding: utf-8 -*-
import time
from yaspin import yaspin
from yaspin.spinners import Spinners

with yaspin(Spinners.noise, text="Noise spinner") as sp:
    time.sleep(2)

    sp.spinner = Spinners.arc  # spinner type
    sp.text = "Arc spinner"    # text along with spinner
    sp.color = "green"         # spinner color
    sp.right = True            # put spinner to the right
    sp.reverse = True          # reverse spin direction

    time.sleep(2)
```

More [examples](https://github.com/pavdmyt/yaspin/tree/master/examples).


## Development

Clone the repository:

```
git clone https://github.com/pavdmyt/yaspin.git
```

Install dev dependencies:

```
pip install -r requirements-dev.txt
```

Lint code:

```
make lint
```

Run tests:

```
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
* Contains [termcolor](https://pypi.python.org/pypi/termcolor) package: MIT License, Copyright (c) 2008-2011 Volvox Development Team
* Contains data from [cli-spinners](https://github.com/sindresorhus/cli-spinners): MIT License, Copyright (c) Sindre Sorhus sindresorhus@gmail.com (sindresorhus.com)


[travis-image]: https://travis-ci.org/pavdmyt/yaspin.svg?branch=master
[travis-url]: https://travis-ci.org/pavdmyt/yaspin

[cov-image]: https://coveralls.io/repos/github/pavdmyt/yaspin/badge.svg?branch=master
[cov-url]: https://coveralls.io/github/pavdmyt/yaspin?branch=master

[codacy-image]: https://api.codacy.com/project/badge/Grade/797c7772d0d3467c88a5e2e9dc79ec98
[codacy-url]: https://www.codacy.com/app/pavdmyt/yaspin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pavdmyt/yaspin&amp;utm_campaign=Badge_Grade

[examples-image]: https://img.shields.io/badge/learn%20by-examples-0077b3.svg
[examples-url]: https://github.com/pavdmyt/yaspin/tree/master/examples

[pypi-image]: https://img.shields.io/pypi/v/yaspin.svg
[pypi-url]: https://pypi.python.org/pypi/yaspin

[pyver-image]: https://img.shields.io/pypi/pyversions/yaspin.svg
[pyver-url]: https://pypi.python.org/pypi/yaspin
