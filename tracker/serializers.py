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
            'id',
            'name',
            'website'
        ]
        read_only_fields = ['id']

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
            'id',
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
        read_only_fields = ['id']

        extra_kwargs = {
            'operator': {'required': False, 'allow_null': True}
        }

    def validate(self, data):
        '''
        Sanitize the input data and use Google's i18n database
        to validate the address components.
        It works also if the method is PATCH and UPDATE, not only PUT.
        '''
        data = strip_all_strings(data)
        if 'country_code' in data:
            data['country_code'] = upper_country_code(data['country_code'])

        existing_facility = self.instance
        street = data.get('street') or getattr(existing_facility, 'street', '')
        street_number = data.get('street_number') or getattr(
            existing_facility, 'street_number', ''
        )
        # combine street name and number to validate,
        # but keep it separate for clean data structure
        full_address = f'{street} {street_number}'

        city = data.get('city') or getattr(existing_facility, 'city', '')
        country_code = data.get('country_code') or getattr(
            existing_facility, 'country_code', ''
        )
        postal_code = data.get('postal_code') or getattr(
            existing_facility, 'postal_code', ''
        )

        address_data = {
            'city': city,
            'country_code': country_code,
            'postal_code': postal_code,
            'street_address': full_address
        }

        if country_code and city:
            try:
                # validate the address using the google library
                normalized_data = normalize_address(address_data)

                # only keep canonical values for country code and postal code
                # preserve the original street and city capitalization
                if 'country_code' in data or not existing_facility:
                    data['country_code'] = normalized_data['country_code']
                if 'postal_code' in data or not existing_facility:
                    data['postal_code'] = normalized_data['postal_code']

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
            'id',
            'facility',
            'date_observed',
            'description',
            'evidence_url',
            'evidence_file'
        ]
        read_only_fields = ['id']

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

    def create(self, validated_data):
        company_data = validated_data.pop('company')
        facility_data = validated_data.pop('facility')

        company = Company.objects.create(**company_data)
        facility = Facility.objects.create(operator=company, **facility_data)

        return {
            'company': company,
            'facility': facility
        }

    def update(self, instance, validated_data):
        company_data = validated_data.pop('company', None)
        facility_data = validated_data.pop('facility', None)

        # it gets the 'facility' object if it exists, otherwise None to prevent errors
        facility_instance = getattr(
            instance, 'facility', instance.get('facility')
            if isinstance(instance, dict) else instance
        )
        # checks if there is company data with which to update the db record,
        # and if there is a db at all to handle edge cases
        company_instance = getattr(facility_instance, 'operator', None)

        if company_data and company_instance:
            # which record is updated, with what, and that is a PATCH method
            company_serializer = CompanySerializer(
                company_instance, data=company_data, partial=True
            )
            # if it is invalid, raise a 400 Bad Request error
            company_serializer.is_valid(raise_exception=True)
            company_instance = company_serializer.save()

        if facility_data and facility_instance:
            facility_serializer = FacilitySerializer(
                facility_instance, data=facility_data, partial=True
            )
            facility_serializer.is_valid(raise_exception=True)
            facility_instance = facility_serializer.save()

        return {
            'company': company_instance,
            'facility': facility_instance
        }
