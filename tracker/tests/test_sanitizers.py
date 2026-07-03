from django.test import SimpleTestCase
from django.contrib.gis.geos import Point
from ..sanitizers import strip_all_strings, clean_website_url, upper_country_code

class TrackerSanitizersTest(SimpleTestCase):   # so it skips the creation of a db

    def test_strip_all_strings(self):
        data = {
            'external_id': ' way/29177094',
            'name': 'Schlachthof Gärtringen  ',
            'operator': 'Schlachthof eG   ',
            'city': 'Gärtringen',
            'country_code': 'DE',
            'postal_code': '12345',
            'street': None,
            'street_number': '',
            'coordinates': Point(8.9190879, 48.6396181)
        }
        cleaned_data = strip_all_strings(data)
        # assert stripped strings
        self.assertEqual(cleaned_data['external_id'], 'way/29177094')
        self.assertEqual(cleaned_data['name'], 'Schlachthof Gärtringen')
        self.assertEqual(cleaned_data['operator'], 'Schlachthof eG')
        self.assertEqual(cleaned_data['city'], 'Gärtringen')
        self.assertEqual(cleaned_data['country_code'], 'DE')
        self.assertEqual(cleaned_data['postal_code'], '12345')
        self.assertEqual(cleaned_data['street_number'], '')
        # assert other data types
        self.assertIsNone(cleaned_data['street'])
        self.assertEqual(cleaned_data['coordinates'].x, 8.9190879)
        self.assertEqual(cleaned_data['coordinates'].y, 48.6396181)

    def test_clean_website_url(self):
        # test for whitespace
        self.assertEqual(
            clean_website_url('  https://example.com '), 'https://example.com'
        )
        # test for uppercase
        self.assertEqual(
            clean_website_url('https://EXAMPLE.com'), 'https://example.com'
        )
        # test for protocol
        self.assertEqual(
            clean_website_url('example.com'), 'https://example.com'
        )
        # all combinations
        self.assertEqual(
            clean_website_url('  EXAMPLE.com '), 'https://example.com'
        )

    def test_empty_or_none_url(self):
        self.assertIsNone(clean_website_url(None))
        self.assertEqual(clean_website_url(''), '')
        self.assertEqual(clean_website_url('  '), '')

    def test_upper_country_code(self):
        self.assertEqual(upper_country_code('de'), 'DE')
        self.assertEqual(upper_country_code('De'), 'DE')

    def test_empty_or_none_country_code(self):
        self.assertIsNone(upper_country_code(None))
        self.assertEqual(upper_country_code(''), '')
