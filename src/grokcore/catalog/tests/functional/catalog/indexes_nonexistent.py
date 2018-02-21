"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. Here we show what happens if you try
to set up an index for an attribute that does not exist on the interface.

Let's set up a site in which we manage a couple of objects::

(Note how the test output needs to be on one line to please to
IGNORE_EXCEPTION_MODULE_IN_PYTHON2 normalizer)

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  Traceback (most recent call last):
    ...
  martian.error.GrokError: grokcore.catalog.Indexes in <module 'grokcore.catalog.tests.functional.catalog.indexes_nonexistent' from ...> refers to an attribute or method 'foo' on interface <InterfaceClass grokcore.catalog.tests.functional.catalog.indexes_nonexistent.IMammoth>, but this does not exist.

Nuke the catalog and intids in the end, so as not to confuse
other tests::

  >>> from zope.site.hooks import setSite
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
"""

import grokcore.site
import grokcore.catalog
from zope.interface import Interface, Attribute
from grokcore.content import Container


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
