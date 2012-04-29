"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. In fact, we have multiple grok.Indexes
setting up more than one set of indexes in the same catalog. What if these
indexes define the same names?

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  Traceback (most recent call last):
    ...
  KeyError: u'name'

  >>> from zope.site.hooks import setSite
  >>> setSite(herd)
  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = getUtility(ICatalog)

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

Unfortunately ftests don't have good isolation from each other yet.
"""

import grokcore.site
import grokcore.catalog
from grokcore.content import Container
from zope.interface import Interface, Attribute


class Herd(Container, grokcore.site.Application):
    pass


class IMammoth(Interface):
    name = Attribute('name')


class IMammoth2(Interface):
    name = Attribute('name')


class MammothIndexes(grokcore.catalog.Indexes):
    grokcore.site.site(Herd)
    grokcore.catalog.context(IMammoth)
    name = grokcore.catalog.Field()


class MammothIndexes2(grokcore.catalog.Indexes):
    grokcore.site.site(Herd)
    grokcore.catalog.context(IMammoth2)
    name = grokcore.catalog.Field()
