"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. In fact, we have multiple grok.Indexes
setting up more than one set of indexes in the same catalog.

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.site.hooks import setSite
  >>> setSite(herd)

We are able to query the catalog::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = getUtility(ICatalog)
  >>> sorted(catalog.keys())
  [u'age', u'age2', u'message', u'message2', u'name', u'name2']
  
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

import grokcore.catalog
import grokcore.site
from grokcore.content import Container, Application
from zope.interface import Interface
from zope import schema


class Herd(Container, Application):
    pass


class IMammoth(Interface):
    name = Attribute('Name')
    age = Attribute('Age')

    def message():
        """Message the mammoth has for the world.
        """


class IMammoth2(Interface):
    name2 = Attribute('Name')
    age2 = Attribute('Age')

    def message2():
        """Message the mammoth has for the world.
        """


class MammothIndexes(grokcore.catalog.Indexes):
    grokcore.site.site(Herd)
    grokcore.catalog.context(IMammoth)

    name = grokcore.catalog.Field()
    age = grokcore.catalog.Field()
    message = grokcore.catalog.Text()


class MammothIndexes2(grokcore.catalog.Indexes):
    grok.site(Herd)
    grok.context(IMammoth2)

    name2 = grokcore.catalog.Field()
    age2 = grokcore.catalog.Field()
    message2 = grokcore.catalog.Text()
