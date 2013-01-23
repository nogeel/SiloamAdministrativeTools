from django.db import models
from django_extensions.db import fields

class Ethnicity(models.Model):
    ethnicity = models.CharField(max_length=255)
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()

    def __unicode__(self):
        return self.ethnicity

    class Meta:
        verbose_name_plural = "Ethnicities"
        ordering = ['ethnicity']


class Homeland(models.Model):
    homeland = models.CharField(max_length=255)
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()

    def __unicode__(self):
        return self.homeland

    class Meta:
        ordering = ['homeland']


class Language(models.Model):
    language = models.CharField(max_length=255)
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()

    def __unicode__(self):
        return self.language

    class Meta:
        ordering = ['language']

class Patient(models.Model):
    patient_id = models.IntegerField()
    dob = models.DateField()
    ethnicity = models.ForeignKey(Ethnicity)
    homeland = models.ForeignKey(Homeland)
    language = models.ForeignKey(Language)
    visit_date = models.DateField()
    active_record = models.BooleanField()
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()

    def equal_patient_object_data(self, patient):
        if patient.homeland.homeland == self.homeland.homeland\
           and patient.ethnicity.ethnicity == self.ethnicity.ethnicity\
           and patient.language.language == self.language.language and\
           patient.dob == self.dob:
            return True
        else:
            return False


class VisitType(models.Model):
    visit_type = models.CharField(max_length=255)
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()

    def __unicode__(self):
        return self.visit_type


class VisitStatus(models.Model):
    visit_status = models.CharField(max_length=255)
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()

    def __unicode__(self):
        return self.visit_status


class InsuranceType(models.Model):
    insurance_type = models.CharField(max_length=255)
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()


class Visit(models.Model):
    visit_id = models.IntegerField()
    patient = models.ForeignKey(Patient)
    visit_type = models.ForeignKey(VisitType)
    visit_status = models.ForeignKey(VisitStatus)
    insurance_type = models.ForeignKey(InsuranceType)
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()


class EventType(models.Model):
    event_type = models.CharField(max_length=255)


class Events(models.Model):
    event_type = models.ForeignKey(EventType)
    message = models.TextField()
    file_line = models.IntegerField(blank=True, null=True)
    raw_data = models.DateField(blank=True, null=True)