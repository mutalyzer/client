Library
=======

The ``Mutalyzer`` class contains all relevant methods. A class instance is
created by providing a build name.

.. code:: python

    >>> from mutalyzer_client import Mutalyzer
    >>> 
    >>> mutalyzer = Mutalyzer('GRCh37')

The `hgvs_to_db` can be used to convert an HGVS_ description to a simple format
to be used in databases.

.. code:: python

    >>> mutalyzer.hgvs_to_db('NC_000001.10:g.12783G>A')
    ('chr1', '12783', 'G', 'A')

To work with VCF files, we recommend to use the PyVCF_ library.

.. code:: python

    >>> from vcf import Reader
    >>> 
    >>> reader = Reader(open('data/sample.vcf'))
    >>> record = next(reader)

To convert a VCF record to HGVS, use the ``vcf_to_hgvs`` method.

.. code:: python

    >>> mutalyzer.vcf_to_hgvs(record.CHROM, record.POS, record.REF, record.ALT[0])
    'NC_000001.10:g.12783G>A'

To convert a VCF record to database format, use the ``vcf_to_db`` method.

.. code:: python

    >>> mutalyzer.vcf_to_db(record.CHROM, record.POS, record.REF, record.ALT[0])
    ('chr1', '12783', 'G', 'A')


.. _HGVS: http://varnomen.hgvs.org/
.. _PyVCF: https://pyvcf.readthedocs.io/en/latest/index.html
