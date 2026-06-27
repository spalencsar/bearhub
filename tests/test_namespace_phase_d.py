from unittest import TestCase

import bearhub
import bearhub.stylesheet
import bauh


class TestPhaseDVersionFlip(TestCase):

    def test_version_canonical_in_bearhub(self):
        self.assertEqual('0.10.7', bearhub.__version__)
        self.assertEqual('bearhub', bearhub.__app_name__)

    def test_bauh_shim_reexports_version(self):
        self.assertEqual(bearhub.__version__, bauh.__version__)
        self.assertEqual(bearhub.__app_name__, bauh.__app_name__)

    def test_bauh_stylesheet_shim(self):
        from bauh import stylesheet as legacy_stylesheet

        self.assertIs(legacy_stylesheet.process_var_of_vars, bearhub.stylesheet.process_var_of_vars)