#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
yaspin
~~~~~~

A lightweight and easy to use terminal spinner.
No external dependencies.

:copyright: (c) 2018 Pavlo Dmytrenko
:license: MIT
"""

import codecs
import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


# Package meta-data
NAME = "yaspin"
LICENSE = "MIT"
DESCRIPTION = "Yet Another Terminal Spinner"
URL = "https://github.com/pavdmyt/yaspin"
EMAIL = "mail@pavdmyt.com"
AUTHOR = "Pavlo Dmytrenko"


def read_version(package):
    version_path = os.path.join(package, "__version__.py")
    with open(version_path, "r") as fd:
        for line in fd:
            if line.startswith("__version__ = "):
                return line.split()[-1].strip().strip('"')


version = read_version(NAME)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["tests/"]
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)


with codecs.open("README.rst", encoding="utf-8") as fd:
    readme = fd.read()


tests_require = ["pytest"]


setup(
    name=NAME,
    version=version,
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=readme,
    url=URL,
    download_url="https://github.com/pavdmyt/yaspin/archive/master.zip",
    packages=find_packages(exclude=("tests", "docs", "examples")),
    include_package_data=True,
    tests_require=tests_require,
    cmdclass={"test": PyTest},
    keywords="progressmeter progress meter rate console terminal console cli"
    " loading loader indicator spinner spinners time busy wait idle",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Other Audience",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Shells",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
)
