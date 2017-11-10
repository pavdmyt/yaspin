#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
yaspin
~~~~~~

A lightweight and easy to use terminal spinner.
No external dependencies.

:copyright: (c) 2017 Pavlo Dmytrenko
:license: MIT
"""

import codecs
import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


# Package meta-data
NAME = 'yaspin'
LICENSE = 'MIT'
DESCRIPTION = 'Yet Another terminal Spinner'
LONG_DESCR = ('Lightweight and easy to use terminal spinner. '
              'No external dependencies. '
              'Find documentation here: https://github.com/pavdmyt/yaspin')
URL = 'https://github.com/pavdmyt/yaspin'
EMAIL = 'mail@pavdmyt.com'
AUTHOR = 'Pavlo Dmytrenko'


def read_version(package):
    version_path = os.path.join(package, '__version__.py')
    with open(version_path, 'r') as fd:
        for line in fd:
            if line.startswith('__version__ = '):
                return line.split()[-1].strip().strip("'")


version = read_version(NAME)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests/']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


with codecs.open('HISTORY.md', encoding='utf-8') as fd:
    history = fd.read()


tests_require = [
    "pytest",
]


setup(
    name=NAME,
    version=version,
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCR + "\n\n" + history,
    url=URL,
    packages=find_packages(exclude=('tests', 'docs', 'examples')),
    include_package_data=True,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
