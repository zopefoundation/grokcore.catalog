"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. We can specify the catalog name using
grok.name.

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.site.hooks import setSite
  >>> setSite(herd)

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility

We have to look up the catalog by name now::

  >>> catalog = getUtility(ICatalog, 'foo_catalog')
  >>> catalog
  <zope.catalog.catalog.Catalog object at ...>

Nuke the catalog and intids in the end, so as not to confuse
other tests::

  >>> sm = herd.getSiteManager()
  >>> from zope.catalog.interfaces import ICatalog
  >>> sm.unregisterUtility(catalog, provided=ICatalog, name='foo_catalog')
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
from grokcore.content import Container, Application, Model


class Herd(Container, Application):
    pass


class Mammoth(Model):

    def __init__(self, name, age, message):
        self.name = name
        self.age = age
        self._message = message

    def message(self):
        return self._message


class MammothIndexes(grokcore.catalog.Indexes):
    grokcore.catalog.context(Mammoth)
    grokcore.catalog.name('foo_catalog')
    grokcore.site.site(Herd)

    name = grokcore.catalog.Field()
    age = grokcore.catalog.Field()
    message = grokcore.catalog.Text()
