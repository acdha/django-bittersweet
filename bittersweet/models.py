# encoding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from itertools import chain


def validated_get_or_create(klass, **kwargs):
    """
    Similar to :meth:`~django.db.models.query.QuerySet.get_or_create` but uses
    the methodical get/save including a full_clean() call to avoid problems with
    models which have validation requirements which are not completely enforced
    by the underlying database.

    For example, with a django-model-translation we always want to go through
    the setattr route rather than inserting into the database so translated
    fields will be mapped according to the active language. This avoids normally
    impossible situations such as creating a record where `title` is defined but
    `title_en` is not.
    """

    defaults = kwargs.pop('defaults', {})

    try:
        obj = klass.objects.get(**kwargs)
        return obj, False
    except klass.DoesNotExist:
        obj = klass()

        for k, v in chain(kwargs.items(), defaults.items()):
            setattr(obj, k, v)

        obj.full_clean()
        obj.save()
        return obj, True
