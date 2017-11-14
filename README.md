# yaspin [![travis][travis-image]][travis-url] [![cov][cov-image]][cov-url] [![pypi][pypi-image]][pypi-url] [![pyver][pyver-image]][pyver-url]

**Y**et **A**nother Terminal Spinner for Python.

**Yaspin** provides a lightweight and configurable spinner to show some progress during long-hanging operations. It is easy to integrate into existing codebase by using it as a *context manager* or as a function *decorator*.

*Lightweight* means that **yaspin** does not have any external dependencies.

![yaspin](https://raw.githubusercontent.com/pavdmyt/yaspin/master/demo.gif)

Convert any character sequence you like in a spinner!


## Features

* Supports all (60+) spinners from [cli-spinners](https://github.com/sindresorhus/cli-spinners)
* Runs at all major CPython versions (_2.6_, _2.7_, _3.3_, _3.4_, _3.5_, _3.6_), PyPy and PyPy3
* No external dependencies
* Flexible API, easy to integrate with existing code


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

    sp.spinner = Spinners.arc
    sp.text = "Arc spinner"

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
* Contains data from [cli-spinners](https://github.com/sindresorhus/cli-spinners): MIT License, Copyright (C) Sindre Sorhus sindresorhus@gmail.com (sindresorhus.com)


[travis-image]: https://travis-ci.org/pavdmyt/yaspin.svg?branch=master
[travis-url]: https://travis-ci.org/pavdmyt/yaspin

[cov-image]: https://coveralls.io/repos/github/pavdmyt/yaspin/badge.svg?branch=master
[cov-url]: https://coveralls.io/github/pavdmyt/yaspin?branch=master

[pypi-image]: https://img.shields.io/pypi/v/yaspin.svg
[pypi-url]: https://pypi.python.org/pypi/yaspin

[pyver-image]: https://img.shields.io/pypi/pyversions/yaspin.svg
[pyver-url]: https://pypi.python.org/pypi/yaspin
