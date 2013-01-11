import csv
import sys
from SiloamReportingTools.models import Language, Homeland, Ethnicity, VisitType, VisitStatus

UNKNOWN= "UNKNOWN"


def setup_data_load(file_path):
    """
    Loads the Ancillary tables from data
    """

    #Ancillary Models to be Loaded first
    languages = set()
    homelands = set()
    ethnicities = set()
    visit_types = set()
    visit_statuses = set()

    #Grab Data from Existing CSV file
    #TODO Double check you are handling the fail correctly (how you want)
    f = open(file_path, 'rt')
    try:
        reader = csv.reader(f, dialect='excel-tab')

        #ignore headers
        reader.next()

        for row in reader:
            languages.add(row[10])
            homelands.add(row[9])
            ethnicities.add(row[8])
            visit_types.add(row[1])
            visit_statuses.add(row[2])

    finally:
        pass

    f.close()

    #Create Objects for each model
    #TODO Set up error model for later loads
    for lang in languages:
        temp = lang.strip()
        if lang == "":
            temp = UNKNOWN
        Language.objects.get_or_create(language=temp)

    for homeland in homelands:
        temp = homeland.strip()
        if homeland == "":
            temp = UNKNOWN
        Homeland.objects.get_or_create(homeland=temp)

    for ethnicity in ethnicities:
        temp = ethnicity.strip()
        if ethnicity == "":
            temp = UNKNOWN
        Ethnicity.objects.get_or_create(ethnicity=temp)

    for visit_type in visit_types:
        temp = visit_type.strip()
        if visit_type == "":
            temp = UNKNOWN
        VisitType.objects.get_or_create(visit_type=temp)

    for visit_status in visit_statuses:
        temp = visit_status.strip()
        if visit_status == "":
            temp = UNKNOWN
        VisitStatus.objects.get_or_create(visit_status=temp)

#def load_patient_data(file_path):
#
#    patient_demo_data = {}
#
#
#try:
#    f = open(file_path, 'rt')
#    reader = csv.reader(f, dialect='excel-tab')
#
#    #ignore headers
#    reader.next()
#
#    for row in reader:
#
#        language = row[10]
#        homelands = row[9]
#        ethnicities = row[8]
#finally:
#    pass
#
#f.close()






