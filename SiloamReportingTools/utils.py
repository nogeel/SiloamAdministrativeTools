import csv, pdb
from datetime import datetime
from django.db.models import Q
from django.db import transaction, reset_queries
from .models import Language, Homeland, Ethnicity, VisitType, VisitStatus, Patient, EventType, Event, ProviderName, \
    Visit, PatientDemographics, InsuranceType, ProcedureCode

UNKNOWN = "UNKNOWN"
UNKNOWN_DATE = "1/1/1900"

APPT_DATE = "appt_date"  # Appointment Date
VISIT_TYPE = "visit_type"
VISIT_STATUS = "visit_status"
PROVIDER = "provider"
PATIENT_ID = "patient_id"
VISIT_ID = "visit_id"
PT_DOB = "pt_dob"  # Patient Date of Birth
ZIP = "zip"    # Not imported
ETHNICITY = "ethnicity"
HOMELAND = "homeland"
LANGUAGE = "language"


INPUT_DATE_FORMAT = "%m/%d/%Y"  # Format it comes from PrimeSuite As
OUTPUT_DATE_FORMAT = "%Y-%m-%d"  # Format expected by django models.DateField()

IGNORE_HEADERS = True
TEST_DATA = (51886, 52784, 1002)  # Minnie Mouse, Donald Duck, and Tony Tiger


def load_demo_file_data(file_path, error_log=True):
    """
    File that contain demographic and visit data csv file from PrimeSuite and call the relevant functions
    for processing
    """
    #Grab Data from Existing CSV file
    #TODO Double check you are handling the fail correctly (how you want)
    f = open(file_path, 'rt')
    try:
        reader = csv.reader(f, dialect='excel-tab')

        counter = 1

        if IGNORE_HEADERS:
            reader.next()

        for row in reader:
            #Pull individual data in dictionary for passing to various methods
            data = {}

            data[APPT_DATE] = strip_and_replace_blank(row[0], is_date=True)

            data[VISIT_TYPE] = strip_and_replace_blank(row[1])
            data[VISIT_STATUS] = strip_and_replace_blank(row[2])
            data[PROVIDER] = strip_and_replace_blank(row[3])
            data[PATIENT_ID] = strip_and_replace_blank(row[4])
            data[VISIT_ID] = strip_and_replace_blank(row[5])

            data[PT_DOB] = strip_and_replace_blank(row[6], is_date=True)

            data[ZIP] = strip_and_replace_blank(row[7])
            data[ETHNICITY] = strip_and_replace_blank(row[8])
            data[HOMELAND] = strip_and_replace_blank(row[9])
            data[LANGUAGE] = strip_and_replace_blank(row[10])

            if data[PATIENT_ID] not in TEST_DATA:
                #Ensure the language, homeland, ethnicity, visit_type, visit_status are already in the system
                setup_data_load(data, error_log)

                #Load Patient Data
                load_patient_data(data)

                #Load Visit Data
                load_visit_data(data)
                data = None

            reset_queries()
            print counter
            counter = counter + 1


    #TODO: Handle exceptions better
    finally:
        pass

    pass


def log_error(ev_type, message, file_line=None, raw_data=None):
    EventType.objects.get_or_create(event_type=ev_type)
    evt = EventType.objects.get(event_type=ev_type)

    Event.objects.create(event_type=evt, message=message, file_line=file_line, raw_data=raw_data)


def setup_data_load(defined_values, error_log=False):
    """ Ensures that Homeland, Language, Ethnicity, Visit_Type, and Visit_Status
    are already in the the system. If error_log is True then is records in the error table
    that a new option has been added.

    """
    try:
        Language.objects.get(language=defined_values[LANGUAGE])
        Homeland.objects.get(homeland=defined_values[HOMELAND])
        Ethnicity.objects.get(ethnicity=defined_values[ETHNICITY])
        VisitType.objects.get(visit_type=defined_values[VISIT_TYPE])
        VisitStatus.objects.get(visit_status=defined_values[VISIT_STATUS])
        ProviderName.objects.get(provider_name=defined_values[PROVIDER])

    except Language.DoesNotExist:
        Language.objects.create(language=defined_values[LANGUAGE])
        if error_log:
            log_error(ev_type="New Language", message="%s was added to Languages" % defined_values[LANGUAGE],
                      raw_data=defined_values[LANGUAGE])
        setup_data_load(defined_values, error_log)

    except Homeland.DoesNotExist:
        Homeland.objects.create(homeland=defined_values[HOMELAND])
        if error_log:
            log_error(ev_type="New Homeland", message="%s was added to Homeland" % defined_values[HOMELAND],
                      raw_data=defined_values[HOMELAND])
        setup_data_load(defined_values, error_log)

    except Ethnicity.DoesNotExist:
        Ethnicity.objects.create(ethnicity=defined_values[ETHNICITY])
        if error_log:
            log_error(ev_type="New Ethnicity", message="%s was added to Ethnicities" % defined_values[ETHNICITY],
                      raw_data=defined_values[ETHNICITY])
        setup_data_load(defined_values, error_log)

    except VisitType.DoesNotExist:
        VisitType.objects.create(visit_type=defined_values[VISIT_TYPE])
        if error_log:
            log_error(ev_type="New Visit Type", message="%s was added to Visit Types" % defined_values[VISIT_TYPE],
                      raw_data=defined_values[VISIT_TYPE])
        setup_data_load(defined_values, error_log)

    except VisitStatus.DoesNotExist:
        VisitStatus.objects.create(visit_status=defined_values[VISIT_STATUS])
        if error_log:
            log_error(ev_type="New Visit Status", message="%s was added to Languages" % defined_values[LANGUAGE],
                      raw_data=defined_values[LANGUAGE])
        setup_data_load(defined_values, error_log)

    except ProviderName.DoesNotExist:
        ProviderName.objects.create(provider_name=defined_values[PROVIDER])
        #Always log a ProviderName being added so they can be linked to a Provider
        log_error(ev_type="New Provider Name",
                  message="%s was added to Provider Names. Manually link to a Provider" % defined_values[PROVIDER],
                  raw_data=defined_values[PROVIDER])
        setup_data_load(defined_values, error_log)


def load_patient_data(defined_values):
    try:
        pt, created = Patient.objects.get_or_create(patient_id=defined_values[PATIENT_ID])

        p = PatientDemographics.objects.get(patient=pt, active_record=True)

        #assert(defined_values[PATIENT_ID] == p.patient_id)

        temp_date = datetime.date(datetime.strptime(defined_values[APPT_DATE], OUTPUT_DATE_FORMAT))

        if p.visit_date < temp_date:
            #If the visit_date is more recent then current row

            save_and_deactivate_patient_demo(p, defined_values)
        elif p.visit_date == temp_date and equal_patient_data(p, defined_values):
            #Ignore cases where the data is already in the system
            pass
        else:
            #Save the record for historical purposes
            save_inactive_patient_record(defined_values)

    except PatientDemographics.DoesNotExist:
        #Create new record
        h = Homeland.objects.get(homeland=defined_values[HOMELAND])
        e = Ethnicity.objects.get(ethnicity=defined_values[ETHNICITY])
        l = Language.objects.get(language=defined_values[LANGUAGE])
        pt_dob = defined_values[PT_DOB]
        lv = defined_values[APPT_DATE]

        p = PatientDemographics.objects.create(active_record=True, patient=pt, dob=pt_dob, homeland=h, ethnicity=e,
                                               language=l, visit_date=lv)

        p.save()

    except PatientDemographics.MultipleObjectsReturned:
        #This error should never not occur. If it does loop through records and find the correct active one

        p = PatientDemographics.objects.filter(patient=pt, active_record=True)

        current_latest = None

        for active_record in p:
            if current_latest is None:
                current_latest = active_record
                #TODO Handle Equality?
            else:
                if current_latest.visit_date < active_record.visit_date:
                    current_latest.active_record = False
                    current_latest.save()
                    current_latest = active_record
                else:
                    active_record.active_record = False
                    active_record.save()
                    #re-run method after fixing the multiple active records problem

        load_patient_data(defined_values)


def load_visit_data(defined_values):
    #TODO Add Logging
    pt, create = Patient.objects.get_or_create(patient_id=defined_values[PATIENT_ID])
    vt, create = VisitType.objects.get_or_create(visit_type=defined_values[VISIT_TYPE])
    vs, create = VisitStatus.objects.get_or_create(visit_status=defined_values[VISIT_STATUS])
    prov, create = ProviderName.objects.get_or_create(provider_name=defined_values[PROVIDER])

    #ignore duplicates
    vs = Visit.objects.filter(visit_id=defined_values[VISIT_ID], patient=pt, visit_type=vt, visit_status=vs,
                             visit_date=defined_values[APPT_DATE], provider_name=prov)

    if vs.count is not 0:
        pass
    else:

        #Handle Those with UNKNOWN visit_id
        if defined_values[VISIT_ID] == UNKNOWN:
            #Visit_created with False
            Visit.objects.create(visit_id=defined_values[VISIT_ID], patient=pt, visit_type=vt, visit_status=vs,
                                 visit_date=defined_values[APPT_DATE], provider_name=prov, primary_visit=False)

        else:
            #Grab all objects with the current visit id
            visits = Visit.objects.filter(visit_id=defined_values[VISIT_ID])
            cnt = visits.count()

            #Create visit if not already loaded
            if cnt == 0:
                Visit.objects.create(visit_id=defined_values[VISIT_ID], patient=pt, visit_type=vt, visit_status=vs,
                                    visit_date=defined_values[APPT_DATE], provider_name=prov, primary_visit=True)
            else:

                Visit.objects.create(visit_id=defined_values[VISIT_ID], patient=pt, visit_type=vt, visit_status=vs,
                                visit_date=defined_values[APPT_DATE], provider_name=prov)

                handle_multiple_visits(defined_values[VISIT_ID])



def strip_and_replace_blank(some_text, is_date=False):
    """Clean incoming value and handle blank text

    some_text -- Text or Data to be Cleaned
    is_date -- Boolean indication whether the UNKNOWN date text should be use or not.
    """
    some_text = some_text.strip()
    if some_text == "":
        if is_date:
            some_text = UNKNOWN_DATE

        else:
            some_text = UNKNOWN

    if is_date:
        temp = datetime.strptime(some_text, INPUT_DATE_FORMAT)
        some_text = datetime.strftime(temp, OUTPUT_DATE_FORMAT)

    return some_text


def has_ssn(some_text):
    """
    To prevent storing actual SSNs the function returns true or false based on if there is text
    in the string or not.
    """
    if some_text == "":
        return False
    else:
        return True


@transaction.commit_on_success
def save_and_deactivate_patient_demo(patient_demo, defined_values):
    """ Creates a new updated active record and makes the previous record inactive
        Pre-condition: patient.patient_id == defined_values[PATIENT_ID]
    """

    #assert(defined_values[PATIENT_ID] == patient.patient_id)

    h = Homeland.objects.get(homeland=defined_values[HOMELAND])
    e = Ethnicity.objects.get(ethnicity=defined_values[ETHNICITY])
    l = Language.objects.get(language=defined_values[LANGUAGE])
    pt_dob = defined_values[PT_DOB]
    lv = defined_values[APPT_DATE]
    vcd = lv
    pt = Patient.objects.get(patient_id=defined_values[PATIENT_ID])

    patient_demo.active_record = False
    patient_demo.save()

    p = PatientDemographics(active_record=True, patient=pt, dob=pt_dob, homeland=h, ethnicity=e,
                            language=l, visit_date=vcd)
    p.save()


def equal_patient_data(patient, defined_values):
    """Evaluates to see if the dictionary contains the same patient information
    in the ethnicity, homeland, language and DOB fields.
    Pre-condition: Assumes Patient_ID are equal between patient and defined values
    """

    temp_date = datetime.date(datetime.strptime(defined_values[PT_DOB], OUTPUT_DATE_FORMAT))

    if patient.homeland.homeland == defined_values[HOMELAND] \
        and patient.ethnicity.ethnicity == defined_values[ETHNICITY] \
        and patient.language.language == defined_values[LANGUAGE] \
        and patient.dob == temp_date:
        return True
    else:
        return False


def equal_visit_data(visit, defined_values):
    #temp_date = datetime.date(datetime.strptime(defined_values[APPT_DATE], OUTPUT_DATE_FORMAT))

    if visit.visit_id == defined_values[VISIT_ID] \
        and visit.patient.patient_id == defined_values[PATIENT_ID] \
        and visit.visit_type.visit_type == defined_values[VISIT_TYPE] \
        and visit.visit_status.visit_status == defined_values[VISIT_STATUS] \
        and visit.provider_name.provider_name == defined_values[PROVIDER] \
        and visit.visit_date == defined_values[APPT_DATE]:
            return True
    else:
        return False


def save_inactive_patient_record(defined_values):
    pt = Patient.objects.get(patient_id=defined_values[PATIENT_ID])
    h = Homeland.objects.get(homeland=defined_values[HOMELAND])
    e = Ethnicity.objects.get(ethnicity=defined_values[ETHNICITY])
    l = Language.objects.get(language=defined_values[LANGUAGE])
    pt_dob = defined_values[PT_DOB]
    lv = defined_values[APPT_DATE]
    vcd = lv

    PatientDemographics.objects.get_or_create(active_record=False, patient=pt, dob=pt_dob, homeland=h, ethnicity=e,
                                              language=l, visit_date=vcd)


def add_insurance(visit_id, insurance, event_log=False):
    ins, created = InsuranceType.objects.get_or_create(insurance_type=insurance)
    if created and event_log:
        log_error(ev_type="New Insurance Type", message="%s was added to Insurance Type" % insurance,
                  raw_data="Visit_ID: %s\tInsuranceType: %s" % (visit_id, insurance))

    v = Visit.objects.get(visit_id=visit_id)
    v.insurance_type = ins
    v.save()


def load_procedure_file(file_path, error_log=True):
    f = open(file_path, 'rt')
    try:
        reader = csv.reader(f, dialect='excel-tab')

        if IGNORE_HEADERS:
            reader.next()

        for row in reader:
            patient_id = strip_and_replace_blank(row[0])
            visit_id = strip_and_replace_blank(row[1])
            proc = strip_and_replace_blank(row[2])
            alt_proc = strip_and_replace_blank(row[3])

            load_procedure_code(patient_id, visit_id, proc, alt_proc)

    finally:
        pass


def load_procedure_code(patient_id, visit_id, proc, alt_proc):
    #Pull individual data in dictionary for passing to various methods
    data = {}

    try:
        vis = Visit.objects.get(visit_id=visit_id)

        if vis.patient_id not in TEST_DATA:
            proc, created = ProcedureCode.objects.get_or_create(code=proc, alt_code=alt_proc)

            vis.procedures.add(proc)
            vis.save()

    except Visit.DoesNotExist:
        print "Visit %s was not found" % visit_id

    except Visit.MultipleObjectsReturned:
        handle_multiple_visits(visit_id)
        load_procedure_code(patient_id=patient_id, visit_id=visit_id, proc=proc, alt_proc=alt_proc)


def load_extra_data_file(file_path, error_log=True):
    f = open(file_path, 'rt')
    try:
        reader = csv.reader(f, dialect='excel-tab')

        if IGNORE_HEADERS:
            reader.next()

        for row in reader:
            patient_id = strip_and_replace_blank(row[0])
            visit_id = strip_and_replace_blank(row[1])
            app_date = strip_and_replace_blank(row[2], is_date=True)
            insurance = strip_and_replace_blank(row[3])
            gender = strip_and_replace_blank(row[4])
            race = strip_and_replace_blank(row[5])
            ethnicity = strip_and_replace_blank(row[6])
            ssn_status = has_ssn(row[7])
            zip = strip_and_replace_blank(row[8])

    finally:
        pass


def handle_multiple_visits(visit_id):

    visits = Visit.objects.filter(visit_id=visit_id)

    total_visits_w_id = visits.count()
    #It looks for Staff Medical Visits.
    staff_visit_count = visits.filter(provider_name__provider__staff_provider=True,
                                      provider_name__provider__medical_provider=True).count()


    if total_visits_w_id == 0:
        visits[0].primary_visit = True
        visits[0].save()

    elif not total_visits_w_id > 2:

        #Case 0 - No Staff Providers - Choose the earlier one
        if staff_visit_count == 0:
            med_count = visits.filter(provider_name__provider__staff_provider=False,
                                      provider_name__provider__medical_provider=True).count()
            #No Staff or Medical
            if med_count == 0:
                set_most_recent_visit_to_true(visits)

            #Medical, but no staff
            else:
                set_most_recent_visit_to_true(visits.filter(provider_name__provider__medical_provider=True))
                no_med = visits.filter(provider_name__provider__medical_provider=False)
                if no_med.count() is not 0:
                    set_all_primary_visit_false(no_med)

        #Has at least 1 Staff Appointment
        elif staff_visit_count > 0:
            set_most_recent_visit_to_true(visits.filter(provider_name__provider__staff_provider=True))
            set_all_primary_visit_false(visits.filter(provider_name__provider__staff_provider=False))


def set_most_recent_visit_to_true(visits):
    #Set most recent created visit as primary.
    visits = visits.order_by('-created_date')
    most_recent = visits[0]
    if not most_recent.primary_visit:
        most_recent.primary_visit = True
        most_recent.save()
    for visit in visits[1:]:
        if visit.primary_visit:
            visit.primary_visit = False
            visit.save()


def set_all_primary_visit_false(visits):

    for visit in visits:
        if visit.primary_visit is not False:
            visit.primary_visit = False
            visit.save()