import doctest
import unittest
from pkg_resources import resource_listdir

from zope.app.appsetup.testlayer import ZODBLayer
from zope.site.hooks import setSite
from zope.testing import renormalizing

import grokcore.catalog


class CatalogZODBLayer(ZODBLayer):
    """Custom ZODBLayer which also cleans up the site."""

    def testTearDown(self):
        setSite(None)
        super(CatalogZODBLayer, self).testTearDown()


FunctionalLayer = CatalogZODBLayer(grokcore.catalog)
checker = renormalizing.RENormalizing()


def suiteFromPackage(name):
    layer_dir = 'functional'
    files = resource_listdir(__name__, '{}/{}'.format(layer_dir, name))
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'grokcore.catalog.tests.%s.%s.%s' % (
            layer_dir, name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            checker=checker,
            extraglobs=dict(getRootFolder=FunctionalLayer.getRootFolder),
            optionflags=(doctest.ELLIPSIS +
                         doctest.NORMALIZE_WHITESPACE +
                         doctest.REPORT_NDIFF +
                         renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2))
        test.layer = FunctionalLayer

        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ["catalog"]:
        suite.addTest(suiteFromPackage(name))
    return suite
