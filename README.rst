**DataProperty**

.. image:: https://badge.fury.io/py/DataProperty.svg
    :target: https://badge.fury.io/py/DataProperty

.. image:: https://img.shields.io/pypi/pyversions/DataProperty.svg
   :target: https://pypi.python.org/pypi/DataProperty

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
Python library for extract property from data.


Installation
============

::

    pip install DataProperty


Usage
=====

Extract property of data
------------------------

e.g. Extract `float` value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    print(DataProperty(-1.1))

::

    data=-1.1, typename=FLOAT, align=right, str_len=4, ascii_char_width=4, integer_digits=1, decimal_places=1, additional_format_len=1


e.g. Extract `int` value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    print(DataProperty(123456789))

::

    data=123456789, typename=INTEGER, align=right, str_len=9, ascii_char_width=9, integer_digits=9, decimal_places=0, additional_format_len=0

e.g. Extract `str` (ascii) value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    print(DataProperty("sample string"))

::

    data=sample string, typename=STRING, align=left, str_len=13, ascii_char_width=13, integer_digits=nan, decimal_places=nan, additional_format_len=0

e.g. Extract `str` (multi-byte) value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    print(DataProperty(u"吾輩は猫である"))
    
    data=吾輩は猫である, typename=STRING, align=left, str_len=7, ascii_char_width=14, integer_digits=nan, decimal_places=nan, additional_format_len=0

::

e.g. Extract time (`datetime`) value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import datetime
    from dataproperty import DataProperty
    print(DataProperty(datetime.datetime(2017, 1, 1, 0, 0, 0)))

::

    data=2017-01-01 00:00:00, typename=DATETIME, align=left, str_len=19, ascii_char_width=19, integer_digits=nan, decimal_places=nan, additional_format_len=0

e.g. Extract `bool` value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    print(DataProperty(True))

::

    data=True, typename=BOOL, align=left, str_len=4, ascii_char_width=4, integer_digits=nan, decimal_places=nan, additional_format_len=0


Extract for each data property from a matrix
----------------------------------------------------

.. code:: python

    import datetime
    from dataproperty import PropertyExtractor, Typecode

    def display_dataprop(prop_matrix, name):
        print()
        print("---------- {:s} ----------".format(name))
        for prop_list in prop_matrix:
            print([getattr(prop, name) for prop in prop_list])

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

    print("---------- typename ----------")
    for prop_list in prop_matrix:
        print([Typecode.get_typename(prop.typecode) for prop in prop_list])

    display_dataprop(prop_matrix, "data")
    display_dataprop(prop_matrix, "align")
    display_dataprop(prop_matrix, "str_len")
    display_dataprop(prop_matrix, "integer_digits")
    display_dataprop(prop_matrix, "decimal_places")

::

    ---------- typename ----------
    ['INTEGER', 'FLOAT', 'STRING', 'INTEGER', 'INTEGER', 'BOOL', 'INFINITY', 'NAN', 'DATETIME']
    ['INTEGER', 'FLOAT', 'STRING', 'FLOAT', 'FLOAT', 'BOOL', 'INFINITY', 'NAN', 'DATETIME']
    ['INTEGER', 'FLOAT', 'STRING', 'INTEGER', 'STRING', 'BOOL', 'INFINITY', 'NAN', 'STRING']
    
    ---------- data ----------
    [1, Decimal('1.1'), 'aa', 1, 1, True, Decimal('Infinity'), Decimal('NaN'), datetime.datetime(2017, 1, 1, 0, 0)]
    [2, Decimal('2.2'), 'bbb', Decimal('2.2'), Decimal('2.2'), False, Decimal('Infinity'), Decimal('NaN'), datetime.datetime(2017, 1, 1, 0, 0)]
    [3, Decimal('3.33'), 'cccc', -3, 'ccc', True, Decimal('Infinity'), Decimal('NaN'), '2017-01-01T01:23:45+0900']
    
    ---------- align ----------
    [right, right, left, right, right, left, left, left, left]
    [right, right, left, right, right, left, left, left, left]
    [right, right, left, right, left, left, left, left, left]
    
    ---------- str_len ----------
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


Extract for each column property from a matrix
------------------------------------------------------

.. code:: python

    import datetime
    from dataproperty import PropertyExtractor, Typecode

    def display_colprop(prop_list, name):
        print()
        print("---------- {:s} ----------".format(name))
        print([getattr(prop, name) for prop in prop_list])

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
    
    print("---------- typename ----------")
    print([Typecode.get_typename(prop.typecode) for prop in col_prop_list])

    display_colprop(col_prop_list, "align")
    display_colprop(col_prop_list, "padding_len")
    display_colprop(col_prop_list, "decimal_places")

::

    ---------- typename ----------
    ['INTEGER', 'FLOAT', 'STRING', 'FLOAT', 'STRING', 'BOOL', 'INFINITY', 'NAN', 'STRING']
    
    ---------- align ----------
    [right, right, left, right, left, left, left, left, left]
    
    ---------- padding_len ----------
    [3, 5, 4, 4, 3, 5, 8, 3, 24]
    
    ---------- decimal_places ----------
    [0, 2, nan, 1, 1, nan, nan, nan, nan]


Dependencies
============

Python 2.7+ or 3.3+

- `python-dateutil <https://dateutil.readthedocs.io/en/stable/>`__
- `pytz <https://pypi.python.org/pypi/pytz/>`__
- `six <https://pypi.python.org/pypi/six/>`__

Test dependencies
-----------------

-  `pytest <https://pypi.python.org/pypi/pytest>`__
-  `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
-  `tox <https://pypi.python.org/pypi/tox>`__
