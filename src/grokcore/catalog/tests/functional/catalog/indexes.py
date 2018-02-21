"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration.

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.site.hooks import setSite
  >>> setSite(herd)

Now we add some indexable objects to the site::

  >>> herd['alpha'] = Mammoth('Alpha', 13, 'Hello world!')
  >>> herd['beta'] = Mammoth('Beta', 14, 'Bye World!')

We are able to query the catalog::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = getUtility(ICatalog)
  >>> for obj in catalog.searchResults(name=('Beta', 'Beta')):
  ...   print(obj.name)
  Beta

Let's query the text index, which incidentally also indexes a method::

  >>> def sortedResults(catalog, **kw):
  ...    result = list(catalog.searchResults(**kw))
  ...    result.sort(key=lambda x:x.name)
  ...    return [item.name for item in result]
  >>> sortedResults(catalog, message='world')
  ['Alpha', 'Beta']
  >>> sortedResults(catalog, message='hello')
  ['Alpha']
  >>> sortedResults(catalog, message='bye')
  ['Beta']

Note that another application that we did not register the
indexes for won't have a catalog available::

  >>> herd2 = Herd2()
  >>> getRootFolder()['herd2'] = herd2
  >>> setSite(herd2)
  >>> queryUtility(ICatalog, default=None) is None
  True
  >>> setSite(herd)

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
from grokcore.content import Container, Model
from zope.interface import Interface, Attribute, implementer


class Herd(Container, grokcore.site.Application):
    pass


class Herd2(Container, grokcore.site.Application):
    pass


class IMammoth(Interface):
    age = Attribute('Age')
    name = Attribute('Name')

    def message():
        """Message the mammoth has for the world.
        """


class MammothIndexes(grokcore.catalog.Indexes):
    grokcore.site.site(Herd)
    grokcore.catalog.context(IMammoth)

    name = grokcore.catalog.Field()
    age = grokcore.catalog.Field()
    message = grokcore.catalog.Text()


@implementer(IMammoth)
class Mammoth(Model):

    def __init__(self, name, age, message):
        self.age = age
        self.name = name
        self._message = message

    def message(self):
        return self._message
