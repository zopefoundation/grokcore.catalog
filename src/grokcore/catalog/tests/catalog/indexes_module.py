"""
You can create an index on module level, but that should lead to a GrokError:

(Note how the test output needs to be on one line to please to
IGNORE_EXCEPTION_MODULE_IN_PYTHON2 normalizer)

  >>> func()
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: <class 'grokcore.catalog.index.Field'> can only be instantiated on class level.

  >>> from grokcore.catalog import testing
  >>> testing.grok(__name__)

"""
import grokcore.site
import grokcore.content
import grokcore.catalog
import zope.index.field

from grokcore.catalog import index, Indexes


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
