"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. In fact, these indexes can be set up for
any site::

Let's set up a site in which we manage a couple of objects::

  >>> from zope.component.hooks import setSite

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> setSite(herd)

The catalog is not yet in the site::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import queryUtility

  >>> catalog = queryUtility(ICatalog, default=None)
  >>> catalog is None
  True

After a mud party it gets there though:

  >>> from zope.event import notify

  >>> notify(MudPartyEvent(herd))
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
from grokcore.content import Container
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implementer
from zope.interface.interfaces import IObjectEvent
from zope.interface.interfaces import ObjectEvent

import grokcore.catalog


class Herd(Container, grokcore.site.Site):
    pass


class IMudPartyEvent(IObjectEvent):
    pass


@implementer(IMudPartyEvent)
class MudPartyEvent(ObjectEvent):
    pass


class IMammoth(Interface):
    name = Attribute('Name')
    age = Attribute('Age')

    def message():
        """Message the mammoth has for the world.
        """


class MammothIndexes(grokcore.catalog.Indexes):
    grokcore.catalog.context(IMammoth)
    grokcore.site.site(Herd)
    grokcore.site.install_on(IMudPartyEvent)

    name = grokcore.catalog.Field()
    age = grokcore.catalog.Field()
    message = grokcore.catalog.Text()
