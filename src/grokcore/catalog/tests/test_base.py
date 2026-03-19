import doctest
import unittest
from importlib.resources import files

import zope.component.eventtesting
from zope.testing import cleanup


def setUpZope(test):
    zope.component.eventtesting.setUp(test)


def cleanUpZope(test):
    cleanup.cleanUp()


def suiteFromPackage(name):
    layer_dir = 'base'
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
