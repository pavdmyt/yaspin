Features
========

- No external dependencies
- Runs at all major **CPython** versions (*2.6*, *2.7*, *3.3*, *3.4*, *3.5*, *3.6*), **PyPy** and **PyPy3**
- Supports all (60+) spinners from `cli-spinners`_
- Supports all *colors*, *highlights*, *attributes* and their mixes from `termcolor`_ library
- Flexible API, easy to integrate with existing code
- Safe **pipes** and **redirects**:

.. code-block:: bash

    $ python script_that_uses_yaspin.py > script.log
    $ python script_that_uses_yaspin.py | grep ERROR
