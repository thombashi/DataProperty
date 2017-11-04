**DataProperty**

.. image:: https://badge.fury.io/py/DataProperty.svg
    :target: https://badge.fury.io/py/DataProperty

.. image:: https://img.shields.io/travis/thombashi/DataProperty/master.svg?label=Linux
    :target: https://travis-ci.org/thombashi/DataProperty

.. image:: https://img.shields.io/appveyor/ci/thombashi/dataproperty/master.svg?label=Windows
    :target: https://ci.appveyor.com/project/thombashi/dataproperty

.. image:: https://coveralls.io/repos/github/thombashi/DataProperty/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/DataProperty?branch=master

    
.. contents:: Table of contents
   :backlinks: top
   :local:


Summary
=======
A Python library for extract property from data.


Installation
============

::

    pip install DataProperty


Usage
=====

Extract property of data
------------------------

e.g. Extract a ``float`` value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from dataproperty import DataProperty
    >>> DataProperty(-1.1)
    data=-1.1, typename=REAL_NUMBER, align=right, ascii_char_width=4, integer_digits=1, decimal_places=1, additional_format_len=1


e.g. Extract a ``int`` value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from dataproperty import DataProperty
    >>> DataProperty(123456789)
    data=123456789, typename=INTEGER, align=right, ascii_char_width=9, integer_digits=9, decimal_places=0, additional_format_len=0

e.g. Extract a ``str`` (ascii) value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from dataproperty import DataProperty
    >>> DataProperty("sample string")
    data=sample string, typename=STRING, align=left, length=13, ascii_char_width=13, additional_format_len=0

e.g. Extract a ``str`` (multi-byte) value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> import six
    >>> from dataproperty import DataProperty
    >>> six.text_type(DataProperty("吾輩は猫である"))
    data=吾輩は猫である, typename=STRING, align=left, length=7, ascii_char_width=14, additional_format_len=0

::

e.g. Extract a time (``datetime``) value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> import datetime
    >>> from dataproperty import DataProperty
    >>> DataProperty(datetime.datetime(2017, 1, 1, 0, 0, 0))
    data=2017-01-01 00:00:00, typename=DATETIME, align=left, ascii_char_width=19, additional_format_len=0

e.g. Extract a ``bool`` value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from dataproperty import DataProperty
    >>> DataProperty(True)
    data=True, typename=BOOL, align=left, ascii_char_width=4, additional_format_len=0


Extract data property for each element from a matrix
----------------------------------------------------
``DataPropertyExtractor.to_dataproperty_matrix`` method returns a matrix of ``DataProperty`` instances from a data matrix. 
An example data set and the result are as follows:

.. code:: python

    dt = datetime.datetime(2017, 1, 1, 0, 0, 0)
    inf = float("inf")
    nan = float("nan")

    data_matrix = [
        [1, 1.1,  "aa",   1,   1,     True,   inf,   nan,   dt],
        [2, 2.2,  "bbb",  2.2, 2.2,   False,  "inf", "nan", dt],
        [3, 3.33, "cccc", -3,  "ccc", "true", inf,   "NAN", "2017-01-01T01:23:45+0900"],
    ]

::

    $ ./to_dataproperty_matrix.py
    ---------- typename ----------
    ['INTEGER', 'REAL_NUMBER', 'STRING', 'INTEGER', 'INTEGER', 'BOOL', 'INFINITY', 'NAN', 'DATETIME']
    ['INTEGER', 'REAL_NUMBER', 'STRING', 'REAL_NUMBER', 'REAL_NUMBER', 'BOOL', 'INFINITY', 'NAN', 'DATETIME']
    ['INTEGER', 'REAL_NUMBER', 'STRING', 'INTEGER', 'STRING', 'BOOL', 'INFINITY', 'NAN', 'STRING']

    ---------- data ----------
    [1, Decimal('1.1'), 'aa', 1, 1, True, Decimal('Infinity'), Decimal('NaN'), datetime.datetime(2017, 1, 1, 0, 0)]
    [2, Decimal('2.2'), 'bbb', Decimal('2.2'), Decimal('2.2'), False, Decimal('Infinity'), Decimal('NaN'), datetime.datetime(2017, 1, 1, 0, 0)]
    [3, Decimal('3.33'), 'cccc', -3, 'ccc', True, Decimal('Infinity'), Decimal('NaN'), '2017-01-01T01:23:45+0900']

    ---------- align ----------
    [right, right, left, right, right, left, left, left, left]
    [right, right, left, right, right, left, left, left, left]
    [right, right, left, right, left, left, left, left, left]

    ---------- length ----------
    [1, 3, 2, 1, 1, 4, 8, 3, 19]
    [1, 3, 3, 3, 3, 5, 8, 3, 19]
    [1, 4, 4, 2, 3, 4, 8, 3, 24]

    ---------- integer_digits ----------
    [1, 1, nan, 1, 1, nan, nan, nan, nan]
    [1, 1, nan, 1, 1, nan, nan, nan, nan]
    [1, 1, nan, 1, nan, nan, nan, nan, nan]

    ---------- decimal_places ----------
    [0, 1, nan, 0, 0, nan, nan, nan, nan]
    [0, 1, nan, 1, 1, nan, nan, nan, nan]
    [0, 2, nan, 0, nan, nan, nan, nan, nan]

Full example source code can be found at *examples/py/to_dataproperty_matrix.py*


Extract property for each column from a matrix
------------------------------------------------------
``DataPropertyExtractor.to_col_dataproperty_list`` method returns a list of ``DataProperty`` instances from a data matrix. The list represents the properties for each column.
An example data set and the result are as follows:

Example data set and result are as follows:

.. code:: python

    dt = datetime.datetime(2017, 1, 1, 0, 0, 0)
    inf = float("inf")
    nan = float("nan")

    data_matrix = [
        [1, 1.1,  "aa",   1,   1,     True,   inf,   nan,   dt],
        [2, 2.2,  "bbb",  2.2, 2.2,   False,  "inf", "nan", dt],
        [3, 3.33, "cccc", -3,  "ccc", "true", inf,   "NAN", "2017-01-01T01:23:45+0900"],
    ]

::

    $ ./to_col_dataproperty_list.py
    ---------- typename ----------
    ['INTEGER', 'REAL_NUMBER', 'STRING', 'REAL_NUMBER', 'STRING', 'BOOL', 'INFINITY', 'NAN', 'STRING']

    ---------- align ----------
    [right, right, left, right, left, left, left, left, left]

    ---------- ascii_char_width ----------
    [3, 5, 4, 4, 3, 5, 8, 3, 24]

    ---------- decimal_places ----------
    [0, 2, nan, 1, 1, nan, nan, nan, nan]


Full example source code can be found at *examples/py/to_col_dataproperty_list.py*


Dependencies
============
Python 2.7+ or 3.4+

- `logbook <http://logbook.readthedocs.io/en/stable/>`__
- `typepy <https://github.com/thombashi/typepy>`__

Test dependencies
-----------------
- `pytest <https://pypi.python.org/pypi/pytest>`__
- `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
- `tox <https://pypi.python.org/pypi/tox>`__
