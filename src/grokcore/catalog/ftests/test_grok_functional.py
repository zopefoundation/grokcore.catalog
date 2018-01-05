import doctest
import unittest
from pkg_resources import resource_listdir

from zope.app.appsetup.testlayer import ZODBLayer
from zope.testing import renormalizing

import grokcore.catalog


FunctionalLayer = ZODBLayer(grokcore.catalog)


checker = renormalizing.RENormalizing()


def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'grokcore.catalog.ftests.%s.%s' % (name, filename[:-3])
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


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
