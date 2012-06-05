# -*- coding: utf-8 -*-
"""
This module contains the tool of abstract.recipe.jenkinsdeploy
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1'

long_description = (
    read('abstract', 'recipe', 'jenkinsdeploy', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '********\n')

entry_point = 'abstract.recipe.jenkinsdeploy:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}
                
 
tests_require = ['zope.testing', 'zc.buildout']

setup(name='abstract.recipe.jenkinsdeploy',
      version=version,
      description="A Jenkins job deplouy tool",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        ],
      keywords='',
      author='Antonio Sagliocco',
      author_email='antonio.sagliocco@abstract.it',
      url='https://github.com/abstract-open-solutions/abstract.recipe.jenkinsdeploy',
      license='gpl',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['abstract', 'abstract.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        'fabric',
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='abstract.recipe.jenkinsdeploy.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
