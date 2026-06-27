from unittest import TestCase

from bearhub.view.qt.prepare import PreparePanel
from bearhub.view.qt.window import ManageWindow
from bearhub.view.qt.components import QtComponentsManager


class TestViewQtNamespace(TestCase):

    def test_bauh_compat_import(self):
        from bauh.view.qt.components import QtComponentsManager as legacy_manager

        self.assertIs(legacy_manager, QtComponentsManager)

    def test_prepare_panel_importable(self):
        self.assertTrue(callable(PreparePanel))

    def test_window_importable(self):
        self.assertTrue(callable(ManageWindow))