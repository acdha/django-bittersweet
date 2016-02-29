# encoding: utf-8
"""Utilities for manipulating the current template context"""
from __future__ import absolute_import, division, print_function, unicode_literals

from django import template

register = template.Library()


@register.filter
def get_key(dictlike, key):
    """Filter to return a dictionary value by name

    Returns ``None`` if the key does not exist so either check or use ``|default_if_none``

    Usage::

        {{ my_dict|get_key:"the key I want" }}
    """

    return dictlike.get(key, None)
