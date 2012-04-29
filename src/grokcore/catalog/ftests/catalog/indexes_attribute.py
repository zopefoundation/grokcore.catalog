"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. If you want to name the index differently
from the attribute, you can do so, by passing an explicit `attribute`
keyword argument to the field.

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.site.hooks import setSite
  >>> setSite(herd)

Now we add some indexable objects to the site::

  >>> herd['alpha'] = Mammoth('Alpha', 13)
  >>> herd['beta'] = Mammoth('Beta', 14)

We are able to query the catalog::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = getUtility(ICatalog)
  >>> for obj in catalog.searchResults(how_old=(13, 13)):
  ...   print obj.name
  Alpha

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
from grokcore.content import Container, Model
from zope.interface import implements, Attribute, Interface


class Herd(Container, grokcore.site.Application):
    pass


class IMammoth(Interface):
    age = Attribute('Age')
    name = Attribute('Name')


class MammothIndexes(grokcore.catalog.Indexes):
    grokcore.site.site(Herd)
    grokcore.catalog.context(IMammoth)

    name = grokcore.catalog.Field()
    how_old = grokcore.catalog.Field('age')


class Mammoth(Model):
    implements(IMammoth)

    def __init__(self, name, age):
        self.name = name
        self.age = age
