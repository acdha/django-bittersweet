# encoding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from mock import patch

from django.http import QueryDict
from django.template import Context, Template


__all__ = ['QueryStringTagTests']


# We don't need to spend time escaping and unescaping our data but we do want to verify that it's called:
@patch('bittersweet.templatetags.bittersweet_querystring.escape', side_effect=lambda i: i)
class QueryStringTagTests(unittest.TestCase):
    longMessage = True

    # NOTE: we have to compare any querystring with more than one key using
    #       assertDictEqual because the key ordering will vary depending on
    #       the Python version and random hash seed or $PYTHONHASHSEED.

    def test_add_facet(self, mock_escape):
        tmpl = Template("""{% load bittersweet_querystring %}"""
                        """{% add_facet qd "item_type" "book" %}""")
        ctx = Context({'qd': QueryDict('q=lincoln')})

        # Note that QueryDict serializes as a dict-of-lists because querystrings
        # are allowed to have multiple values for the same key:
        self.assertDictEqual(QueryDict(tmpl.render(ctx)),
                             {'q': ['lincoln'], 'item_type': ['book']})

        ctx = Context({'qd': QueryDict('q=lincoln&item_type=movie')})
        self.assertDictEqual(QueryDict(tmpl.render(ctx)),
                             {'q': ['lincoln'], 'item_type': ['movie', 'book']})

        self.assertEqual(mock_escape.call_count, 2)

    def test_remove_facet(self, mock_escape):
        tmpl = Template("""{% load bittersweet_querystring %}"""
                        """{% remove_facet qd "item_type" "movie" %}""")
        ctx = Context({'qd': QueryDict('q=lincoln&item_type=movie')})
        self.assertEqual(tmpl.render(ctx), 'q=lincoln')

        ctx = Context({'qd': QueryDict('q=lincoln&item_type=movie&item_type=book')})
        self.assertDictEqual(QueryDict(tmpl.render(ctx)),
                             {'q': ['lincoln'], 'item_type': ['book']})

        self.assertEqual(mock_escape.call_count, 2)

    def test_remove_facet_decode_errors(self, mock_escape):
        # Observed in-the-wild unusual character encodings:
        # This was received as raw Windows-1256 data:
        q_encoded = b'q=\xdf\xca\xc7\xc8+\xc7\xe1\xda\xd4\xde+\xe6+\xc7\xe1\xda\xd6\xe3\xc7\xc1'
        q = q_encoded.decode('windows-1256')

        ctx = Context({'qd': QueryDict(q_encoded)})

        tmpl = Template("""{%% load bittersweet_querystring %%}"""
                        """{%% remove_facet qd "q" "%s" %%}""" % q)

        # In Django 1.6, the invalid data would be replaced with a Unicode REPLACEMENT CHARACTER
        # In Django 1.7+, the invalid data is decoded as ISO-8859-1 which is almost certainly
        # not the actual encoding but our goal is simply to confirm that the malformed request
        # will not cause an exception
        self.assertIn('q=%C3%9F%C3', tmpl.render(ctx),
                      'remove_facet should not choke on invalid data')
        self.assertEqual(mock_escape.call_count, 1)

    def test_qs_alter_add(self, mock_escape):
        tmpl = Template("""{% load bittersweet_querystring %}"""
                        """{% qs_alter qd foo="bar" %}""")
        ctx = Context({'qd': QueryDict('q=lincoln')})
        self.assertDictEqual(QueryDict(tmpl.render(ctx)),
                             {'q': ['lincoln'], 'foo': ['bar']})
        self.assertEqual(mock_escape.call_count, 1)

    def test_qs_alter_delete(self, mock_escape):
        tmpl = Template("""{% load bittersweet_querystring %}"""
                        """{% qs_alter qd foo="bar" delete:q %}""")
        ctx = Context({'qd': QueryDict('q=lincoln')})
        self.assertEqual(tmpl.render(ctx), 'foo=bar')
        self.assertEqual(mock_escape.call_count, 1)

    def test_qs_alter_delete_value(self, mock_escape):
        tmpl = Template("""{% load bittersweet_querystring %}"""
                        """{% qs_alter qd delete_value:"q","president" %}""")
        ctx = Context({'qd': QueryDict('q=lincoln&q=president')})
        self.assertEqual(tmpl.render(ctx), 'q=lincoln')
        self.assertEqual(mock_escape.call_count, 1)

    def test_qs_alter_delete_value_from_variable(self, mock_escape):
        tmpl = Template("""{% load bittersweet_querystring %}"""
                        """{% qs_alter qd delete_value:"q",value_to_delete %}""")
        ctx = Context({'qd': QueryDict('q=lincoln&q=president'),
                       'value_to_delete': 'president'})
        self.assertEqual(tmpl.render(ctx), 'q=lincoln')
        self.assertEqual(mock_escape.call_count, 1)

    def test_qs_alter_add_using_string(self, mock_escape):
        tmpl = Template("""{% load bittersweet_querystring %}"""
                        """{% qs_alter "q=lincoln" foo="bar" %}""")
        self.assertDictEqual(QueryDict(tmpl.render(Context())),
                             {'q': ['lincoln'], 'foo': ['bar']})
        self.assertEqual(mock_escape.call_count, 1)

    def test_qs_alter_delete_using_string(self, mock_escape):
        tmpl = Template("""{% load bittersweet_querystring %}"""
                        """{% qs_alter "q=lincoln" foo="bar" delete:q %}""")
        self.assertEqual(tmpl.render(Context()), 'foo=bar')
        self.assertEqual(mock_escape.call_count, 1)

    def test_qs_alter_delete_value_using_string(self, mock_escape):
        tmpl = Template("""{% load bittersweet_querystring %}"""
                        """{% qs_alter "q=president&q=lincoln" delete_value:"q","president" %}""")
        self.assertEqual(tmpl.render(Context()), 'q=lincoln')
        self.assertEqual(mock_escape.call_count, 1)

    def test_qs_alter_delete_value_from_variable_using_string(self, mock_escape):
        tmpl = Template("""{% load bittersweet_querystring %}"""
                        """{% qs_alter "q=lincoln&q=president" delete_value:"q",value_to_delete %}""")
        ctx = Context({'value_to_delete': 'president'})
        self.assertEqual(tmpl.render(ctx), 'q=lincoln')
        self.assertEqual(mock_escape.call_count, 1)
