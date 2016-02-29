# encoding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import models


class TestModel(models.Model):
    external_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
