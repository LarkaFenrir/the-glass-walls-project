from django.contrib.gis.db import models

# Create your models here.

class Facility(models.Model):
    external_id = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    operator = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='facilities',
        null=True,
        blank=True
    )
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postcode = models.CharField(max_length=30, blank=True)
    street = models.CharField(max_length=255, blank=True)
    coordinates = models.PointField()

    class Meta:
        verbose_name_plural = 'facilities'

    def __str__(self):
        return f'{self.name} ({self.city})'

class Company(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=500, blank=True)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name

class Violation(models.Model):
    facility = models.ForeignKey(
        'Facility',
        on_delete=models.CASCADE,
        related_name='violations'
    )
    date_observed = models.DateField()
    description = models.TextField(blank=True)
    evidence_url = models.URLField(blank=True)
    evidence_file = models.FileField(
        upload_to='violations/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = 'violations'

    def __str__(self):
        return f'Violation at {self.facility.name} ({self.date_observed})'
