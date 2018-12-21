#!/usr/bin/env python3
import unittest
from setuptools import setup

def test_suite():
    loader = unittest.TestLoader()
    return loader.discover('tests', pattern='test_*.py')

setup(
    name='flask-auth-server',
    version='0.0.1',
    author='Ezra Singh',
    author_email='singhezra@gmail.com',
    license='MIT',
    test_suite='setup.test_suite'
)