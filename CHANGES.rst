CHANGES
*******

4.0 (2023-07-12)
================

- Add support for Python 3.7, 3.8, 3.9, 3.10, 3.11.

- Drop support for Python 2.7, 3.4, 3.5, 3.6.

- Fix tests to be able to run with ``zope.component >= 5``.


3.0.1 (2018-01-12)
==================

- Rearrange tests such that Travis CI can pick up all functional tests too.

3.0.0 (2018-01-05)
==================

- Python 3 compatibility.

2.3 (2017-08-11)
================

- Introduce IntId index that is more optimized to index values by their int ids.

2.2.1 (2016-01-29)
==================

- Update tests.

2.2 (2015-11-20)
================

- Introduce Datetime index that's more optimized for index datetime objects.
  Please note the index uses seconds-resolution (the integer timestamp
  representing the datetime's value).

2.1 (2015-06-11)
================

- Make possible to install a catalog in a site on a different event
  than ``IObjectAddedEvent`` using the ``grokcore.site.install_on``
  directive.

2.0 (2013-05-07)
================

- Rename IIndexDefinition and IndexDefinition into IAttributeIndexDefinition
  and AtributeIndexDefinition respectively. This is used for the current
  index "classes" and allow for setup() magic for attribute indexes when
  creating new catalogs.

  This allows for IIndexDefinition and IndexDefinition to be used for
  simpler catalog index definitions where no Grok magic is applied when
  creating catalogs.

1.0 (2012-05-01)
================

* Initial fork from Grok.
