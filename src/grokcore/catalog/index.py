#############################################################################
#
# Copyright (c) 2007-2008 Zope Foundation and Contributors.
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
"""grokcore.catalog index definitions
"""
import calendar
import sys

import BTrees.Length
import zc.catalog.index
import zope.catalog.attribute
import zope.catalog.interfaces
import zope.component
import zope.container.contained
from martian.error import GrokError
from martian.error import GrokImportError
from martian.util import frame_is_class
from zc.catalog.catalogindex import SetIndex
from zc.catalog.catalogindex import ValueIndex
from zope.catalog.field import FieldIndex
from zope.catalog.interfaces import IAttributeIndex
from zope.catalog.text import TextIndex
from zope.interface import implementer
from zope.interface.interfaces import IInterface
from zope.interface.interfaces import IMethod
from zope.intid.interfaces import IIntIds

from grokcore.catalog.interfaces import IAttributeIndexDefinition
from grokcore.catalog.interfaces import IIndexDefinition


@implementer(IIndexDefinition)
class IndexDefinition:
    """The definition of a particular index in a
    :data:`grokcore.catalog.Indexes` class.

    Note that, since index creation (and thus a call to our :meth:`setup()`
    method) currently occurs only during the creation of a new Grok
    `Application` object in the Zope Database, the presence of this
    declaration in Grok application code is nearly always a no-op.

    """
    index_class = None

    def __init__(self, *args, **kw):
        frame = sys._getframe(1)
        if not frame_is_class(frame):
            raise GrokImportError(
                "%r can only be instantiated on class level." % self.__class__)
        # Store any extra parameters to pass to index later.
        self._args = args
        self._kw = kw

    def setup(self, catalog, name, context, module_info):
        # For indexes that do not implement IAttributeIndex, we
        # cannot do magic things. In these cases, just initialize
        # the index with the given attributes.
        catalog[name] = self.index_class(*self._args, **self._kw)


@implementer(IAttributeIndexDefinition)
class AttributeIndexDefinition:
    """The definition of a particular index in a
    :data:`grokcore.catalog.Indexes` class.

    This base class defines the actual behavior of
    :class:`grokcore.catalog.index.Field` and the other kinds of attribute
    index that Grok supports. Upon our instantiation, we save every parameter
    that we were passed; later, if an index actually needs to be created
    (which is typically at the moment when a new
    :class:`grokcore.site.Application` object is added to the Zope Database),
    then our :meth:`setup()` method gets called.

    The only parameter that is actually significant to us is `attribute`
    which (optionally) defines the attribute we should index. All other
    parameters are simply passed along to the Zope index we create, which
    interprets them as configuration details of its own.

    Note that, since index creation (and thus a call to our :meth:`setup()`
    method) currently occurs only during the creation of a new Grok
    `Application` object in the Zope Database, the presence of this
    declaration in Grok application code is nearly always a no-op.

    """
    index_class = None

    def __init__(self, *args, **kw):
        frame = sys._getframe(1)
        if not frame_is_class(frame):
            raise GrokImportError(
                "%r can only be instantiated on class level." % self.__class__)
        if not IAttributeIndex.implementedBy(self.index_class):
            raise GrokImportError(
                "%r does not implement IAttributeIndex." % self.__class__)
        # Store any extra parameters to pass to index later.
        self._args = args
        self._attribute = kw.pop('attribute', None)
        self._kw = kw

    def setup(self, catalog, name, context, module_info):
        # If the user supplied attribute= when instantiating us, we
        # allow that value to override the attribute name under which we
        # are actually stored inside of the `grokcore.catalog.Indexes`
        # instance.
        if self._attribute is not None:
            field_name = self._attribute
        else:
            field_name = name

        if IInterface.providedBy(context):
            try:
                method = context[field_name]
            except KeyError:
                raise GrokError(
                    "grokcore.catalog.Indexes in %r refers to an attribute or "
                    "method %r on interface %r, but this does not "
                    "exist." % (module_info.getModule(),
                                field_name, context), None)
            call = IMethod.providedBy(method)
        else:
            call = callable(getattr(context, field_name, None))
            context = None  # no interface lookup
        catalog[name] = self.index_class(
            field_name=field_name,
            interface=context,
            field_callable=call,
            *self._args, **self._kw)


class Field(AttributeIndexDefinition):
    """A :class:`grokcore.catalog.Indexes` index that matches
    against an entire field.
    """
    index_class = FieldIndex


class Text(AttributeIndexDefinition):
    """A :class:`grokcore.catalog.Indexes` index supporting
    full-text searches of a field.
    """
    index_class = TextIndex


class Set(AttributeIndexDefinition):
    """A :class:`grokcore.catalog.Indexes` index supporting
    keyword searches of a field.
    """
    index_class = SetIndex


class Value(AttributeIndexDefinition):
    """A :class:`grokcore.catalog.Indexes` index similar to,
    but more flexible than :class:`grokcore.catalog.Field` index.

    The index allows searches for documents that contain any of a set of
    values; between a set of values; any (non-None) values; and any empty
    values.
    """
    index_class = ValueIndex


def to_timestamp(dt):
    if dt is None:
        return None
    return calendar.timegm(dt.timetuple())


class _DatetimeIndex(zc.catalog.index.ValueIndex):

    def clear(self):
        self.values_to_documents = BTrees.LOBTree.LOBTree()
        self.documents_to_values = BTrees.LLBTree.LLBTree()
        self.documentCount = BTrees.Length.Length(0)
        self.wordCount = BTrees.Length.Length(0)

    def index_doc(self, doc_id, value):
        if value is None:
            return
        value = to_timestamp(value)
        super().index_doc(doc_id, value)

    def apply(self, query):
        if 'any_of' in query:
            # The "value" of the dict is a sequence of datetime objects.
            # Convert it into a timestamps.
            query['any_of'] = [to_timestamp(v) for v in query['any_of']]
        elif 'between' in query:
            # The "value" of the dict is a sequence of arguments to pass on to
            # the underlying btree. Convert the first two parameters that are
            # datetime objects (or None) into timestamps.
            query['between'] = parameters = list(query['between'])
            parameters[0] = to_timestamp(parameters[0])
            parameters[1] = to_timestamp(parameters[1])
        return super().apply(query)

    def values(self, min=None, max=None, excludemin=False, excludemax=False,
               doc_id=None):
        min = to_timestamp(min) if min is not None else None
        max = to_timestamp(max) if max is not None else None
        return super().values(
            min, max, excludemin, excludemax, doc_id)


class DatetimeIndex(
        zope.catalog.attribute.AttributeIndex,
        _DatetimeIndex,
        zope.container.contained.Contained):
    pass


class _IntIdIndex(zope.index.field.index.FieldIndex):

    def clear(self):
        self._fwd_index = BTrees.IOBTree.IOBTree()
        self._rev_index = BTrees.IIBTree.IIBTree()
        self._num_docs = BTrees.Length.Length(0)

    def _get_value_id(self, value):
        if value is None:
            return None
        if isinstance(value, int):
            return value
        intids = zope.component.getUtility(IIntIds)
        return intids.getId(value)

    def index_doc(self, docid, value):
        return super().index_doc(
            docid, self._get_value_id(value))

    def apply(self, query):
        value = self._get_value_id(query)
        return super().apply((value, value))


class IntIdIndex(
        zope.catalog.attribute.AttributeIndex,
        _IntIdIndex,
        zope.container.contained.Contained):
    pass


class Datetime(AttributeIndexDefinition):
    """A :class:`grokcore.catalog.Indexes` index specifically meant for
    datetime objects.

    """
    index_class = DatetimeIndex


class IntId(AttributeIndexDefinition):
    """A :class:`grokcore.catalog.Indexes` index specifically meant to index
    values with their intid.

    """
    index_class = IntIdIndex
