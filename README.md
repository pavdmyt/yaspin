# yaspin [![travis][travis-image]][travis-url] [![cov][cov-image]][cov-url] [![pypi][pypi-image]][pypi-url] [![pyver][pyver-image]][pyver-url]

**Y**et **A**nother Terminal **Spin**ner for Python.

**Yaspin** provides a lightweight and configurable spinner to show some progress during long-hanging operations. It is easy to integrate into existing codebase by using it as a *context manager* or as a function *decorator*.

*Lightweight* means that **yaspin** does not have any external dependencies.

![yaspin](https://raw.githubusercontent.com/pavdmyt/yaspin/master/demo.gif)

Convert any character sequence you like in a spinner!


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

Context manager:

```python
import time
from yaspin import yaspin

with yaspin():
    # time consuming code
    time.sleep(3)

# Context manager with text
with yaspin(text="Processing..."):
    # time consuming code
    time.sleep(3)
```

Function decorator:

```python
import time
from yaspin import yaspin

@yaspin(text="Loading...")
def some_operations():
    # time consuming code
    time.sleep(3)

some_operations()
```

It is also possible to control spinner manually:

```python
import time
from yaspin import yaspin

spinner = yaspin()
spinner.start()

# time consuming tasks
time.sleep(3)

spinner.stop()
```

Run any spinner from [cli-spinners](https://github.com/sindresorhus/cli-spinners):

```python
import time
from yaspin import yaspin
from yaspin.spinners import Spinners

with yaspin(Spinners.earth):
    # time consuming code
    time.sleep(3)
```

Any Colour You Like [🌈](https://en.wikipedia.org/wiki/Any_Colour_You_Like)

```python
import time
from yaspin import yaspin

with yaspin(text="Colors!") as sp:
    colors = ("red", "green", "yellow", "blue", "magenta", "cyan", "white")
    for color in colors:
        sp.color = color
        sp.text = color
        time.sleep(2)
```

```python
import time
from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners

text = "Bold blink magenta spinner on cyan color"
color_fn = lambda frame: colored(frame, "magenta", "on_cyan", attrs=["bold", "blink"])

with yaspin(Spinners.bouncingBall, text=text, color=color_fn):
    time.sleep(3)
```

Run any spinner you want:

```python
import time
from yaspin import yaspin, Spinner

sp = Spinner(["😸", "😹", "😺", "😻", "😼", "😽", "😾", "😿", "🙀"], 200)
with yaspin(sp, text="Cat!"):
    # cat consuming code :)
    time.sleep(5)
```

Change spinner properties on the fly:

```python
import time
from yaspin import yaspin
from yaspin.spinners import Spinners

with yaspin(Spinners.noise, text="Noise spinner") as sp:
    time.sleep(2)

    sp.spinner = Spinners.arc  # spinner type
    sp.text = "Arc spinner"    # text along with spinner
    sp.color = "magenta"       # spinner color
    sp.right = True            # put spinner to the right
    sp.reverse = True          # reverse spin direction

    time.sleep(2)
```

Success and Failure finalizers:

```python
import time
from random import randint
from yaspin import yaspin

with yaspin(text="ℙƴ☂ℌøἤ") as sp:
    time.sleep(2)
    success = randint(0, 1)

    if success:
        # can also be called with arguments: sp.ok("✅")
        sp.ok()
    else:
        # can also be called with arguments: sp.fail("💥")
        sp.fail()
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

[pypi-image]: https://img.shields.io/pypi/v/yaspin.svg
[pypi-url]: https://pypi.python.org/pypi/yaspin

[pyver-image]: https://img.shields.io/pypi/pyversions/yaspin.svg
[pyver-url]: https://pypi.python.org/pypi/yaspin
