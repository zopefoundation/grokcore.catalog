# -*- coding: utf-8 -*-

import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


long_description = (
    read('README.rst') + '\n' + read('CHANGES.rst'))


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
    version='4.0',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.catalog',
    description='Grok-like configuration for catalog and indexes',
    long_description=long_description,
    license='ZPL 2.1',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
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
        'grokcore.component >= 2.5',
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
    extras_require={'test': tests_require},
)
