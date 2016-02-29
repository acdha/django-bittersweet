# encoding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from django.template import Context, Template

__all__ = ['ContextUtilsTagsTests']


class ContextUtilsTagsTests(unittest.TestCase):
    longMessage = True

    def test_get_key(self):
        tmpl = Template("""{% load bittersweet_context_utils %}"""
                        """{{ my_dict|get_key:"foo" }}""")
        ctx = Context({'my_dict': {'foo': 'bar', 'baz': 'qux'}})
        self.assertEqual(tmpl.render(ctx), 'bar')

    def test_get_key_variable(self):
        tmpl = Template("""{% load bittersweet_context_utils %}"""
                        """{{ my_dict|get_key:key_name }}""")
        ctx = Context({'my_dict': {'foo': 'bar', 'baz': 'qux'},
                       'key_name': 'baz'})
        self.assertEqual(tmpl.render(ctx), 'qux')
