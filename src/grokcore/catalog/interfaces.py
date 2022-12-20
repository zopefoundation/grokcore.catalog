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
"""grokcore.catalog interfaces
"""
from zope.interface import Attribute
from zope.interface import Interface


class IIndexDefinition(Interface):
    """Define an index for grok.Indexes."""

    def __init__(self, *args, **kw):
        """Arguments and keyword arguments passed to the index class.

        All parameters are simply passed along to the index class we create,
        which interprets them as configuration details of its own.
        """

    def setup(catalog, name, context):
        """Set up index called name in given catalog.

        Use name for index name and attribute to index. Set up
        index for interface or class context.
        """


class IAttributeIndexDefinition(IIndexDefinition):
    """Define an index for grok.Indexes providing IAttributeIndex.
    """

    def __init__(self, attribute=None, *args, **kw):
        """Attribute to index.

        Attribute (optionally) defines the attribute we should index. All
        other parameters are simply passed along to the index class we
        create, which interprets them as configuration details of its own.

        Arguments and keyword arguments passed to the index class.
        """


class IBaseClasses(Interface):
    Indexes = Attribute("Base class for a catalog indexes component.")
