yaspin
======

**Y**et **A**nother Terminal Spinner for Python.

**Yaspin** provides a lightweight and configurable spinner to show some progress during long-hanging operations. It is easy to integrate into existing codebase by using it as a *context manager* or as a function *decorator*.

*Lightweight* means that **yaspin** does not have any external dependencies.

![yaspin](https://raw.githubusercontent.com/pavdmyt/yaspin/master/demo.gif)

Convert any character sequence you like in a spinner!


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

```python
import time
from yaspin import spinner


# Use as a context manager
with spinner():
    time_consuming_code()


# Context manager with text
with spinner(text="Processing..."):
    time_consuming_code()


# Context manager with custom sequence
with spinner(sequence='.oOo. ', interval=0.14):
    time_consuming_code()


# As decorator
@spinner(text="Загрузка...")
def some_operations():
    time.sleep(3)
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

MIT - Pavlo Dmytrenko
