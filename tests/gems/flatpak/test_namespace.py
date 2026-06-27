from unittest import TestCase

from bearhub.gems.flatpak.controller import FlatpakManager
from bearhub.view.core.gems import _discover_gem_dirs, _import_controller_module


class TestFlatpakNamespace(TestCase):

    def test_bauh_compat_import(self):
        from bauh.gems.flatpak.model import FlatpakApplication

        self.assertTrue(issubclass(FlatpakApplication, object))

    def test_flatpak_discovered_under_bearhub(self):
        gem_dirs = dict(_discover_gem_dirs())
        self.assertIn('flatpak', gem_dirs)
        self.assertIn('bearhub/gems/flatpak', gem_dirs['flatpak'].replace('\\', '/'))

    def test_controller_import_prefers_bearhub(self):
        module = _import_controller_module('flatpak')
        self.assertEqual(module.__name__, 'bearhub.gems.flatpak.controller')
        self.assertIs(module.FlatpakManager, FlatpakManager)