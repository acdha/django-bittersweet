#!/usr/bin/env python
# encoding: utf-8
import os
import re
import sys

from setuptools import setup

readme = open('README.rst').read()

setup(
    name='django-bittersweet',
    version='1.0.0',
    description="""Reusable Django model validation utility""",
    long_description=readme,
    author='Chris Adams',
    author_email='chris@improbable.org',
    url='https://github.com/acdha/django-bittersweet',
    packages=[
        'bittersweet',
    ],
    include_package_data=True,
    install_requires=[
        'Django'
    ],
    test_suite='tests.run_tests.run_tests',
    license='CC0',
    zip_safe=False,
    keywords='bittersweet',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
