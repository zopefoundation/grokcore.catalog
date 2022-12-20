"""
We now demonstrate the use of a SetIndex with Grok::

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.component.hooks import setSite
  >>> setSite(herd)

Now we add some indexable objects to the site::

  >>> herd['alpha'] = Mammoth('Alpha', ['big', 'brown'])
  >>> herd['beta'] = Mammoth('Beta', ['big', 'black', 'friendly'])
  >>> herd['gamma'] = Mammoth('Gamma', ['brown', 'friendly', 'gorgeous'])

Let's query the set index::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = getUtility(ICatalog)
  >>> def sortedResults(catalog, **kw):
  ...    result = list(catalog.searchResults(**kw))
  ...    result.sort(key=lambda x:x.name)
  ...    return [item.name for item in result]
  >>> sortedResults(catalog, features={'any_of': ['brown']})
  ['Alpha', 'Gamma']
  >>> sortedResults(catalog, features={'any_of': ['big']})
  ['Alpha', 'Beta']
  >>> sortedResults(catalog, features={'any_of': ['friendly']})
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
from grokcore.content import Container
from grokcore.content import Model
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implementer

import grokcore.catalog


class Herd(Container, grokcore.site.Application):
    pass


class IMammoth(Interface):
    features = Attribute('Features')


class MammothIndexes(grokcore.catalog.Indexes):
    grokcore.site.site(Herd)
    grokcore.catalog.context(IMammoth)

    features = grokcore.catalog.Set()


@implementer(IMammoth)
class Mammoth(Model):

    def __init__(self, name, features):
        self.name = name
        self.features = features
