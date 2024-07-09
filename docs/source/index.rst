.. python-isodata documentation master file, created by
   sphinx-quickstart on Tue Feb  4 20:05:16 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to python-isodata's documentation!
==========================================
A Python library to retrieve energy market information from the major US ISOs.

Source: https://github.com/CaffeineLab/isodata


Installation
------------

.. code-block:: bash

   pip install python-isodata


Usage
-----

.. code-block:: python

   >>> from isodata.sessions import Session
   >>> pjm = Session('pjm')
   >>> pjm.authorize((username, password, (cert, key))
   >>> report = pjm.query(report='QueryPortfolios')

Energy Trading Tools
--------------------
`Caffeine Lab <https://caffeinelab.com/>`_ will publish more tools for energy traders at:

https://caffeinelab.com/mining-energy-data.html

.. toctree::
   :maxdepth: 2
   :caption: Contents:
.. autosummary::
   :toctree: generated



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`