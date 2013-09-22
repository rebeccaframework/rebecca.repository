from setuptools import setup, find_packages
import sys
import os

py3 = sys.version_info.major >= 3

version = '0.0'

requires = [
    "setuptools",
    "zope.interface",
    "six",
]

tests_require = [
    "pytest",
    "pytest-cov",
    "coverage",
    "testfixtures",
    "pyramid",
]

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='rebecca.repository',
      version=version,
      description="helper utility for repository pattern of PofEAA",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Framework :: Pyramid",
        ],
      keywords='',
      author='Atsushi Odagiri',
      author_email='aodagx@gmail.com',
      url='https://github.com/rebeccaframework/rebecca.repository',
      license='MIT',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['rebecca'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      extras_require={
          "testing": tests_require,
          "dev": ["docutils"],
          "pyramid": ["pyramid"],
          "sqlalchemy": ["sqlalchemy"],
          "fs": ["repoze.filesafe"],
      },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
