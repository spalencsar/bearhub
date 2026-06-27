from unittest import TestCase

from bearhub.view.core.config import CoreConfigManager
from bearhub.view.core.controller import GenericSoftwareManager
from bearhub.view.core.gems import load_managers
from bearhub.view.core.update import check_for_update


class TestViewCoreNamespace(TestCase):

    def test_bauh_compat_import(self):
        from bauh.view.core.config import CoreConfigManager as legacy_config

        self.assertIs(legacy_config, CoreConfigManager)

    def test_controller_importable_from_bearhub(self):
        self.assertTrue(callable(GenericSoftwareManager))

    def test_gems_loader_native(self):
        self.assertTrue(callable(load_managers))

    def test_update_check_callable(self):
        self.assertTrue(callable(check_for_update))