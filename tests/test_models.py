#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from bittersweet.models import validated_get_or_create
from django.test import TestCase
from mock import patch

from .models import TestModel


class TestValidated_get_or_create(TestCase):

    def test_preexisting(self):
        TestModel.objects.create(title='Pre-Existing Model', external_id=1)

        with patch.object(TestModel, 'save') as patch_save:
            obj, created = validated_get_or_create(TestModel, external_id=1)
            self.assertFalse(patch_save.called)

        self.assertFalse(created)
        self.assertEqual('Pre-Existing Model', obj.title)
        self.assertEqual(obj.external_id, 1)

    def test_created(self):
        with patch.object(TestModel, 'save') as patch_save:
            with patch.object(TestModel, 'full_clean') as patch_full_clean:
                obj, created = validated_get_or_create(TestModel, external_id=1, defaults={'title': 'New'})
                self.assertTrue(patch_save.called)
                self.assertTrue(patch_full_clean.called)

        self.assertTrue(created)
        self.assertEqual(obj.external_id, 1)
        self.assertEqual('New', obj.title)
