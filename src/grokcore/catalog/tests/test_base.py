import doctest
import unittest
from pkg_resources import resource_listdir

from zope.testing import cleanup, renormalizing
import zope.component.eventtesting


def setUpZope(test):
    zope.component.eventtesting.setUp(test)


def cleanUpZope(test):
    cleanup.cleanUp()


checker = renormalizing.RENormalizing()


def suiteFromPackage(name):
    layer_dir = 'base'
    files = resource_listdir(__name__, '{}/{}'.format(layer_dir, name))
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename.endswith('_fixture.py'):
            continue
        if filename == '__init__.py':
            continue

        print(filename)

        dottedname = 'grokcore.catalog.tests.%s.%s.%s' % (
            layer_dir, name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            setUp=setUpZope,
            tearDown=cleanUpZope,
            checker=checker,
            optionflags=(
                doctest.ELLIPSIS +
                doctest.NORMALIZE_WHITESPACE +
                renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2))

        suite.addTest(test)

    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ['catalog']:
        suite.addTest(suiteFromPackage(name))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
