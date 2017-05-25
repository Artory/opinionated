import codecs
import unittest
from setuptools import setup, Command
import sys

import opinionated

class RunTests(Command):
  user_options = []

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    loader = unittest.TestLoader()
    tests = loader.discover('tests', pattern='test_*.py', top_level_dir='.')
    runner = unittest.TextTestRunner()
    results = runner.run(tests)
    sys.exit(0 if results.wasSuccessful() else 1)


with codecs.open('README.rst', 'r', 'utf-8') as fd:
  setup(
      name='opinionated',
      version=opinionated.__version__,
      description='Opinionated formatter/normalizer for python code',
      long_description=fd.read(),
      license='Apache License, Version 2.0',
      packages=['opinionated'],
      classifiers=[
          'Development Status :: 1 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Quality Assurance',
      ],
      entry_points={'console_scripts': ['opinionated = opinionated:run_main'],},
      cmdclass={'test': RunTests,},)
