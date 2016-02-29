# encoding: utf-8
"""
Render a template variable as Django template source in the current context
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from django import template

register = template.Library()


class RenderInlineNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        source = self.nodelist.render(context)
        t = template.Template(source)
        return t.render(context)


@register.tag
def render_inline(parser, token):
    """
    A template tag which renders its contents as a template using the current context, allowing you to process
    template code stored in something like gettext blocks, model content, ``django-flatblocks``, etc. as if
    it was actually in the current template.

    .. note: this could use things like ``|safe`` and is not safe to use on untrusted data

    Usage:

        my_template.html::

            {% render_inline %}
            <b>{{ VARIABLE_WHICH_CONTAINS_TEMPLATE_MARKUP }}</b>
            {% end_render_inline %}

        Context::

            {'VARIABLE_WHICH_CONTAINS_TEMPLATE_MARKUP': 'Hello {{ CURRENT_USER.name }}'}

        Output::

            '<b>Hello J. Random User</b>'
    """

    nodelist = parser.parse(('end_render_inline', ))

    parser.delete_first_token()

    return RenderInlineNode(nodelist)
