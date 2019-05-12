Release History
===============

0.14.3 / 2019-05-12
-------------------

* fix(#29): race condition between spinner thread and ``write()``


0.14.2 / 2019-04-27
-------------------

* fix: remove extra ``\b`` written to stdout. Fixes ``write()`` in rxvt terminal


0.14.1 / 2019-01-28
-------------------

* fix(#26): traceback on PYTHONOPTIMIZE=2


0.14.0 / 2018-09-05
-------------------

* Support for handling POSIX signals
* New function in public API: ``kbi_safe_yaspin``


0.13.0 / 2018-08-14
-------------------

* API improvements: ``spinner``, ``color``, ``on_color``, ``attrs`` and ``side`` argument values are handled via ``__getattr__``
* New ``yaspin`` arguments: ``on_color``, ``attrs``
* ``right=False`` argument replaced with ``side="left"``
* ``Yaspin.right`` replaced with ``Yaspin.side``
* ``reverse`` argument replaced with ``reversal``
* ``Yaspin.reverse`` replaced with ``Yaspin.reversal``
* Remove default text stripping in ``Yaspin._freeze``


0.12.0 / 2018-07-16
-------------------

* Add support for Python 3.7
* Drop support for Python 2.6 and 3.3

* dev: Migrate to Pipfile
* dev: Speedup local unittests with pytest-xdist


0.11.1 / 2018-07-10
-------------------

* fix(#16): remove default text stripping in ``Yaspin.write`` to allow printing of the hierarchical text


0.11.0 / 2018-06-23
-------------------

* Update cli-spinners to v1.3.1


0.10.0 / 2018-03-23
-------------------

* New ``hide`` and ``show`` methods to toggle the display of the spinner


0.9.0 / 2018-02-26
------------------

* New ``write`` method for writing text into terminal without breaking the spinner


0.8.0 / 2017-12-31
------------------

* Speedup reading spinners collection with simplejson


0.7.1 / 2017-12-02
------------------

* fix(#7): handling bytes sequences in ``Spinner.frames``


0.7.0 / 2017-11-28
------------------

* Reverse spinner support


0.6.0 / 2017-11-26
------------------

* Right spinner support


0.5.0 / 2017-11-24
------------------

* Colors support


0.4.2 / 2017-11-17
------------------

* RST vs PyPI episode 2


0.4.1 / 2017-11-17
------------------

* RST vs PyPI episode 1


0.4.0 / 2017-11-17
------------------

* Support for success and failure finalizers


0.3.0 / 2017-11-14
------------------

* Support for changing spinner properties on the fly


0.2.0 / 2017-11-10
------------------

* Support all spinners from `cli-spinners`_
* API changes:
    - ``yaspin.spinner`` -> ``yaspin.yaspin``


0.1.0 / 2017-10-31
------------------

* First version


.. _cli-spinners: https://github.com/sindresorhus/cli-spinners
