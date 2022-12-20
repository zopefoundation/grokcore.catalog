"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. Here we show what happens if you try
to set up an index for an attribute that does not exist on the interface.

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  Traceback (most recent call last):
    ...
  martian.error.GrokError: grokcore.catalog.Indexes in <module 'grokcore.catalog.tests.functional.catalog.indexes_nonexistent' from ...> refers to an attribute or method 'foo' on interface <InterfaceClass grokcore.catalog.tests.functional.catalog.indexes_nonexistent.IMammoth>, but this does not exist.

Nuke the catalog and intids in the end, so as not to confuse
other tests::

  >>> from zope.component.hooks import setSite
  >>> setSite(herd)
  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility
  >>> catalog = getUtility(ICatalog)

  >>> sm = herd.getSiteManager()
  >>> from zope.catalog.interfaces import ICatalog
  >>> sm.unregisterUtility(catalog, provided=ICatalog)
  True
  >>> from zope.intid.interfaces import IIntIds
  >>> from zope import component
  >>> intids = component.getUtility(IIntIds)
  >>> sm.unregisterUtility(intids, provided=IIntIds)
  True
"""  # noqa: E501 line too long

import grokcore.site
from grokcore.content import Container
from zope.interface import Attribute
from zope.interface import Interface

import grokcore.catalog


class Herd(Container, grokcore.site.Application):
    pass


class IMammoth(Interface):
    name = Attribute('name')
    age = Attribute('age')

    def message():
        """Message the mammoth has for the world.
        """


class MammothIndexes(grokcore.catalog.Indexes):
    grokcore.site.site(Herd)
    grokcore.catalog.context(IMammoth)
    foo = grokcore.catalog.Field()
