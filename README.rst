**DataProperty**

.. image:: https://img.shields.io/pypi/pyversions/DataProperty.svg
   :target: https://pypi.python.org/pypi/DataProperty
.. image:: https://travis-ci.org/thombashi/DataProperty.svg?branch=master
    :target: https://travis-ci.org/thombashi/DataProperty
.. image:: https://ci.appveyor.com/api/projects/status/6ybxtfnle9lhykr9?svg=true
    :target: https://ci.appveyor.com/project/thombashi/dataproperty
.. image:: https://coveralls.io/repos/github/thombashi/DataProperty/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/DataProperty?branch=master

.. contents:: Table of contents
   :backlinks: top
   :local:

Summary
=======
Python library for extract property from data.

Installation
============

::

    pip install DataProperty

Usage
=====

Extract property of data
------------------------

e.g. Extract property of a `float` value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    DataProperty(-1.0)

::

    data=-1.0, typename=FLOAT, align=right, str_len=4, integer_digits=1, decimal_places=1, additional_format_len=1

e.g. Extract property of a `int` value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    DataProperty(123456789)

::

    data=123456789, typename=INT, align=right, str_len=9, integer_digits=9, decimal_places=0, additional_format_len=0

e.g. Extract property of a `str` value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    DataProperty("abcdefgh")

::

    data=abcdefgh, typename=STRING, align=left, str_len=8, integer_digits=nan, decimal_places=nan, additional_format_len=0

e.g. Extract property of a time value (from `datetime`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import datetime
    from dataproperty import DataProperty
    DataProperty(datetime.datetime(2017, 1, 1, 0, 0, 0))

::

    data=2017-01-01 00:00:00, typename=DATETIME, align=left, str_len=19, integer_digits=nan, decimal_places=nan, additional_format_len=0

e.g. Extract property of a time value (from `str`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    DataProperty("2017-01-01T01:23:45+0900")

::

    data=2017-01-01 01:23:45+09:00, typename=DATETIME, align=left, str_len=25, integer_digits=nan, decimal_places=nan, additional_format_len=0


e.g. Extract property of a `bool` value.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    DataProperty(True)

::

    data=True, typename=BOOL, align=left, str_len=4, integer_digits=nan, decimal_places=nan, additional_format_len=0


Extract property of data for each data from a matrix
----------------------------------------------------

.. code:: python

    import datetime
    from dataproperty import PropertyExtractor, Typecode
    import six

    def display(prop_matrix, name):
        six.print_()
        six.print_("---------- %s ----------" % (name))
        for prop_list in prop_matrix:
            six.print_([getattr(prop, name) for prop in prop_list])

    dt = datetime.datetime(2017, 1, 1, 0, 0, 0)
    inf = float("inf")
    nan = float("nan")
    data_matrix = [
        [1, 1.1,  "aa",   1,   1,     True,   inf,   nan,   dt],
        [2, 2.2,  "bbb",  2.2, 2.2,   False,  "inf", "nan", dt],
        [3, 3.33, "cccc", -3,  "ccc", "true", inf,   "NAN", "2017-01-01T01:23:45+0900"],
    ]
    prop_extractor = PropertyExtractor()

    prop_extractor.data_matrix = data_matrix
    prop_matrix = prop_extractor.extract_data_property_matrix()

    six.print_("---------- typename ----------")
    for prop_list in prop_matrix:
        six.print_([Typecode.get_typename(prop.typecode) for prop in prop_list])

    display(prop_matrix, "data")
    display(prop_matrix, "align")
    display(prop_matrix, "str_len")
    display(prop_matrix, "integer_digits")
    display(prop_matrix, "decimal_places")

::

    ---------- typename ----------
    ['INT', 'FLOAT', 'STRING', 'INT', 'INT', 'BOOL', 'INFINITY', 'NAN', 'DATETIME']
    ['INT', 'FLOAT', 'STRING', 'FLOAT', 'FLOAT', 'BOOL', 'INFINITY', 'NAN', 'DATETIME']
    ['INT', 'FLOAT', 'STRING', 'INT', 'STRING', 'BOOL', 'INFINITY', 'NAN', 'DATETIME']

    ---------- data ----------
    [1, 1.1, 'aa', 1, 1, True, inf, nan, datetime.datetime(2017, 1, 1, 0, 0)]
    [2, 2.2, 'bbb', 2.2, 2.2, False, inf, nan, datetime.datetime(2017, 1, 1, 0, 0)]
    [3, 3.33, 'cccc', -3, 'ccc', True, inf, nan, datetime.datetime(2017, 1, 1, 1, 23, 45, tzinfo=tzoffset(None, 32400))]

    ---------- align ----------
    [right, right, left, right, right, left, left, left, left]
    [right, right, left, right, right, left, left, left, left]
    [right, right, left, right, left, left, left, left, left]

    ---------- str_len ----------
    [1, 3, 2, 1, 1, 4, 3, 3, 19]
    [1, 3, 3, 3, 3, 5, 3, 3, 19]
    [1, 4, 4, 2, 3, 4, 3, 3, 24]

    ---------- integer_digits ----------
    [1, 1, nan, 1, 1, nan, nan, nan, nan]
    [1, 1, nan, 1, 1, nan, nan, nan, nan]
    [1, 1, nan, 1, nan, nan, nan, nan, nan]

    ---------- decimal_places ----------
    [0, 1, nan, 0, 0, nan, nan, nan, nan]
    [0, 1, nan, 1, 1, nan, nan, nan, nan]
    [0, 2, nan, 0, nan, nan, nan, nan, nan]

Extract property of data for each column from a matrix
------------------------------------------------------

.. code:: python

    import datetime
    from dataproperty import PropertyExtractor, Typecode
    import six

    def display(prop_list, name):
        six.print_()
        six.print_("---------- %s ----------" % (name))
        six.print_([getattr(prop, name) for prop in prop_list])

    dt = datetime.datetime(2017, 1, 1, 0, 0, 0)
    inf = float("inf")
    nan = float("nan")
    data_matrix = [
        [1, 1.1,  "aa",   1,   1,     True,   inf,   nan,   dt],
        [2, 2.2,  "bbb",  2.2, 2.2,   False,  "inf", "nan", dt],
        [3, 3.33, "cccc", -3,  "ccc", "true", inf,   "NAN", "2017-01-01T01:23:45+0900"],
    ]
    prop_extractor = PropertyExtractor()

    prop_extractor.header_list = [
        "int", "float", "str", "num", "mix", "bool", "inf", "nan", "time"]
    prop_extractor.data_matrix = data_matrix
    col_prop_list = prop_extractor.extract_column_property_list()

    six.print_("---------- typename ----------")
    six.print_([Typecode.get_typename(prop.typecode) for prop in col_prop_list])

    display(col_prop_list, "align")
    display(col_prop_list, "padding_len")
    display(col_prop_list, "decimal_places")

::

    ---------- typename ----------
    ['INT', 'FLOAT', 'STRING', 'FLOAT', 'STRING', 'BOOL', 'INFINITY', 'NAN', 'DATETIME']

    ---------- align ----------
    [right, right, left, right, left, left, left, left, left]

    ---------- padding_len ----------
    [3, 5, 4, 4, 3, 5, 3, 3, 24]

    ---------- decimal_places ----------
    [0, 2, nan, 1, 1, nan, nan, nan, nan]


Dependencies
============

Python 2.6+ or 3.3+

- `python-dateutil <https://dateutil.readthedocs.io/en/stable/>`__
- `pytz <https://pypi.python.org/pypi/pytz/>`__
- `six <https://pypi.python.org/pypi/six/>`__

Test dependencies
-----------------

-  `pytest <https://pypi.python.org/pypi/pytest>`__
-  `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
-  `tox <https://pypi.python.org/pypi/tox>`__
