"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. Here we see how we can register indexes for
an interface instead of an application directly.

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.site.hooks import setSite
  >>> setSite(herd)

We are able to find the catalog::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility
  >>> catalog = getUtility(ICatalog)
  >>> catalog is not None
  True
  >>> catalog.get('name') is not None
  True

Nuke the catalog and intids for this site, so as not to confuse
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

Now let's create another application providing the same interface::

  >>> herd2 = Herd2()
  >>> getRootFolder()['herd2'] = herd2
  >>> setSite(herd2)
  >>> catalog = getUtility(ICatalog)
  >>> catalog is not None
  True
  >>> catalog.get('name') is not None
  True

Nuke the catalog and intids in the end, so as not to confuse
other tests::

  >>> sm = herd2.getSiteManager()
  >>> sm.unregisterUtility(catalog, provided=ICatalog)
  True
  >>> intids = component.getUtility(IIntIds)
  >>> sm.unregisterUtility(intids, provided=IIntIds)
  True
"""

import grokcore.site
import grokcore.catalog
from grokcore.content import Container
from zope.interface import Attribute, Interface, implementer


class IHerd(Interface):
    pass


@implementer(IHerd)
class Herd(Container, grokcore.site.Application):
    pass


@implementer(IHerd)
class Herd2(Container, grokcore.site.Application):
    pass


class IMammoth(Interface):
    name = Attribute("")
    age = Attribute("")

    def message():
        """Message the mammoth has for the world.
        """


class MammothIndexes(grokcore.catalog.Indexes):
    grokcore.site.site(IHerd)
    grokcore.catalog.context(IMammoth)

    name = grokcore.catalog.Field()
    age = grokcore.catalog.Field()
    message = grokcore.catalog.Text()
