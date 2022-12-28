import doctest
import unittest

from pkg_resources import resource_listdir

from zope.app.appsetup.testlayer import ZODBLayer
from zope.component.hooks import setSite

import grokcore.catalog


class CatalogZODBLayer(ZODBLayer):
    """Custom ZODBLayer which also cleans up the site."""

    def testTearDown(self):
        setSite(None)
        super().testTearDown()


FunctionalLayer = CatalogZODBLayer(grokcore.catalog)


def suiteFromPackage(name):
    layer_dir = 'functional'
    files = resource_listdir(__name__, f'{layer_dir}/{name}')
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'grokcore.catalog.tests.{}.{}.{}'.format(
            layer_dir, name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            extraglobs=dict(getRootFolder=FunctionalLayer.getRootFolder),
            optionflags=(doctest.ELLIPSIS +
                         doctest.NORMALIZE_WHITESPACE +
                         doctest.REPORT_NDIFF))
        test.layer = FunctionalLayer

        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ["catalog"]:
        suite.addTest(suiteFromPackage(name))
    return suite
