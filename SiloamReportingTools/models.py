from django.db import models
from django_extensions.db import fields

MONTHS = ['January', "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]


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
    patient_id = models.IntegerField(primary_key=True)
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()


class PatientDemographics(models.Model):
    patient = models.ForeignKey(Patient)
    dob = models.DateField()
    ethnicity = models.ForeignKey(Ethnicity)
    homeland = models.ForeignKey(Homeland)
    language = models.ForeignKey(Language)
    visit_date = models.DateField()
    active_record = models.BooleanField()
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()

    def equal_patient_object_data(self, patient):
        """
        Pre-condition: Assumes Patient ID are Equal
        """
        if patient.homeland.homeland == self.homeland.homeland\
           and patient.ethnicity.ethnicity == self.ethnicity.ethnicity\
           and patient.language.language == self.language.language\
           and patient.dob == self.dob:
            return True
        else:
            return False


class VisitTypeClass(models.Model):
    visit_type_class = models.CharField(max_length=255)
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()

    def __unicode__(self):
        return self.visit_type_class


class VisitType(models.Model):
    visit_type = models.CharField(max_length=255)
    visit_type_class = models.ForeignKey(VisitTypeClass, null=True)
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


class Provider(models.Model):
    name = models.CharField(max_length=255)
    staff_provider = models.BooleanField()
    medical_provider = models.BooleanField()
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()

    def __unicode__(self):
        return u'%s' % self.name

    def no_show_count(self, year, month=None, medical_provider=None, staff_provider=None, all_encounters=None):
        return self.visit_status_counts_by_provider('Patient No-Show', year=year, month=month,
                                                    medical_provider=medical_provider, staff_provider=staff_provider,
                                                    all_encounters=all_encounters)

    def complete_visits(self, year, month=None, medical_provider=None, staff_provider=None, all_encounters=None):
        return self.visit_status_counts_by_provider('Complete', year=year, month=month,
                                                    medical_provider=medical_provider, staff_provider=staff_provider,
                                                    all_encounters=all_encounters)

    def workin_count(self, year, month=None, medical_provider=None, staff_provider=None, all_encounters=None):
        return self.visit_type_complete_counts_by_provider('Work In', year=year, month=month,
                                                           medical_provider=medical_provider,
                                                           staff_provider=staff_provider, all_encounters=all_encounters)

    def complete_appointments(self, year, month=None, medical_provider=None, staff_provider=None, all_encounters=None):

        v = Visit.objects.all()

        if medical_provider and staff_provider:
            v = v.filter(provider_name__provider__staff_provider=True, provider_name__provider__medical_provider=True)
        elif medical_provider:
            v = v.filter(provider_name__provider__medical_provider=True)
        elif staff_provider:
            v = v.filter(provider_name__provider__staff_provider=True)
        elif all_encounters:
            pass  # Use all Objects
        else:
            v = v.filter(provider_name__provider__name=self.name)

        v = v.filter(visit_status__visit_status='Complete', visit_date__year=year).exclude(visit_type__visit_type='Work In')

        status_count = {}
        if month is not None:
            status_count[month] = v.filter(visit_date__month=month).count()
        else:
            for month_number, name in enumerate(MONTHS):
                #iterate over each month
                status_count[name] = v.filter(visit_date__month=(month_number+1)).count()

        return status_count

    def no_show_rate(self, year, month=None, medical_provider=None, staff_provider=None, all_encounters=None):
        complete = self.complete_appointments(year=year, month=month, medical_provider=medical_provider,
                                              staff_provider=staff_provider, all_encounters=all_encounters)
        no_show  = self.visit_status_counts_by_provider('Patient No-Show', year=year, month=month,
                                                        medical_provider=medical_provider,
                                                        staff_provider=staff_provider, all_encounters=all_encounters)

        no_show_rate = {}

        for key in complete:
            if no_show[key]+complete[key] is not 0:
                no_show_rate[key] = float(no_show[key])/(no_show[key]+complete[key])
            else:
                no_show_rate[key] = None

        return no_show_rate

    def papsmear_count(self, year, month=None, medical_provider=None, staff_provider=None, all_encounters=None):
            return self.visit_type_complete_counts_by_provider('Pap Smear', year=year, month=month,
                                                               medical_provider=medical_provider,
                                                               staff_provider=staff_provider,
                                                               all_encounters=all_encounters)

    def ref_part_2_count(self, year, month=None, medical_provider=None, staff_provider=None, all_encounters=None):
        return self.visit_type_complete_counts_by_provider('Refugee P2', year=year, month=month,
                                                           medical_provider=medical_provider,
                                                           staff_provider=staff_provider, all_encounters=all_encounters)

    def patient_rescheduled_count(self, year, month=None, medical_provider=None, staff_provider=None,
                                  all_encounters=None):
        return self.visit_status_counts_by_provider('Patient Rescheduled', year=year, month=month,
                                                    medical_provider=medical_provider, staff_provider=staff_provider,
                                                    all_encounters=all_encounters)

    def office_rescheduled_count(self, year, month=None, medical_provider=None, staff_provider=None,
                                 all_encounters=None):
        return self.visit_status_counts_by_provider('Office Rescheduled', year=year, month=month,
                                                    medical_provider=medical_provider, staff_provider=staff_provider,
                                                    all_encounters=all_encounters)

    def patient_canceled_count(self, year, month=None, medical_provider=None, staff_provider=None, all_encounters=None):
            return self.visit_status_counts_by_provider('Patient Canceled', year=year, month=month,
                                                        medical_provider=medical_provider,
                                                        staff_provider=staff_provider, all_encounters=all_encounters)

    def office_canceled_count(self, year, month=None, medical_provider=None, staff_provider=None, all_encounters=None):
        return self.visit_status_counts_by_provider('Office Canceled', year=year, month=month,
                                                    medical_provider=medical_provider, staff_provider=staff_provider,
                                                    all_encounters=all_encounters)

    def visit_status_counts_by_provider(self, status, year, month=None, medical_provider=False, staff_provider=False,
                                        all_encounters=None):


        v = Visit.objects.all()

        if medical_provider and staff_provider:
            v = v.filter(provider_name__provider__staff_provider=True, provider_name__provider__medical_provider=True)
        elif medical_provider:
            v = v.filter(provider_name__provider__medical_provider=True)
        elif staff_provider:
            v = v.filter(provider_name__provider__staff_provider=True)
        elif all_encounters:
            pass  # leave as objects.all() since count all encounters
        else:
            v = v.filter(provider_name__provider__name=self.name)

        v = v.filter(visit_status__visit_status=status, visit_date__year=year)

        status_count = {}
        if month is not None:
            status_count[month] = v.filter(visit_date__month=month).count()
        else:
            for month_number, name in enumerate(MONTHS):
                #iterate over each month
                status_count[name] = v.filter(visit_date__month=(month_number+1)).count()

        return status_count

    def visit_type_complete_counts_by_provider(self, type,  year, month=None, medical_provider=None,
                                               staff_provider=None, all_encounters=None):
        return self.visit_type_counts_by_provider(type, 'Complete', year, month, medical_provider=medical_provider,
                                                  staff_provider=staff_provider, all_encounters=all_encounters)

    def visit_type_counts_by_provider(self, type, status,  year, month=None, medical_provider=False,
                                      staff_provider=False, all_encounters=None):

        v = Visit.objects.all()

        if medical_provider and staff_provider:
            v = v.filter(provider_name__provider__staff_provider=True, provider_name__provider__medical_provider=True)
        elif medical_provider:
            v = v.filter(provider_name__provider__medical_provider=True)
        elif staff_provider:
            v = v.filter(provider_name__provider__staff_provider=True)
        elif all_encounters:
            pass  # Leave it as Visit.Objects.all()
        else:
            v = Visit.objects.filter(provider_name__provider__name=self.name)

        v = v.filter(visit_date__year=year, visit_type__visit_type=type, visit_status__visit_status=status)

        status_count = {}
        if month is not None:
            status_count[month] = v.filter(visit_date__month=month).count()
        else:
            for month_number, name in enumerate(MONTHS):
                #iterate over each month
                status_count[name] = v.filter(visit_date__month=(month_number+1)).count()

        return status_count


class ProviderName(models.Model):
    provider_name = models.CharField(max_length=255)
    provider = models.ForeignKey(Provider, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.provider_name


class ProcedureCode(models.Model):
    code = models.CharField(max_length=255)
    alt_code = models.CharField(max_length=255)
    procedure_description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'%s:\t%s' % (self.procedure_code, self.procedure_description)


class Visit(models.Model):
    visit_date = models.DateField()
    visit_id = models.CharField(max_length=24)
    patient = models.ForeignKey(Patient)
    visit_type = models.ForeignKey(VisitType)
    visit_status = models.ForeignKey(VisitStatus)
    provider_name = models.ForeignKey(ProviderName)
    primary_visit = models.BooleanField()
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()



class EventType(models.Model):
    event_type = models.CharField(max_length=255)
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()


class Event(models.Model):
    event_type = models.ForeignKey(EventType)
    message = models.TextField()
    file_line = models.IntegerField(blank=True, null=True)
    raw_data = models.TextField(blank=True, null=True)
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()

    def __unicode__(self):
        return u'%s' % self.provider_name