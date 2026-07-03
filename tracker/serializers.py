from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from models import Facility, Company, Violation
from i18naddress import normalize_address, InvalidAddressError
from sanitizers import strip_all_strings, clean_website_url, upper_country_code
from django.utils import timezone

class FacilitySerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Facility
        geo_field = 'coordinates'
        fields = [
            'external_id',
            'name',
            'operator',
            'city',
            'country_code',
            'postal_code',
            'street',
            'street_number',
            'coordinates'
        ]

    def validate(self, data):
        '''
        Sanitize the input data and use Google's i18n database
        to validate the address components.
        '''
        # combine street name and number to validate,
        # but keep it separate for clean data structure
        data = strip_all_strings(data)
        if 'country_code' in data:
            data['country_code'] = upper_country_code(data['country_code'])
        full_address = f"{data.get('street')} {data.get('street_number')}"
        address_data = {
            'city': data.get('city'),
            'country_code': data.get('country_code'),
            'postal_code': data.get('postal_code'),
            'street_address': full_address
        }

        try:
            # after validating the street address it doesn't overwrite it
            normalized_data = normalize_address(address_data)
            data['city'] = normalized_data.get('city')
            data['country_code'] = normalized_data.get('country_code')
            data['postal_code'] = normalized_data.get('postal_code')

        except InvalidAddressError as e:
            errors = {}
            for field, error_code in e.errors.items():
                errors[field] = f'Invalid {field} for the selected country.'
            raise serializers.ValidationError(errors)

        return data

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            'name',
            'website'
        ]

    def validate_website(self, value):
        return clean_website_url(value)

class ViolationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Violation
        fields = [
            'facility',
            'date_observed',
            'description',
            'evidence_url',
            'evidence_file'
        ]

    def validate_date_observed(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("The date cannot be in the future.")
        return value

    def validate_evidence_url(self, value):
        return clean_website_url(value)
