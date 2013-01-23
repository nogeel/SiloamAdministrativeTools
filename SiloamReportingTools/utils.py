import csv
from datetime import datetime
from django.db import transaction
from .models import Language, Homeland, Ethnicity, VisitType, VisitStatus, Patient

UNKNOWN = "UNKNOWN"
UNKNOWN_DATE = "1/1/1900"

APPT_DATE = "appt_date" #Appointment Date
VISIT_TYPE = "visit_type"
VISIT_STATUS = "visit_status"
PROVIDER = "provider"
PATIENT_ID = "patient_id"
VISIT_ID = "visit_id"
PT_DOB = "pt_dob" #Patient Date of Birth
ZIP = "zip"
ETHNICITY = "ethnicity"
HOMELAND = "homeland"
LANGUAGE = "language"


INPUT_DATE_FORMAT = "%m/%d/%Y" #Format it comes from PrimeSuite As
OUTPUT_DATE_FORMAT = "%Y-%m-%d" #Format expected by django models.DateField()

IGNORE_HEADERS = True
TEST_DATA = (51886, 52784, 1002 ) #Minnie Mouse, Donald Duck, and Tony Tiger


def load_demo_file_data(file_path, error_log=True):

    #Grab Data from Existing CSV file
    #TODO Double check you are handling the fail correctly (how you want)
    f = open(file_path, 'rt')
    try:
        reader = csv.reader(f, dialect='excel-tab')

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


            #Ensure the language, homeland, ethnicity, visit_type, visit_status are already in the system
            setup_data_load(data, error_log)

            #Load Patient Data
            load_patient_data(data)

            #Load Visit Data
            data = None

    #TODO: Handle exceptions better
    finally:
        pass

    pass


def setup_data_load(defined_values, error_log):
    """ Ensures that Homeland, Language, Ethnicity, Visit_Type, and Visit_Status
    are already in the the system. If error_log is True then is records in the error table
    that a new option has been added.

    """
    #TODO Set up error model for later loads
    Language.objects.get_or_create(language=defined_values[LANGUAGE])
    Homeland.objects.get_or_create(homeland=defined_values[HOMELAND])
    Ethnicity.objects.get_or_create(ethnicity=defined_values[ETHNICITY])
    VisitType.objects.get_or_create(visit_type=defined_values[VISIT_TYPE])
    VisitStatus.objects.get_or_create(visit_status=defined_values[VISIT_STATUS])


def load_patient_data(defined_values):
    try:
        #See if patient already exist
        p = Patient.objects.get(patient_id=defined_values[PATIENT_ID], active_record=True)

        temp_date = datetime.date(datetime.strptime(defined_values[APPT_DATE], OUTPUT_DATE_FORMAT))


        if p.last_visit < temp_date:
            #If the visit_date is more recent then current row

            if equal_patient_data(p, defined_values):
                if p.visit_created_date <= temp_date:
                    #If the data is the same, just update the APPT_Date
                    p.last_visit = defined_values[APPT_DATE]
                    p.save()
            else:
            #If the data isn't the same create new record and deactivate current one
                save_and_deactivate_patient_demo(p, defined_values)

        else:
            #Save the record for historical purposes
            save_inactive_patient_record(defined_values)

    except Patient.DoesNotExist:
        #Create new record
        h = Homeland.objects.get(homeland=defined_values[HOMELAND])
        e = Ethnicity.objects.get(ethnicity=defined_values[ETHNICITY])
        l = Language.objects.get(language=defined_values[LANGUAGE])
        pt_dob = defined_values[PT_DOB]
        lv = defined_values[APPT_DATE]

        p = Patient(active_record=True, patient_id=defined_values[PATIENT_ID], dob=pt_dob, homeland=h, ethnicity=e,
            language=l, last_visit=lv)

        p.save()

    except Patient.MultipleObjectsReturned:
        #This error should not occur. If it does loop through records and find the correct active one
        p = Patient.objects.filter(patient_id=defined_values[PATIENT_ID], active_record=True)

        current_latest = None

        for active_record in p:
            if current_latest is None:
                current_latest = active_record
                #TODO Handle Equality?
            else:
                if current_latest.last_visit < active_record.last_visit:
                    current_latest.active_record = False
                    current_latest.save()
                    current_latest = active_record
                else:
                    active_record.active_record = False
                    active_record.save()
                    #re-run method after fixing the multiple active records problem
                    load_patient_data(defined_values)


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

@transaction.commit_on_success
def save_and_deactivate_patient_demo(patient, defined_values):
    """ Creates a new updated active record and makes the previous record inactive
        Pre-condition: patiend.patient_id == defined_values[PATIENT_ID]
    """

    assert(defined_values[PATIENT_ID] == patient.patient_id)

    h = Homeland.objects.get(homeland=defined_values[HOMELAND])
    e = Ethnicity.objects.get(ethnicity=defined_values[ETHNICITY])
    l = Language.objects.get(language=defined_values[LANGUAGE])
    pt_dob = defined_values[PT_DOB]
    lv = defined_values[APPT_DATE]
    vcd = lv

    patient.active_record = False
    patient.save()

    p = Patient(active_record=True, patient_id=defined_values[PATIENT_ID], dob=pt_dob, homeland=h, ethnicity=e,
        language=l, visit_date=vcd)
    p.save()

def equal_patient_data(patient, defined_values):
    """Evaluates to see if the dictionary contains the same patient information
    in the ethnicity, homeland, language and DOB fields.
    Pre-condition: Assumes Patient_ID are equal between patient and defined values
    """

    if patient.homeland.homeland == defined_values[HOMELAND]\
       and patient.ethnicity.ethnicity == defined_values[ETHNICITY]\
       and patient.language.language == defined_values[LANGUAGE] and \
       patient.dob == defined_values[PT_DOB]:
        return True
    else:
        return False

def save_inactive_patient_record(defined_values):

    h = Homeland.objects.get(homeland=defined_values[HOMELAND])
    e = Ethnicity.objects.get(ethnicity=defined_values[ETHNICITY])
    l = Language.objects.get(language=defined_values[LANGUAGE])
    pt_dob = defined_values[PT_DOB]
    lv = defined_values[APPT_DATE]

    old_records = Patient.objects.filter(patient_id=defined_values[PATIENT_ID], active_record=False)

    #If there aren't any old records for the patient.
    if not old_records:
        p = Patient(active_record=False, patient_id=defined_values[PATIENT_ID], dob=pt_dob, homeland=h, ethnicity=e,
        language=l, last_visit=lv, visit_created_date=lv)
        p.save()
    else:
        #Check for Overlap case

        #Check to change creation date

        #Check to update Last Visit date


        equal_data_records = []

        for record in old_records:
            if p.equal_patient_object_data(record):
                equal_data_records.append(record)