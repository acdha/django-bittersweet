# encoding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from django.template import Context, Template

__all__ = ['JSONFilterTests']


class JSONFilterTests(unittest.TestCase):
    longMessage = True

    def test_json_basic(self):
        tmpl = Template("""{% load bittersweet_json %}"""
                        """{{ my_dict|json|safe }}""")
        ctx = Context({"my_dict": {'foo': 'bar'}})
        self.assertEqual(tmpl.render(ctx), '{"foo": "bar"}')

    def test_json_escaping(self):
        tmpl = Template("""{% load bittersweet_json %}"""
                        """{{ my_dict|json|safe }}""")
        ctx = Context({"my_dict": {'foo': '<script>alert("XSS!");</script>'}})
        self.assertEqual(tmpl.render(ctx),
                         '{"foo": "\\u003cscript\\u003ealert(\\"XSS!\\");\\u003c/script\\u003e"}')
