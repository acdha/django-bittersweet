# encoding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from django.template import Context, Template

__all__ = ['RenderInlineTests']


class RenderInlineTests(unittest.TestCase):
    longMessage = True

    def test_render_inline(self):
        tmpl = Template("""{% load bittersweet_render_inline %}"""
                        """{% render_inline %}{{ template_fragment }}{% end_render_inline %}""")
        ctx = Context({'template_fragment': 'This is “{{ foo }}”', 'foo': 'bar'})
        self.assertEqual(tmpl.render(ctx),
                         "This is “bar”")
