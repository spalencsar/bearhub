from unittest import TestCase

from bearhub.view.util.cache import DefaultMemoryCacheFactory
from bearhub.view.util.resource import get_path
from bearhub.view.util.translation import I18n


class TestViewUtilNamespace(TestCase):

    def test_bauh_compat_import(self):
        from bauh.view.util.cache import DefaultMemoryCacheFactory as legacy_factory

        self.assertIs(legacy_factory, DefaultMemoryCacheFactory)

    def test_resource_prefers_bearhub_tree(self):
        path = get_path('locale/about/en')
        self.assertIn('bearhub/view/resources', path.replace('\\', '/'))

    def test_translation_class_available(self):
        self.assertTrue(callable(I18n))