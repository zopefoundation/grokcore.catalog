"""
We now demonstrate the use of a ValueIndex with Grok::

Let's set up a site in which we manage a couple of objects::

  >>> import datetime
  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.component.hooks import setSite
  >>> setSite(herd)

Now we add some indexable objects to the site::

  >>> herd['alpha'] = Opossum('Alpha', datetime.datetime(2001, 6, 7))
  >>> herd['beta'] = Opossum('Beta', datetime.datetime(2001, 7, 8))
  >>> herd['gamma'] = Opossum('Gamma', datetime.datetime(2001, 7, 9))
  >>> herd['delta'] = Opossum('Delta', datetime.datetime(2001, 9, 24))

Let's query the datetime index::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = getUtility(ICatalog)
  >>> def sortedResults(catalog, **kw):
  ...    result = list(catalog.searchResults(**kw))
  ...    result.sort(key=lambda x:x.name)
  ...    return [item.name for item in result]
  >>> sortedResults(catalog, birthday={
  ...     'any_of': [datetime.datetime(2001, 6, 7),
  ...                datetime.datetime(2001, 9, 24)]})
  ['Alpha', 'Delta']
  >>> sortedResults(catalog, birthday={
  ...     'between': [datetime.datetime(2001, 6, 7),
  ...                datetime.datetime(2001, 7, 9)]})
  ['Alpha', 'Beta', 'Gamma']
  >>> sortedResults(catalog, birthday={
  ...     'between': [datetime.datetime(2001, 6, 7),
  ...                datetime.datetime(2001, 7, 9),
  ...                True,  # exclude boundary.
  ...                True  # exclude boundary.
  ...                ]})
  ['Beta']

Note how the index uses a seconds-resolution and sub-second data is ignored::

  >>> herd['omega'] = Opossum(
  ...     'Omega', datetime.datetime(2002, 5, 3, 14, 53, 14, 1))
  >>> herd['psi'] = Opossum(
  ...     'Psi', datetime.datetime(2002, 5, 3, 14, 53, 14, 999999))
  >>> sortedResults(catalog, birthday={
  ...     'between': [datetime.datetime(2002, 5, 3, 14, 53, 14),
  ...                 datetime.datetime(2002, 5, 3, 14, 53, 14)]})
  ['Omega', 'Psi']

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


class IOpossum(Interface):
    name = Attribute('Name')
    birthday = Attribute('Birthday')


class OpossumIndexes(grokcore.catalog.Indexes):
    grokcore.site.site(Herd)
    grokcore.catalog.context(IOpossum)

    birthday = grokcore.catalog.Datetime()


@implementer(IOpossum)
class Opossum(Model):

    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday
