from unittest import TestCase
from unittest.mock import Mock, patch

from bearhub.gems.web.controller import DEFAULT_LANGUAGE_HEADER
from bearhub.gems.web.controller import WebApplicationManager

LOCALE_TARGET = 'bearhub.gems.web.controller.locale.getlocale'


class ControllerTest(TestCase):

    def test_DEFAULT_LANGUAGE_HEADER(self):
        self.assertEqual('en-US, en', DEFAULT_LANGUAGE_HEADER)


class WebApplicationManagerTest(TestCase):

    def setUp(self):
        self.manager = WebApplicationManager(context=Mock())

    @patch(LOCALE_TARGET, side_effect=Exception)
    def test_get_accept_language_header__must_return_default_locale_when_exception_raised(self, getlocale: Mock):
        returned = self.manager.get_accept_language_header()
        self.assertEqual(DEFAULT_LANGUAGE_HEADER, returned)
        getlocale.assert_called_once()

    @patch(LOCALE_TARGET, return_value=(None, None))
    def test_get_accept_language_header__must_return_default_locale_when_no_locale_is_returned(self, getlocale: Mock):
        returned = self.manager.get_accept_language_header()
        self.assertEqual(DEFAULT_LANGUAGE_HEADER, returned)
        getlocale.assert_called_once()

    @patch(LOCALE_TARGET, return_value=('es_AR', 'UTF-8'))
    def test_get_accept_language_header__must_return_the_system_locale_without_underscore_plus_default_locale(self, getlocale: Mock):
        returned = self.manager.get_accept_language_header()
        self.assertEqual(f'es-AR, es, {DEFAULT_LANGUAGE_HEADER}', returned)
        getlocale.assert_called_once()

    @patch(LOCALE_TARGET, return_value=('es', 'UTF-8'))
    def test_get_accept_language_header__must_return_the_simple_system_locale_plus_default_locale(self, getlocale: Mock):
        returned = self.manager.get_accept_language_header()
        self.assertEqual(f'es, {DEFAULT_LANGUAGE_HEADER}', returned)
        getlocale.assert_called_once()

    @patch(LOCALE_TARGET, return_value=('en_IN', 'UTF-8'))
    def test_get_accept_language_header__must_not_concatenate_default_locale_if_system_locale_has_it(self, getlocale: Mock):
        returned = self.manager.get_accept_language_header()
        self.assertEqual('en-IN, en', returned)
        getlocale.assert_called_once()

    def test_strip_url_protocol__http_no_www(self):
        res = self.manager.strip_url_protocol('http://test.com')
        self.assertEqual('test.com', res)

    def test_strip_url_protocol__http_with_www(self):
        res = self.manager.strip_url_protocol('http://www.test.com')
        self.assertEqual('test.com', res)

    def test_strip_url_protocol__https_no_www(self):
        res = self.manager.strip_url_protocol('https://test.com')
        self.assertEqual('test.com', res)

    def test_strip_url_protocol__https_with_www(self):
        res = self.manager.strip_url_protocol('https://www.test.com')
        self.assertEqual('test.com', res)