from unittest import TestCase

from bearhub.gems.arch.controller import ArchManager
from bearhub.view.core.gems import _discover_gem_dirs, _import_controller_module


class TestArchNamespace(TestCase):

    def test_bauh_compat_import(self):
        from bearhub.gems.arch.model import ArchPackage

        self.assertTrue(issubclass(ArchPackage, object))

    def test_arch_discovered_under_bearhub(self):
        gem_dirs = dict(_discover_gem_dirs())
        self.assertIn('arch', gem_dirs)
        self.assertIn('bearhub/gems/arch', gem_dirs['arch'].replace('\\', '/'))

    def test_controller_import_prefers_bearhub(self):
        module = _import_controller_module('arch')
        self.assertEqual(module.__name__, 'bearhub.gems.arch.controller')
        self.assertIs(module.ArchManager, ArchManager)