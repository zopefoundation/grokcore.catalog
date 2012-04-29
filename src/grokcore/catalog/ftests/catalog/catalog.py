"""
Let's setup a site in which we manage a couple of objects:

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.site.hooks import setSite
  >>> setSite(herd)

Now we add some indexable objects to the site:

  >>> herd['manfred'] = Mammoth('Manfred')
  >>> herd['ellie'] = Mammoth('Ellie')

Then we are able to query the catalog:

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility
  >>> catalog = getUtility(ICatalog)
  >>> for obj in catalog.searchResults(name=('Ellie', 'Ellie')):
  ...     print obj.name
  Ellie

Nuke the catalog and intids in the end, so as not to confuse
other tests::

  >>> from zope import component
  >>> sm = herd.getSiteManager()
  >>> sm.unregisterUtility(catalog, provided=ICatalog)
  True
  >>> intids = component.getUtility(IIntIds)
  >>> sm.unregisterUtility(intids, provided=IIntIds)
  True

"""

import grokcore.site
from zope import interface
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from zope.catalog.catalog import Catalog
from zope.catalog.interfaces import ICatalog
from zope.catalog.field import FieldIndex
from grokcore.content import Model, Container


def setup_catalog(catalog):
    catalog['name'] = FieldIndex('name', IMammoth)


class IMammoth(interface.Interface):
    name = interface.Attribute('name')


class Mammoth(Model):
    interface.implements(IMammoth)

    def __init__(self, name):
        self.name = name


class Herd(Container, grokcore.site.Site):
    grokcore.site.local_utility(
        IntIds, provides=IIntIds)
    grokcore.site.local_utility(
        Catalog, provides=ICatalog, setup=setup_catalog)
