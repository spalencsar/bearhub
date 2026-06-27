from unittest import TestCase

from bearhub.api.paths import CONFIG_DIR, CACHE_DIR
from bearhub.commons.util import size_to_byte


class TestApiNamespace(TestCase):

    def test_bauh_compat_api_import(self):
        from bauh.api.paths import CONFIG_DIR as legacy_config

        self.assertEqual(legacy_config, CONFIG_DIR)

    def test_bauh_compat_commons_import(self):
        from bauh.commons.util import size_to_byte as legacy_size

        self.assertEqual(legacy_size(1, 'K'), size_to_byte(1, 'K'))