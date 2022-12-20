import doctest
import unittest

from pkg_resources import resource_listdir

import zope.component.eventtesting
from zope.testing import cleanup


def setUpZope(test):
    zope.component.eventtesting.setUp(test)


def cleanUpZope(test):
    cleanup.cleanUp()


def suiteFromPackage(name):
    layer_dir = 'base'
    files = resource_listdir(__name__, f'{layer_dir}/{name}')
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename.endswith('_fixture.py'):
            continue
        if filename == '__init__.py':
            continue

        print(filename)

        dottedname = 'grokcore.catalog.tests.{}.{}.{}'.format(
            layer_dir, name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            setUp=setUpZope,
            tearDown=cleanUpZope,
            optionflags=(
                doctest.ELLIPSIS +
                doctest.NORMALIZE_WHITESPACE))

        suite.addTest(test)

    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ['catalog']:
        suite.addTest(suiteFromPackage(name))
    return suite
