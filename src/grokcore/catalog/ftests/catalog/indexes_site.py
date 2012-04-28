"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. In fact, these indexes can be set up for
any site::

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.site.hooks import setSite
  >>> setSite(herd)

The catalog is there in the site::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = queryUtility(ICatalog, default=None)
  >>> catalog is not None
  True

Nuke the catalog and intids in the end, so as not to confuse
other tests::

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
from grokcore.content import Container, Site
from zope.interface import Interface


class Herd(Container, Site):
    pass


class IMammoth(Interface):
    name = Attribute('Name')
    age = Attribute('Age')

    def message():
        """Message the mammoth has for the world.
        """


class MammothIndexes(grokcore.catalog.Indexes):
    grokcore.catalog.site(Herd)
    grokcore.catalog.context(IMammoth)

    name = grokcore.catalog.Field()
    age = grokcore.catalog.Field()
    message = grokcore.catalog.Text()
