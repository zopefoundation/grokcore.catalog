"""
You can create an index on module level, but that should lead to a GrokError:

  >>> func()
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: <class 'grokcore.catalog.index.Field'> can only be instantiated on class level.

  >>> from grokcore.catalog import testing
  >>> testing.grok(__name__)

"""  # noqa: E501 line too long
import grokcore.content
import grokcore.site
import zope.index.field

import grokcore.catalog
from grokcore.catalog import Indexes
from grokcore.catalog import index


def func():
    index.Field()


class Herd(grokcore.site.Application):
    pass


class Mammoth(grokcore.content.Model):
    pass


class FooIndex(zope.index.field.FieldIndex):
    # Not an IAttributeIndex index type.
    index_class = zope.index.field.index.FieldIndex


class FooIndexes(Indexes):
    grokcore.catalog.context(Mammoth)
    grokcore.catalog.name('foo_catalog')
    grokcore.site.site(Herd)

    foo = FooIndex()
