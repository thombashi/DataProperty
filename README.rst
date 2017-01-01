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

e.g. Extract a ``float`` value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    print(DataProperty(-1.1))

::

    data=-1.1, typename=FLOAT, align=right, str_len=4, ascii_char_width=4, integer_digits=1, decimal_places=1, additional_format_len=1


e.g. Extract a ``int`` value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    print(DataProperty(123456789))

::

    data=123456789, typename=INTEGER, align=right, str_len=9, ascii_char_width=9, integer_digits=9, decimal_places=0, additional_format_len=0

e.g. Extract a ``str`` (ascii) value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    print(DataProperty("sample string"))

::

    data=sample string, typename=STRING, align=left, str_len=13, ascii_char_width=13, integer_digits=nan, decimal_places=nan, additional_format_len=0

e.g. Extract a ``str`` (multi-byte) value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    print(six.text_type(DataProperty(u"吾輩は猫である")))
    
    data=吾輩は猫である, typename=STRING, align=left, str_len=7, ascii_char_width=14, integer_digits=nan, decimal_places=nan, additional_format_len=0

::

e.g. Extract a time (``datetime``) value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import datetime
    from dataproperty import DataProperty
    print(DataProperty(datetime.datetime(2017, 1, 1, 0, 0, 0)))

::

    data=2017-01-01 00:00:00, typename=DATETIME, align=left, str_len=19, ascii_char_width=19, integer_digits=nan, decimal_places=nan, additional_format_len=0

e.g. Extract a ``bool`` value property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    print(DataProperty(True))

::

    data=True, typename=BOOL, align=left, str_len=4, ascii_char_width=4, integer_digits=nan, decimal_places=nan, additional_format_len=0


Extract data property for each element from a matrix
----------------------------------------------------

.. code:: python

    import datetime
    from dataproperty import DataPropertyExtractor, Typecode

    def display_dp_matrix_attr(dp_matrix, attr_name):
        """show a value assocciated with an attribute for each DataProperty instance in the dp_matrix"""

        print()
        print("---------- {:s} ----------".format(attr_name))
        for dp_list in dp_matrix:
            print([getattr(dp, attr_name) for dp in dp_list])

    # sample data definitions
    dt = datetime.datetime(2017, 1, 1, 0, 0, 0)
    inf = float("inf")
    nan = float("nan")
    data_matrix = [
        [1, 1.1,  "aa",   1,   1,     True,   inf,   nan,   dt],
        [2, 2.2,  "bbb",  2.2, 2.2,   False,  "inf", "nan", dt],
        [3, 3.33, "cccc", -3,  "ccc", "true", inf,   "NAN", "2017-01-01T01:23:45+0900"],
    ]

    # extract data property for each element from a matrix
    dp_extractor = DataPropertyExtractor()
    dp_extractor.data_matrix = data_matrix
    dp_matrix = dp_extractor.to_dataproperty_matrix()

    print("---------- typename ----------")
    for dp_list in dp_matrix:
        print([Typecode.get_typename(dp.typecode) for dp in dp_list])

    display_dp_matrix_attr(dp_matrix, "data")
    display_dp_matrix_attr(dp_matrix, "align")
    display_dp_matrix_attr(dp_matrix, "str_len")
    display_dp_matrix_attr(dp_matrix, "integer_digits")
    display_dp_matrix_attr(dp_matrix, "decimal_places")

::

    ---------- typename ----------
    [u'INTEGER', u'FLOAT', u'STRING', u'INTEGER', u'INTEGER', u'BOOL', u'INFINITY', u'NAN', u'DATETIME']
    [u'INTEGER', u'FLOAT', u'STRING', u'FLOAT', u'FLOAT', u'BOOL', u'INFINITY', u'NAN', u'DATETIME']
    [u'INTEGER', u'FLOAT', u'STRING', u'INTEGER', u'STRING', u'BOOL', u'INFINITY', u'NAN', u'STRING']

    ---------- data ----------
    [1, Decimal('1.1'), u'aa', 1, 1, True, Decimal('Infinity'), Decimal('NaN'), datetime.datetime(2017, 1, 1, 0, 0)]
    [2, Decimal('2.2'), u'bbb', Decimal('2.2'), Decimal('2.2'), False, Decimal('Infinity'), Decimal('NaN'), datetime.datetime(2017, 1, 1, 0, 0)]
    [3, Decimal('3.33'), u'cccc', -3, u'ccc', True, Decimal('Infinity'), Decimal('NaN'), u'2017-01-01T01:23:45+0900']

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


Extract property for each column from a matrix
------------------------------------------------------

.. code:: python

    import datetime
    from dataproperty import DataPropertyExtractor, Typecode

    def display_col_dp(dp_list, attr_name):
        """show a value assocciated with an attribute for each DataProperty instance in the dp_list"""

        print()
        print("---------- {:s} ----------".format(attr_name))
        print([getattr(dp, attr_name) for dp in dp_list])

    # sample data definitions
    dt = datetime.datetime(2017, 1, 1, 0, 0, 0)
    inf = float("inf")
    nan = float("nan")
    data_matrix = [
        [1, 1.1,  "aa",   1,   1,     True,   inf,   nan,   dt],
        [2, 2.2,  "bbb",  2.2, 2.2,   False,  "inf", "nan", dt],
        [3, 3.33, "cccc", -3,  "ccc", "true", inf,   "NAN", "2017-01-01T01:23:45+0900"],
    ]

    # extract property for each column from a matrix
    dp_extractor = DataPropertyExtractor()
    dp_extractor.header_list = [
        "int", "float", "str", "num", "mix", "bool", "inf", "nan", "time"]
    dp_extractor.data_matrix = data_matrix
    col_dp_list = dp_extractor.to_col_dataproperty_list()

    print("---------- typename ----------")
    print([Typecode.get_typename(dp.typecode) for dp in col_dp_list])

    display_col_dp(col_dp_list, "align")
    display_col_dp(col_dp_list, "ascii_char_width")
    display_col_dp(col_dp_list, "decimal_places")

::

    ---------- typename ----------
    [u'INTEGER', u'FLOAT', u'STRING', u'FLOAT', u'STRING', u'BOOL', u'INFINITY', u'NAN', u'STRING']

    ---------- align ----------
    [right, right, left, right, left, left, left, left, left]

    ---------- ascii_char_width ----------
    [3, 5, 4, 4, 3, 5, 8, 3, 24]

    ---------- decimal_places ----------
    [0, 2, nan, 1, 1, nan, nan, nan, nan]


Dependencies
============

Python 2.7+ or 3.3+

- `mbstrdecoder <https://github.com/thombashi/mbstrdecoder>`__
- `python-dateutil <https://dateutil.readthedocs.io/en/stable/>`__
- `pytz <https://pypi.python.org/pypi/pytz/>`__
- `six <https://pypi.python.org/pypi/six/>`__

Test dependencies
-----------------

-  `pytest <https://pypi.python.org/pypi/pytest>`__
-  `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
-  `tox <https://pypi.python.org/pypi/tox>`__
