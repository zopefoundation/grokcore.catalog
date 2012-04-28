##############################################################################
#
# Copyright (c) 2006-2012 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""grokcore.catalog meta
"""
import grokcore.component
import grokcore.site
import martian
import zope.component

from grokcore.catalog.components import IndexesClass
from grokcore.site import site
from martian.error import GrokError
from zope.catalog.catalog import Catalog
from zope.catalog.interfaces import ICatalog
from zope.exceptions.interfaces import DuplicationError
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent.interfaces import IObjectAddedEvent


class IndexesGrokker(martian.InstanceGrokker):
    """Grokker for index bundles."""
    martian.component(IndexesClass)

    def grok(self, name, factory, module_info, config, **kw):
        site = grokcore.site.site.bind().get(factory)
        context = grokcore.component.context.bind().get(
            factory, module_info.getModule())
        catalog_name = grokcore.component.name.bind().get(factory)

        if site is None:
            raise GrokError(
                "No site specified for grok.Indexes "
                "subclass in module %r. "
                "Use grokcore.site.site() to specify."
                % module_info.getModule(), factory)

        indexes = getattr(factory, '__grok_indexes__', None)
        if indexes is None:
            return False

        subscriber = IndexesSetupSubscriber(
            catalog_name, indexes, context, module_info)

        subscribed = (site, IObjectAddedEvent)
        config.action(
            discriminator=None,
            callable=zope.component.provideHandler,
            args=(subscriber, subscribed))
        return True


class IndexesSetupSubscriber(object):
    """Helper that sets up indexes when their Grok site is created.

    Each `grokcore.catalog.Indexes` class serves as an assertion that,
    whenever an instance of its `grokcore.site.site()` is created,
    the given list of indexes should be generated as well.

    But a long period of time could elapse between when the application
    starts (and its indexes are grokked), and the moment, maybe days or
    weeks later, when a new instance of that `grokcore.site.Site` is created.

    Hence this `IndexesSetupSubscriber`:
    it can be instantiated at grokking time with the index information,
    and then registered with the Component Architecture as an event that
    should be fired later, whenever the right kind of `grok.Site` is
    instantiated.  At that point its `__call__` method is kicked off and
    it makes sure the index catalogs get created properly.
    """
    def __init__(self, catalog_name, indexes, context, module_info):
        self.catalog_name = catalog_name
        self.indexes = indexes
        self.context = context
        self.module_info = module_info

    def __call__(self, site, event):
        # make sure we have an intids
        self._createIntIds(site)
        
        # get the catalog
        catalog = self._createCatalog(site)

        # now install indexes
        for name, index in self.indexes.items():
            try:
                index.setup(catalog, name, self.context, self.module_info)
            except DuplicationError:
                raise GrokError(
                    "grok.Indexes in module %r causes "
                    "creation of catalog index %r in catalog %r, "
                    "but an index with that name is already present." %
                    (self.module_info.getModule(), name, self.catalog_name),
                    None)

    def _createCatalog(self, site):
        """Create the catalog if needed and return it.

        If the catalog already exists, return that.

        """
        catalog = zope.component.queryUtility(
            ICatalog, name=self.catalog_name, context=site, default=None)
        if catalog is not None:
            return catalog
        catalog = Catalog()
        setupUtility = zope.component.getUtility(
            grokcore.site.interfaces.IUtilityInstaller)
        setupUtility(site, catalog, ICatalog, name=self.catalog_name)
        return catalog

    def _createIntIds(self, site):
        """Create intids if needed, and return it.
        """
        intids = zope.component.queryUtility(
            IIntIds, context=site, default=None)
        if intids is not None:
            return intids
        intids = IntIds()
        setupUtility = zope.component.getUtility(
            grokcore.site.interfaces.IUtilityInstaller)
        setupUtility(site, intids, IIntIds)
        return intids
