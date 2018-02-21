"""
We now demonstrate the use of a ValueIndex with Grok::

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.site.hooks import setSite
  >>> setSite(herd)

Now we add some indexable objects to the site::

  >>> herd['alpha'] = SabreTooth('Alpha', 'tolerant')
  >>> herd['beta'] = SabreTooth('Beta', 'narrowminded')
  >>> herd['gamma'] = SabreTooth('Gamma', 'friendly')

Let's query the set index::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = getUtility(ICatalog)
  >>> def sortedResults(catalog, **kw):
  ...    result = list(catalog.searchResults(**kw))
  ...    result.sort(key=lambda x:x.name)
  ...    return [item.name for item in result]
  >>> sortedResults(catalog, feature={'any_of': ['tolerant', 'friendly']})
  ['Alpha', 'Gamma']

  >>> sortedResults(catalog, feature={'any_of': ['narrowminded', 'foo']})
  ['Beta']

  >>> sortedResults(catalog, feature={'any_of': ['narrowminded', 'friendly']})
  ['Beta', 'Gamma']

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
from grokcore.content import Container, Model
from zope.interface import implementer, Interface, Attribute


class Herd(Container, grokcore.site.Application):
    pass


class ISabreTooth(Interface):
    feature = Attribute('Feature')


class SabreToothIndexes(grokcore.catalog.Indexes):
    grokcore.site.site(Herd)
    grokcore.catalog.context(ISabreTooth)

    feature = grokcore.catalog.Value()


@implementer(ISabreTooth)
class SabreTooth(Model):

    def __init__(self, name, features):
        self.name = name
        self.feature = features
