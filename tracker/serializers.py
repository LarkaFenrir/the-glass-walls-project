from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from tracker.models import Facility, Company, Violation
from i18naddress import normalize_address, InvalidAddressError
from tracker.sanitizers import strip_all_strings, clean_website_url, upper_country_code
from django.utils import timezone

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            'name',
            'website'
        ]

    def to_internal_value(self, data):
        '''
        It overrides a built-in Django REST framework to validate an URL that
        does not have a protocol prefix.
        '''
        # the QueryDict that from the HTTP request has a copy attr
        # the else statement is for my tests
        data = data.copy() if hasattr(data, 'copy') else data
        # if there is the 'website' key and it's not empty,
        # it cleans the url
        if 'website' in data and data['website']:
            data['website'] = clean_website_url(data['website'])
        # it validates with the built-in method of Django-REST framework again
        return super().to_internal_value(data)

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

        extra_kwargs = {
            'operator': {'required': False, 'allow_null': True}
        }

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

        extra_kwargs = {
            'facility': {'required': False, 'allow_null': True}
        }

    def validate_date_observed(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("The date cannot be in the future.")
        return value

    def to_internal_value(self, data):
        data = data.copy() if hasattr(data, 'copy') else data
        if 'evidence_url' in data and data['evidence_url']:
            data['evidence_url'] = clean_website_url(data['evidence_url'])
        return super().to_internal_value(data)

class TrackerSerializer(serializers.Serializer):

    company = CompanySerializer()
    facility = FacilitySerializer()
    violation = ViolationSerializer(required=False, allow_null=True)

    def create(self, validated_data):
        company_data = validated_data.pop('company')
        facility_data = validated_data.pop('facility')
        violation_data = validated_data.pop('violation', None)

        company = Company.objects.create(**company_data)
        facility = Facility.objects.create(operator=company, **facility_data)

        violation = None   # in case no violation is given, no error thrown
        if violation_data:
            violation = Violation.objects.create(facility=facility, **violation_data)

        return {
            'company': company,
            'facility': facility,
            'violation': violation
        }
