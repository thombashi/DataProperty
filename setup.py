# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import io
import os.path
import sys

import setuptools


MISC_DIR = "misc"
REQUIREMENT_DIR = "requirements"

with io.open("README.rst", encoding="utf8") as f:
    long_description = f.read()

with io.open(os.path.join(MISC_DIR, "summary.txt"), encoding="utf8") as f:
    summary = f.read()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "docs_requirements.txt")) as f:
    docs_requires = [line.strip() for line in f if line.strip()]

needs_pytest = set(["pytest", "test", "ptr"]).intersection(sys.argv)
pytest_runner_require = ["pytest-runner"] if needs_pytest else []
setuptools_require = ["setuptools>=20.2.2"]

MODULE_NAME = "DataProperty"
AUTHOR = "Tsuyoshi Hombashi"
EMAIL = "tsuyoshi.hombashi@gmail.com"

setuptools.setup(
    name=MODULE_NAME,
    version="0.27.0",
    url="https://github.com/thombashi/{}".format(MODULE_NAME),

    author=AUTHOR,
    author_email=EMAIL,
    description=summary,
    include_package_data=True,
    keywords=["data", "property"],
    license="MIT License",
    long_description=long_description,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    packages=setuptools.find_packages(exclude=["test*"]),

    install_requires=setuptools_require + install_requires,
    setup_requires=setuptools_require + pytest_runner_require,
    tests_require=tests_requires,
    extras_require={
        "test": tests_requires,
        "docs": docs_requires,
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
