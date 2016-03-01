#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

settings.configure(DEBUG=True,
                   USE_TZ=True,
                   DATABASES={
                       'default': {
                           'ENGINE': 'django.db.backends.sqlite3',
                       }
                   },
                   INSTALLED_APPS=[
                       'django.contrib.auth',
                       'django.contrib.contenttypes',
                       'django.contrib.sites',
                       'bittersweet',
                       'tests',
                   ],
                   SITE_ID=1,
                   MIDDLEWARE_CLASSES=())

django.setup()


def get_test_runner():
    TestRunner = get_runner(settings)
    return TestRunner()


def run_tests(*args):
    if not args:
        args = ['tests']

    test_runner = get_test_runner()

    failures = test_runner.run_tests(args, interactive=True, verbosity=2)
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
