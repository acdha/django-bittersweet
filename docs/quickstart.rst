QuickStart
==========

::

    pip install django-bittersweet

Validated ``get_or_create``
---------------------------

::

    from bittersweet.models import validated_get_or_create

    try:
        obj, created = validated_get_or_create(MyModel, key=foo, defaults={'foo': 'bar'})
    except ValidationError as exc:
        raise RuntimeError('Cannot create MyModel: %s' % exc)

Templating
----------

Filter: ``|json``
~~~~~~~~~~~~~~~~~

::

    {% load bittersweet_json %}

    {{ my_variable|json }}

Filter: ``get_key``
~~~~~~~~~~~~~~~~~~~

::

    {% load bittersweet_context_utils %}

    {{ my_dict|get_key:"title" }}

Tag: ``{% render_inline %}``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    {% load bittersweet_render_inline %}

    {% render_inline %}
        <b>{{ VARIABLE_WHICH_CONTAINS_TEMPLATE_MARKUP }}</b>
    {% end_render_inline }

Tag: ``{% add_facet %}``
~~~~~~~~~~~~~~~~~~~~~~~~

::

    {% load bittersweet_querystring %}

    <a href="?{% add_facet request.GET "item_type" "book" %}">Books</a>
    <a href="?{% add_facet request.GET field_name field_value %}">{{ field_value }}</a>

Tag: ``{% remove_facet %}``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    {% load bittersweet_querystring %}

    <a href="?{% remove_facet request.GET "item_type" "book" %}">Remove: Books</a>
    <a href="?{% remove_facet request.GET field_name field_value %}">Remove: {{ field_value }}</a>


Tag: ``{% qs_alter %}``
~~~~~~~~~~~~~~~~~~~~~~~

::

    {% load bittersweet_querystring %}

Query string provided as QueryDict::

    {% qs_alter request.GET foo=bar %}
    {% qs_alter request.GET foo=bar baaz=quux %}
    {% qs_alter request.GET foo=bar baaz=quux delete:corge %}

Remove one facet from a list::

    {% qs_alter request.GET foo=bar baaz=quux delete_value:"facets",value %}

Query string provided as string::

    {% qs_alter "foo=baaz" foo=bar %}"

Any query string may be stored in a variable in the local template context by making the last
argument "as variable_name"::

    {% qs_alter request.GET foo=bar baaz=quux delete:corge as new_qs %}
