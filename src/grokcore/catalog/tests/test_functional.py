import doctest
import unittest
from importlib.resources import files

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
    package_dir = files('grokcore.catalog.tests').joinpath(
        f'{layer_dir}/{name}')

    filenames = []
    for item in package_dir.iterdir():
        if item.is_file() and item.name.endswith('.py'):
            filenames.append(item.name)

    suite = unittest.TestSuite()
    for filename in sorted(filenames):
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
