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

e.g. float
~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    DataProperty(-1.0)

::

    data=-1.0, typename=FLOAT, align=right, str_len=4, integer_digits=1, decimal_places=1, additional_format_len=1

e.g. int
~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    DataProperty(123456789)

::

    data=123456789, typename=INT, align=right, str_len=9, integer_digits=9, decimal_places=0, additional_format_len=0

e.g. string
~~~~~~~~~~~

.. code:: python

    from dataproperty import DataProperty
    DataProperty("abcdefgh")

::

    data=abcdefgh, typename=STRING, align=left, str_len=8, integer_digits=nan, decimal_places=nan, additional_format_len=0

Extract property of data for each data from a matrix
----------------------------------------------------

.. code:: python

    from dataproperty import PropertyExtractor, Typecode
    import six

    data_matrix = [
        [1, 1.1, "aa",  1,   1],
        [2, 2.2, "bbb", 2.2, 2.2],
        [3, 3.33, "cccc", -3, "ccc"],
    ]
    prop_extractor = PropertyExtractor()

    def display(prop_matrix, name):
        six.print_()
        six.print_("---------- %s ----------" % (name))
        for prop_list in prop_matrix:
            six.print_([getattr(prop, name) for prop in prop_list])

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
    ['INT', 'FLOAT', 'STRING', 'INT', 'INT']
    ['INT', 'FLOAT', 'STRING', 'FLOAT', 'FLOAT']
    ['INT', 'FLOAT', 'STRING', 'INT', 'STRING']

    ---------- data ----------
    [1, 1.1, 'aa', 1, 1]
    [2, 2.2, 'bbb', 2.2, 2.2]
    [3, 3.33, 'cccc', -3, 'ccc']

    ---------- align ----------
    [right, right, left, right, right]
    [right, right, left, right, right]
    [right, right, left, right, left]

    ---------- str_len ----------
    [1, 3, 2, 1, 1]
    [1, 3, 3, 3, 3]
    [1, 4, 4, 2, 3]

    ---------- integer_digits ----------
    [1, 1, nan, 1, 1]
    [1, 1, nan, 1, 1]
    [1, 1, nan, 1, nan]

    ---------- decimal_places ----------
    [0, 1, nan, 0, 0]
    [0, 1, nan, 1, 1]
    [0, 2, nan, 0, nan]

Extract property of data for each column from a matrix
------------------------------------------------------

.. code:: python

    from dataproperty import PropertyExtractor, Typecode
    import six

    data_matrix = [
        [1, 1.1, "aa",  1,   1],
        [2, 2.2, "bbb", 2.2, 2.2],
        [3, 3.33, "cccc", -3, "ccc"],
    ]
    prop_extractor = PropertyExtractor()

    def display(prop_list, name):
        six.print_()
        six.print_("---------- %s ----------" % (name))
        six.print_([getattr(prop, name) for prop in prop_list])

    prop_extractor.header_list = ["int", "float", "str", "num", "mix"]
    prop_extractor.data_matrix = data_matrix
    col_prop_list = prop_extractor.extract_column_property_list()

    six.print_("---------- typename ----------")
    six.print_([Typecode.get_typename(prop.typecode) for prop in col_prop_list])

    display(col_prop_list, "align")
    display(col_prop_list, "padding_len")
    display(col_prop_list, "decimal_places")

::

    ---------- typename ----------
    ['INT', 'FLOAT', 'STRING', 'FLOAT', 'STRING']

    ---------- align ----------
    [right, right, left, right, left]

    ---------- padding_len ----------
    [3, 5, 4, 3, 3]

    ---------- decimal_places ----------
    [nan, 2, nan, 1, 1]

Dependencies
============

Python 2.6+ or 3.3+

-  `six <https://pypi.python.org/pypi/six/>`__

Test dependencies
-----------------

-  `pytest <https://pypi.python.org/pypi/pytest>`__
-  `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
-  `tox <https://pypi.python.org/pypi/tox>`__
