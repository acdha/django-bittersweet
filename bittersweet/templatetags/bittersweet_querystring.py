# encoding: utf-8
"""
Query String manipulation filters
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from django.http import QueryDict
from django.template import Library, Node, TemplateSyntaxError, Variable
from django.utils.html import escape
from django.utils.translation import ugettext as _

register = Library()


class QueryStringAlterer(Node):
    """
    Query String alteration template tag

    Receives a query string (either text or a QueryDict such as request.GET)
    and a list of changes to apply. The result will be returned as text query
    string, allowing use like this::

        <a href="?{% qs_alter request.GET type=object.type %}">{{ label }}</a>

    There are two available alterations:

        Assignment:

            name=var

        Deletion - removes the named parameter:

            delete:name

        Delete a parameter matching a value:

            delete_value:"name",value

        Delete a parameter matching a value from another variable:

            delete_value:field_name,value

    Examples:

    Query string provided as QueryDict::

        {% qs_alter request.GET foo=bar %}
        {% qs_alter request.GET foo=bar baaz=quux %}
        {% qs_alter request.GET foo=bar baaz=quux delete:corge %}

    Remove one facet from a list::

        {% qs_alter request.GET foo=bar baaz=quux delete_value:"facets",value %}

    Query string provided as string::

        {% qs_alter "foo=baaz" foo=bar %}

    Any query string may be stored in a variable in the local template context by making the last
    argument "as variable_name"::

        {% qs_alter request.GET foo=bar baaz=quux delete:corge as new_qs %}
    """

    def __init__(self, base_qs, as_variable, *args):
        self.base_qs = Variable(base_qs)
        self.args = args
        # Control whether we return the result or save it to the context:
        self.as_variable = as_variable

    def render(self, context):
        base_qs = self.base_qs.resolve(context)

        if isinstance(base_qs, QueryDict):
            qs = base_qs.copy()
        else:
            qs = QueryDict(base_qs, mutable=True)

        for arg in self.args:
            if arg.startswith("delete:"):
                v = arg[7:]
                if v in qs:
                    del qs[v]
            elif arg.startswith("delete_value:"):
                field, value = arg[13:].split(",", 2)
                value = Variable(value).resolve(context)

                if not (field[0] == '"' and field[-1] == '"'):
                    field = Variable(field).resolve(context)
                else:
                    field = field.strip('"\'')

                f_list = qs.getlist(field)
                if value in f_list:
                    f_list.remove(value)
                    qs.setlist(field, f_list)

            else:
                k, v = arg.split("=", 2)
                qs[k] = Variable(v).resolve(context)

        encoded_qs = escape(qs.urlencode())
        if self.as_variable:
            context[self.as_variable] = encoded_qs
            return ""
        else:
            return encoded_qs

    @classmethod
    def qs_alter_tag(cls, parser, token):
        try:
            bits = token.split_contents()
        except ValueError:
            raise TemplateSyntaxError(_('qs_alter requires at least two arguments: the initial query string'
                                        ' and at least one alteration'))

        if bits[-2] == 'as':
            as_variable = bits[-1]
            bits = bits[0:-2]
        else:
            as_variable = None

        return QueryStringAlterer(bits[1], as_variable, *bits[2:])

register.tag('qs_alter', QueryStringAlterer.qs_alter_tag)


class FacetAlterer(Node):
    """
    Search Facet-oriented querystring manipulation tag

    There are two tags (`add_facet` and `remove_facet`) which accept three
    arguments:

    :param original:
        initial querystring (most commonly a QueryDict like `request.GET` but
        may also be a simple dictionary)

    :param name:
        Either a variable containing the name of the field or a quoted literal
        value

    :param value:
        Either a variable containing the value or a quoted literal value

    Both add and remove safely handle multiple values by adding or removing the
    provided value while preserving whatever other values were present in the
    provided initial querystring.

    Examples:

    The most basic form, using literal values::

        <a href="?{% add_facet request.GET "item_type" "book" %}">Books</a>

    Using a variable key and value::

        <a href="?{% add_facet request.GET field_name field_value %}">{{ field_value }}</a>
    """

    def __init__(self, mode, original_querystring, key, value, *args):
        self.original_querystring = Variable(original_querystring)

        self.key = key
        self.value = value

        if mode not in ('add', 'remove'):
            raise TemplateSyntaxError('mode must be either add or remove')

        self.mode = mode

        self.output_variable_name = None

        if args:
            if len(args) == 2 and args[0] == 'as':
                self.output_variable_name = args[1]
            else:
                raise TemplateSyntaxError('No optional arguments other than `as output_variable` are allowed')

    def render(self, context):
        original_querystring = self.original_querystring.resolve(context)

        if isinstance(original_querystring, QueryDict):
            qs = original_querystring.copy()
        else:
            qs = QueryDict(original_querystring, mutable=True)

        qs.pop("page", None)

        key = self.key
        val = self.value

        if not (key[0] == key[-1] == '"'):
            key = Variable(key).resolve(context)
        else:
            key = key.strip('"')

        if not (val[0] == val[-1] == '"'):
            val = Variable(val).resolve(context)
        else:
            val = val.strip('"')

        field_values = qs.getlist(key)

        if self.mode == "add":
            field_values.append(val)
        else:
            if val in field_values:
                field_values.remove(val)

        qs.setlist(key, field_values)

        output = escape(qs.urlencode())

        if self.output_variable_name:
            context[self.output_variable_name] = output
        else:
            return output

    @classmethod
    def add_facet(cls, parser, token):
        try:
            bits = token.split_contents()
        except ValueError:
            raise TemplateSyntaxError('add_facet requires at least three '
                                      'arguments: the initial query string, '
                                      'the field and the new value')

        return FacetAlterer("add", bits[1], *bits[2:])

    @classmethod
    def remove_facet(cls, parser, token):
        try:
            bits = token.split_contents()
        except ValueError:
            raise TemplateSyntaxError('remove_facet requires at least three '
                                      'arguments: the initial query string, '
                                      'the field and the value to remove')

        return FacetAlterer("remove", bits[1], *bits[2:])

register.tag('add_facet', FacetAlterer.add_facet)
register.tag('remove_facet', FacetAlterer.remove_facet)
