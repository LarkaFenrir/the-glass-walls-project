from django.test import TestCase
from django.contrib.gis.geos import Point
from ..models import Facility, Company, Violation
from django.utils import timezone

class TrackerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.company = Company.objects.create(
            name='Schlachthof eG'
        )

        cls.facility = Facility.objects.create(
            external_id='way/29177094',
            name='Schlachthof Gärtringen',
            operator=cls.company,
            city='Gärtringen',
            country='DE',
            postcode='71116',
            street='Riedbrunnenstraße',
            street_number='5',
            coordinates=Point(8.9190879, 48.6396181)
        )

        cls.violation = Violation.objects.create(
            facility=cls.facility,
            date_observed=timezone.now(),
            description='Failed stunning equipment.'
        )

    def test_company_creation(self):
        '''
        Test the creation of the company, and the associated facilities.
        '''
        self.assertEqual(self.company.name, 'Schlachthof eG')
        self.assertEqual(self.company.facilities.count(), 1)
        self.assertEqual(self.company.facilities.first().name, 'Schlachthof Gärtringen')

    def test_facility_creation(self):
        self.assertEqual(self.facility.name, 'Schlachthof Gärtringen')
        self.assertEqual(self.facility.operator.name, 'Schlachthof eG')
        self.assertEqual(self.facility.coordinates.x, 8.9190879)

    def test_violation_creation(self):
        self.assertEqual(self.violation.facility.name, 'Schlachthof Gärtringen')
        self.assertEqual(self.violation.description, 'Failed stunning equipment.')

    def test_str_representation(self):
        self.assertEqual(str(self.facility), 'Schlachthof Gärtringen (Gärtringen)')
        self.assertEqual(str(self.company), 'Schlachthof eG')
        self.assertEqual(
            str(self.violation),
            f'Violation at Schlachthof Gärtringen ({self.violation.date_observed})'
        )
