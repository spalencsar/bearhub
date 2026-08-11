import unittest

from bearhub.stylesheet import process_theme, read_default_themes, read_theme_metada
from bearhub.view.core.config import CoreConfigManager


class UrsineThemeTest(unittest.TestCase):

    def test_ursine_theme_is_shipped(self):
        themes = read_default_themes()
        self.assertIn('ursine', themes)
        self.assertTrue(themes['ursine'].endswith('ursine.qss'))

    def test_ursine_metadata(self):
        themes = read_default_themes()
        meta = read_theme_metada(key='ursine', file_path=themes['ursine'])
        self.assertEqual('default', meta.root_theme)
        self.assertEqual('Ursine', meta.default_name)
        self.assertFalse(meta.abstract)

    def test_ursine_processes_without_unresolved_core_vars(self):
        themes = read_default_themes()
        path = themes['ursine']
        meta = read_theme_metada(key='ursine', file_path=path)
        with open(path) as f:
            raw = f.read()

        processed = process_theme(
            file_path=path,
            theme_str=raw,
            metadata=meta,
            available_themes=themes,
        )
        self.assertIsNotNone(processed)
        stylesheet = processed[0]
        self.assertIn('#1a1d23', stylesheet)  # slate panel
        self.assertIn('#e8a54b', stylesheet)  # honey accent
        # Core placeholders from ursine.vars should be substituted
        self.assertNotIn('@outer_widget.background.color', stylesheet)
        self.assertNotIn('@font.color', stylesheet)
        self.assertNotIn('@upgrade.color', stylesheet)

    def test_default_config_keeps_proven_light_until_redesign(self):
        cfg = CoreConfigManager().get_default_config()
        self.assertEqual('light', cfg['ui']['theme'])
        # Ursine remains available as an optional colors-only theme
        self.assertIn('ursine', read_default_themes())


if __name__ == '__main__':
    unittest.main()
