from unittest import TestCase

from bearhub.gems.web.controller import WebApplicationManager
from bearhub.view.core.gems import _discover_gem_dirs, _import_controller_module


class TestWebNamespace(TestCase):

    def test_bauh_compat_import(self):
        from bauh.gems.web.controller import DEFAULT_LANGUAGE_HEADER

        self.assertEqual('en-US, en', DEFAULT_LANGUAGE_HEADER)

    def test_web_discovered_under_bearhub(self):
        gem_dirs = dict(_discover_gem_dirs())
        self.assertIn('web', gem_dirs)
        self.assertIn('bearhub/gems/web', gem_dirs['web'].replace('\\', '/'))

    def test_controller_import_prefers_bearhub(self):
        module = _import_controller_module('web')
        self.assertEqual(module.__name__, 'bearhub.gems.web.controller')
        self.assertIs(module.WebApplicationManager, WebApplicationManager)