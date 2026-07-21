from django.test import TestCase
from django.contrib.gis.geos import Point
from django.utils import timezone
from datetime import timedelta
from tracker.models import Company, Facility, Violation
from tracker.serializers import (
    CompanySerializer,
    FacilitySerializer,
    ViolationSerializer,
    TrackerSerializer
)

class TrackerSerializerTest(TestCase):

    # needed to access the company.id for facility validation tests
    # not strictly needed, but shows how the path works as intended
    @classmethod
    def setUpTestData(cls):

        cls.company = Company.objects.create(
            name='  Schlachthof eG   ',
            website='companyWEB.com'
        )

    def test_company_serializer_valid(self):
        messy_data = {
            'name': '  Schlachthof eG   ',
            'website': 'companyWEB.com'
        }
        clean_data = CompanySerializer(data=messy_data)
        self.assertTrue(clean_data.is_valid(), clean_data.errors)
        self.assertEqual(clean_data.validated_data['website'], 'https://companyweb.com')

    def test_company_serializer_invalid(self):
        messy_data = {
            'name': None,
            'website': 'https://companyweb.com'
        }
        clean_data = CompanySerializer(data=messy_data)
        self.assertFalse(clean_data.is_valid(), clean_data.errors)

    def test_facility_serializer_valid(self):
        messy_data = {
            'external_id': 'way/29177094  ',
            'name': '  Schlachthof Gärtringen',
            'operator': self.company.id,
            'city': 'Gärtringen',
            'country_code': 'de',
            'postal_code': '12345',
            'street': 'Riedbrunnenstraße',
            'street_number': '5',
            # SRID = Spatial Reference System Identifier
            # tracks exact degrees of latitude and longitude
            # POINT needs to be in uppercase not to trigger future regex checks
            'coordinates': 'SRID=4326;POINT(8.9190879 48.6396181)'
        }
        clean_data = FacilitySerializer(data=messy_data)
        self.assertTrue(clean_data.is_valid(), clean_data.errors)
        self.assertEqual(clean_data.validated_data['external_id'], 'way/29177094')
        self.assertEqual(clean_data.validated_data['name'], 'Schlachthof Gärtringen')
        self.assertEqual(clean_data.validated_data['operator'], self.company)
        self.assertEqual(clean_data.validated_data['city'], 'Gärtringen')
        self.assertEqual(clean_data.validated_data['country_code'], 'DE')
        self.assertEqual(clean_data.validated_data['postal_code'], '12345')
        self.assertEqual(clean_data.validated_data['street'], 'Riedbrunnenstraße')
        self.assertEqual(clean_data.validated_data['street_number'], '5')
        self.assertEqual(clean_data.validated_data['coordinates'].x, 8.9190879)
        self.assertEqual(clean_data.validated_data['coordinates'].y, 48.6396181)

    def test_facility_serializer_invalid(self):
        messy_data = {
            'external_id': 'way/29177094  ',
            'name': '  Schlachthof Gärtringen',
            'city': 'Gärtringen',
            'country_code': 'de',
            # postal code too long to trigger Google's library
            'postal_code': '123456789',
            'street': 'Riedbrunnenstraße',
            'street_number': '5',
            'coordinates': 'SRID=4326;POINT(8.9190879 48.6396181)'
        }
        clean_data = FacilitySerializer(data=messy_data)
        self.assertFalse(clean_data.is_valid(), clean_data.errors)
        # shows that the lack of operator is not the issue
        self.assertIn('postal_code', clean_data.errors)

    def test_violation_serializer_valid(self):
        messy_data = {
            'date_observed': timezone.now().date(),
            'description': 'Failed stunning equipment.',
            'evidence_url': 'evidenceURL.com'
        }
        clean_data = ViolationSerializer(data=messy_data)
        self.assertTrue(clean_data.is_valid(), clean_data.errors)
        self.assertEqual(
            clean_data.validated_data['date_observed'], timezone.now().date()
        )
        self.assertEqual(
            clean_data.validated_data['description'], 'Failed stunning equipment.'
        )
        self.assertEqual(
            clean_data.validated_data['evidence_url'], 'https://evidenceurl.com'
        )

    def test_violation_serializer_invalid_date(self):
        messy_data = {
            'date_observed': timezone.now().date() + timedelta(days=2),
            'description': 'Failed stunning equipment.',
            'evidence_url': 'evidenceURL.com'
        }
        clean_data = ViolationSerializer(data=messy_data)
        self.assertFalse(clean_data.is_valid(), clean_data.errors)
        # to show the problem is the date, not the website formatting
        self.assertIn('date_observed', clean_data.errors)

    def test_tracker_serializer_valid(self):
        messy_data = {
            'company': {
                'name': '  Schlachthof eG   ',
                'website': 'companyWEB.com'
            },

            'facility': {
                'external_id': 'way/29177094  ',
                'name': '  Schlachthof Gärtringen',
                'city': 'Gärtringen',
                'country_code': 'de',
                'postal_code': '12345',
                'street': 'Riedbrunnenstraße',
                'street_number': '5',
                'coordinates': 'SRID=4326;POINT(8.9190879 48.6396181)'
            }
        }
        clean_data = TrackerSerializer(data=messy_data)
        self.assertTrue(clean_data.is_valid(), clean_data.errors)
        # saving to trigger the function create()
        created_objects = clean_data.save()
        # extract instances
        company = created_objects['company']
        facility = created_objects['facility']
        # check company is created and sanitized
        self.assertIsInstance(company, Company)
        self.assertEqual(company.name, 'Schlachthof eG')
        self.assertEqual(company.website, 'https://companyweb.com')
        # check facility is created and sanitized
        self.assertIsInstance(facility, Facility)
        self.assertEqual(facility.external_id, 'way/29177094')
        self.assertEqual(facility.name, 'Schlachthof Gärtringen')
        self.assertEqual(facility.city, 'Gärtringen')
        self.assertEqual(facility.country_code, 'DE')
        self.assertEqual(facility.postal_code, '12345')
        self.assertEqual(facility.street, 'Riedbrunnenstraße')
        self.assertEqual(facility.street_number, '5')
        self.assertEqual(facility.coordinates.x, 8.9190879)
        self.assertEqual(facility.coordinates.y, 48.6396181)

    def test_tracker_serializer_invalid(self):
        messy_data = {
            'company': {
                'name': '  Schlachthof eG   ',
                'website': 'companyWEB.com'
            },

            'facility': {
                'external_id': 'way/29177094  ',
                'name': '  Schlachthof Gärtringen',
                'city': 'Gärtringen',
                'country_code': 'de',
                # postal code too long to trigger Google's library
                'postal_code': '123456789',
                'street': 'Riedbrunnenstraße',
                'street_number': '5',
                'coordinates': 'SRID=4326;POINT(8.9190879 48.6396181)'
            }
        }
        clean_data = TrackerSerializer(data=messy_data)
        self.assertFalse(clean_data.is_valid(), clean_data.errors)
        # make sure that it is invalid because of the facility postal code
        self.assertIn('facility', clean_data.errors)
