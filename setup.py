# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('README.txt') + '\n' + read('CHANGES.txt'))


tests_require = [
    'grokcore.content',
    'zope.app.appsetup',
    'zope.component',
    'zope.configuration',
    'zope.location',
    'zope.testing',
    'zope.app.wsgi',
]


setup(
    name='grokcore.catalog',
    version='4.0.dev0',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://grok.zope.org',
    download_url='http://pypi.python.org/pypi/grokcore.catalog',
    description='Grok-like configuration for catalog and indexes',
    long_description=long_description,
    license='ZPL',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Zope :: 3',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'grokcore.component >= 2.5dev',
        'grokcore.site >= 1.7',
        'martian >= 0.13',
        'setuptools',
        'zc.catalog',
        'zope.annotation',
        'zope.catalog',
        'zope.component',
        'zope.container',
        'zope.event',
        'zope.exceptions',
        'zope.interface',
        'zope.intid',
        'zope.lifecycleevent',
        'zope.keyreference',
        'zope.site',
    ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
)
