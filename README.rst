**DataProperty**

.. image:: https://img.shields.io/pypi/pyversions/DataProperty.svg
   :target: https://pypi.python.org/pypi/DataProperty
.. image:: https://travis-ci.org/thombashi/DataProperty.svg?branch=master
    :target: https://travis-ci.org/thombashi/DataProperty
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

.. code:: python

    from dataproperty import PropertyExtractor, Typecode

    data_matrix = [
        [1, 1.1, "aaa", 1,   1],
        [2, 2.2, "bbb", 2.2, 2.2],
        [3, 3.3, "ccc", 3,   "ccc"],
    ]
    prop_matrix = PropertyExtractor.extract_data_property_matrix(data_matrix)

    print "---------- typename ----------"
    for prop_list in prop_matrix:
        print [Typecode.get_typename(prop.typecode) for prop in prop_list]

    print "---------- str_len ----------"
    for prop_list in prop_matrix:
        print [prop.str_len for prop in prop_list]

    print "---------- integer_digits ----------"
    for prop_list in prop_matrix:
        print [prop.integer_digits for prop in prop_list]

    print "---------- decimal_places ----------"
    for prop_list in prop_matrix:
        print [prop.decimal_places for prop in prop_list]

::

    ---------- typename ----------
    ['INT', 'FLOAT', 'STRING', 'INT', 'INT']
    ['INT', 'FLOAT', 'STRING', 'FLOAT', 'FLOAT']
    ['INT', 'FLOAT', 'STRING', 'INT', 'STRING']
    ---------- str_len ----------
    [1, 3, 3, 1, 1]
    [1, 3, 3, 3, 3]
    [1, 3, 3, 1, 3]
    ---------- integer_digits ----------
    [1, 1, nan, 1, 1]
    [1, 1, nan, 1, 1]
    [1, 1, nan, 1, nan]
    ---------- decimal_places ----------
    [0, 1, nan, 0, 0]
    [0, 1, nan, 1, 1]
    [0, 1, nan, 0, nan]

.. code:: python

    from dataproperty import PropertyExtractor, Typecode

    header_list = ["int", "float", "str", "num", "mix"]
    data_matrix = [
        [1, 1.1, "aaa", 1,   1],
        [2, 2.2, "bbb", 2.2, 2.2],
        [3, 3.3, "ccc", 3,   "ccc"],
    ]
    col_prop_list = PropertyExtractor.extract_column_property_list(header_list, data_matrix)

    print "---------- typename ----------"
    print [Typecode.get_typename(prop.typecode) for prop in col_prop_list]

    print "---------- padding_len ----------"
    print [prop.padding_len for prop in col_prop_list]

    print "---------- decimal_places ----------"
    print [prop.decimal_places for prop in col_prop_list]

::

    ---------- typename ----------
    ['INT', 'FLOAT', 'STRING', 'FLOAT', 'STRING']
    ---------- padding_len ----------
    [3, 5, 3, 3, 3]
    ---------- decimal_places ----------
    [nan, 1, nan, 1, 1]

Dependencies
============

Python 2.5+ or 3.3+

-  `six <https://pypi.python.org/pypi/six/>`__

Test dependencies
-----------------

-  `pytest <https://pypi.python.org/pypi/pytest>`__
-  `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
-  `tox <https://pypi.python.org/pypi/tox>`__
