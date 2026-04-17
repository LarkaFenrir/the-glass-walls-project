from django.contrib.gis import admin
from .models import Facility, Company, Violation

# Register your models here.

class ViolationInline(admin.TabularInline):
    model = Violation
    extra = 1
    fields = [
        'date_observed',
        'description',
        'evidence_url',
        'evidence_file'
    ]

@admin.register(Facility)
class FacilityAdmin(admin.GISModelAdmin):
    list_display = (
        'name',
        'operator',
        'city',
        'country',
        'postcode',
        'street'
    )
    search_fields = (
        'name',
        'operator__name',
        'city',
        'country',
        'postcode'
    )

    inlines = [ViolationInline]

admin.site.register(Company)
