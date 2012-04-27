##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
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

import martian.util
from grokcore.catalog.interfaces import IIndexDefinition


class IndexesClass(object):
    """Base class for index collections in a Grok application.

    A `grokcore.catalog.Indexes` utility provides one or more Zope Database
    content indexes for use in a :class:`grokcore.site.Site` or
    :class:`grok.Application`.  The site or application that the
    indexes are intended for should be named with the :func:`grok.site()`
    directive, and the kind of object to index should be named with a
    :func:`grokcore.component.context()` directive.

    Inside their class, the developer should specify one or more
    :class:`grokcore.catalog.index.Field`,
    :class:`grokcore.catalog.index.Text`, or
    :class:`grokcore.catalog.index.Set` instances naming object
    attributes that should be indexed (and therefore searchable).::

        class ArticleIndex(grokcore.catalog.Indexes):
            grokcore.site.site(Newspaper)
            grokcore.component.context(Article)
            author = index.Field()
            title = index.Field()
            body = index.Text()

    See the :mod:`grok.index` module for more information on field
    types.

    .. note:: Indexes are persistent: they are stored in the Zope
              database alongside the site or application that they
              index.  They are created when the site or application is
              first created (and made persistent), and so an
              already-created site will not change just because the
              definition of one of its :data:`grok.Indexes` changes;
              it will either have to be deleted and re-created, or
              some other operation performed to bring its indexes up
              to date.

    """
    def __init__(self, name, bases=(), attrs=None):
        if attrs is None:
            return
        indexes = {}
        for name, value in attrs.items():
            # Ignore everything that's not an index definition object
            # except for values set by directives
            if '.' in name:
                setattr(self, name, value)
                continue
            if not IIndexDefinition.providedBy(value):
                continue
            indexes[name] = value
        self.__grok_indexes__ = indexes
        # __grok_module__ is needed to make defined_locally() return True for
        # inline templates
        self.__grok_module__ = martian.util.caller_module()

Indexes = IndexesClass('Indexes')
