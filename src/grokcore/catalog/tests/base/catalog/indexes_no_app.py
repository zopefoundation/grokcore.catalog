"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration.  We do need to specify a site (such as
the application) for the Indexes however, otherwise we get a GrokError:

(Note how the test output needs to be on one line to please to
IGNORE_EXCEPTION_MODULE_IN_PYTHON2 normalizer)

  >>> from grokcore.catalog import testing
  >>> testing.grok(__name__)
  Traceback (most recent call last):
    ...
  martian.error.GrokError: No site specified for grokcore.catalog.Indexes subclass in module <module 'grokcore.catalog.tests.base.catalog.indexes_no_app' from ...>. Use grokcore.site.site() to specify.

"""
import grokcore.site
import grokcore.catalog
import grokcore.component

from grokcore.site import Application
from grokcore.content import Model, Container


class Herd(Container, grokcore.site.Application):
    pass


class Mammoth(Model):
    pass


class MammothIndexes(grokcore.catalog.Indexes):
    grokcore.catalog.context(Mammoth)
    grokcore.catalog.name('foo_catalog')

    name = grokcore.catalog.Field()
    age = grokcore.catalog.Field()
    message = grokcore.catalog.Text()
