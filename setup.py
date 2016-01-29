# -*- coding:utf-8 -*-

import os
import sys


from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
    with open(os.path.join(here, 'CHANGES.txt')) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ''


install_requires = [
    'cssutils',
]


docs_extras = [
]

tests_require = [
]

testing_extras = tests_require + [
]

setup(name='cssdiff',
      version='0.1',
      description='semantic css diff',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: Implementation :: CPython",
      ],
      keywords=["css", "cssdiff", "diff", "semantic diff", "web"],
      author="podhmo",
      author_email="",
      url="https://github.com/podhmo/cssdiff",
      packages=find_packages(exclude=["cssdiff.tests"]),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
          'testing': testing_extras,
          'docs': docs_extras,
      },
      tests_require=tests_require,
      test_suite="cssdiff.tests",
      entry_points="""
      [console_scripts]
      cssdiff=cssdiff:main
""")
