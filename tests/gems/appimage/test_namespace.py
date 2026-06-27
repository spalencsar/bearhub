from unittest import TestCase

from bearhub.gems.appimage.controller import AppImageManager
from bearhub.view.core.gems import _discover_gem_dirs, _import_controller_module


class TestAppImageNamespace(TestCase):

    def test_bauh_compat_import(self):
        from bauh.gems.appimage.util import replace_desktop_entry_exec_command

        self.assertTrue(callable(replace_desktop_entry_exec_command))

    def test_appimage_discovered_under_bearhub(self):
        gem_dirs = dict(_discover_gem_dirs())
        self.assertIn('appimage', gem_dirs)
        self.assertIn('bearhub/gems/appimage', gem_dirs['appimage'].replace('\\', '/'))

    def test_controller_import_prefers_bearhub(self):
        module = _import_controller_module('appimage')
        self.assertEqual(module.__name__, 'bearhub.gems.appimage.controller')
        self.assertIs(module.AppImageManager, AppImageManager)