import copy
from datetime import datetime
from .utils import strip_and_replace_blank, equal_patient_data, save_and_deactivate_patient_demo, load_patient_data, \
    save_inactive_patient_record, log_error, setup_data_load, load_visit_data, add_insurance, equal_visit_data
from .utils import HOMELAND, ETHNICITY, LANGUAGE, APPT_DATE, PT_DOB, PATIENT_ID, UNKNOWN, OUTPUT_DATE_FORMAT, \
    VISIT_TYPE, VISIT_STATUS, PROVIDER, VISIT_ID, handle_multiple_visits, \
    set_most_recent_visit_to_true, set_all_primary_visit_false
from .models import Patient, Ethnicity, Language, Homeland, Event, VisitStatus, VisitType, EventType, ProviderName, \
    Provider, Visit, PatientDemographics, InsuranceType

from django.test import TestCase


class TestTextCleaner(TestCase):
    def test_strip_and_replace_blank_date(self):
        """ Strip and replace blanks removes leading and trailing whitespace and fills in
        blank values with a defined unknown for both text and dates.
        """
        input_date = '\t1/2/1998 '
        output_date = '1998-01-02'
        #Assumes the Input Unknown Date is 1/1/1900
        output_unknown_date = '1900-01-01'
        input_text = ' Some Form of Text\t'
        output_text = 'Some Form of Text'

        #Test normal date with leading tab and trailing space
        result = strip_and_replace_blank(input_date, is_date=True)
        self.assertEqual(output_date, result)

        #Test blank date filled with unknown date
        result = strip_and_replace_blank('', is_date=True)
        self.assertEqual(output_unknown_date, result)

        #Test normal text with leading space and tailing tab
        result = strip_and_replace_blank(input_text)
        self.assertEqual(output_text, result)

        #Test Blank Text filled with value for UNKNOWN
        result = strip_and_replace_blank('')
        self.assertEqual(UNKNOWN, result)


class EqualPatientDataTest(TestCase):
    """Test to Make sure the equal patient

    """

    def setUp(self):
        self.data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                     PT_DOB: "1970-04-20", APPT_DATE: "2012-1-2"}

        #Builds the object in Django
        self.e = Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        self.assertEqual(Ethnicity.objects.filter(ethnicity=self.data[ETHNICITY]).count(), 1)
        self.l = Language.objects.create(language=self.data[LANGUAGE])
        self.h = Homeland.objects.create(homeland=self.data[HOMELAND])
        self.p = Patient.objects.create(patient_id=self.data[PATIENT_ID])

        PatientDemographics(active_record=True, patient=self.p, dob=self.data[PT_DOB], homeland=self.h,
                            ethnicity=self.e,
                            language=self.l, visit_date=self.data[APPT_DATE]).save()

        self.p = PatientDemographics.objects.get()

    def test_equal_patient_demographics(self):
        """ Patient demographic data is equal (Homeland, Ethnicity, Language, PT_DOB
        """
        #Make sure they are equal
        self.assertTrue(equal_patient_data(self.p, self.data))

    def test_not_equal_homeland(self):
        # Test to make sure the method catches any changes between each of the fields.
        # Resets Back to original values
        self.data[HOMELAND] = "Gibberish"
        self.assertFalse(equal_patient_data(self.p, self.data))

    def test_not_equal_language(self):
        self.data[LANGUAGE] = "NotTheSame"
        self.assertFalse(equal_patient_data(self.p, self.data))

    def test_not_equal_ethnicity(self):
        self.data[ETHNICITY] = "Gibberish"
        self.assertFalse(equal_patient_data(self.p, self.data))

    def test_not_equal_dob(self):
        self.data[PT_DOB] = "1983-3-30"
        self.assertFalse(equal_patient_data(self.p, self.data))


class TestLoadPatientData(TestCase):
    def test_load_patient_data_patient_not_found_exception(self):
        data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2"}

        Homeland.objects.get_or_create(homeland=data[HOMELAND])
        Language.objects.get_or_create(language=data[LANGUAGE])
        Ethnicity.objects.get_or_create(ethnicity=data[ETHNICITY])
        Patient.objects.get_or_create(patient_id=data[PATIENT_ID])

        self.assertEqual(PatientDemographics.objects.all().count(), 0)
        #Test Patient Does not exist
        load_patient_data(data)
        self.assertEqual(PatientDemographics.objects.all().count(), 1)
        pt, _ = Patient.objects.get_or_create(patient_id=data[PATIENT_ID])
        p = PatientDemographics.objects.get(patient=pt)

        #self.assertTrue(equal_patient_data(p, data))
        temp = datetime.date(datetime.strptime(data[PT_DOB], OUTPUT_DATE_FORMAT))
        self.assertEqual(p.dob, temp)
        temp = datetime.date(datetime.strptime(data[APPT_DATE], OUTPUT_DATE_FORMAT))
        self.assertEqual(p.visit_date, temp)


    def test_load_patient_data_multiple_retrieved_exception(self):
        #Test Multiple Patients returned

        self.assertEquals(Patient.objects.all().count(), 0)

        # Create Case 1
        data1 = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                 PT_DOB: "1958-4-25", APPT_DATE: "2012-1-2"}

        h = Homeland.objects.create(homeland=data1[HOMELAND])
        l = Language.objects.create(language=data1[LANGUAGE])
        e = Ethnicity.objects.create(ethnicity=data1[ETHNICITY])

        p1 = PatientDemographics.objects.create(active_record=True, patient_id=data1[PATIENT_ID], dob=data1[PT_DOB],
                                                homeland=h,
                                                ethnicity=e, language=l, visit_date=data1[APPT_DATE])

        self.assertEquals(PatientDemographics.objects.all().count(), 1)

        # Create Case 2
        data2 = copy.deepcopy(data1)
        data2[APPT_DATE] = "2012-3-1"

        p2 = PatientDemographics.objects.create(active_record=True, patient_id=data2[PATIENT_ID], dob=data2[PT_DOB],
                                                homeland=h,
                                                ethnicity=e, language=l, visit_date=data2[APPT_DATE])

        self.assertEquals(PatientDemographics.objects.all().count(), 2)
        self.assertEquals(PatientDemographics.objects.filter(patient_id="1234", active_record=True).count(), 2)

        #Create a third case to run through the algorithm.
        data3 = copy.deepcopy(data1)
        data3[APPT_DATE] = "2012-8-5"
        self.assertEqual(data3[PATIENT_ID], p1.patient_id)
        self.assertEqual(data3[PATIENT_ID], p2.patient_id)

        load_patient_data(data3)
        self.assertEquals(PatientDemographics.objects.all().count(), 3)
        self.assertEquals(Patient.objects.filter(patient_id="1234").count(), 1)
        pt = Patient.objects.get(patient_id="1234")
        r_res = PatientDemographics.objects.get(patient=pt, active_record=True)
        self.assertEqual(r_res.visit_date, datetime.date(datetime.strptime(data3[APPT_DATE], OUTPUT_DATE_FORMAT)))

    def test_load_patient_data_normal_case(self):
        from SiloamReportingTools.utils import HOMELAND, ETHNICITY, LANGUAGE, APPT_DATE, PT_DOB, PATIENT_ID

        data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                PT_DOB: "1981-3-20", APPT_DATE: "2012-1-3"}

        Homeland.objects.create(homeland=data[HOMELAND])
        Language.objects.create(language=data[LANGUAGE])
        Ethnicity.objects.create(ethnicity=data[ETHNICITY])

        self.assertEquals(PatientDemographics.objects.all().count(), 0)
        load_patient_data(data)
        self.assertEquals(PatientDemographics.objects.all().count(), 1)

        # Case where new data is newer than the current Active Record
        temp_data = copy.deepcopy(data)
        temp_data[APPT_DATE] = "2013-1-4"
        load_patient_data(temp_data)
        self.assertEquals(PatientDemographics.objects.all().count(), 2)
        self.assertEqual(PatientDemographics.objects.filter(active_record=True).count(), 1)
        p = PatientDemographics.objects.get(active_record=True)
        date = datetime.date(datetime.strptime(temp_data[APPT_DATE], OUTPUT_DATE_FORMAT))
        self.assertEqual(p.visit_date, date)
        p.delete()
        self.assertEquals(PatientDemographics.objects.all().count(), 1)
        p = PatientDemographics.objects.all()
        p.delete()
        self.assertEquals(PatientDemographics.objects.all().count(), 0)

        # Case where they are equal (no change)
        load_patient_data(data)
        self.assertEquals(Patient.objects.all().count(), 1)
        p = PatientDemographics.objects.get(active_record=True)
        self.assertTrue(equal_patient_data(p, data))
        load_patient_data(data)
        self.assertEquals(PatientDemographics.objects.all().count(), 1)
        self.assertEqual(PatientDemographics.objects.filter(active_record=True).count(), 1)

        # Case where new data is older than the active record
        temp_data = copy.deepcopy(data)
        temp_data[APPT_DATE] = "2013-1-2"
        load_patient_data(temp_data)
        self.assertEquals(PatientDemographics.objects.all().count(), 2)
        self.assertEqual(PatientDemographics.objects.filter(active_record=True).count(), 1)


class TestOtherUtils(TestCase):
    def setUp(self):
        self.data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234", \
                     PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2"}

        self.eth1 = Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        self.l = Language.objects.create(language=self.data[LANGUAGE])
        self.h = Homeland.objects.create(homeland=self.data[HOMELAND])
        self.pt = Patient.objects.create(patient_id=self.data[PATIENT_ID])
        #self.pt = Patient.objects.get(patient_id=self.data[PATIENT_ID])
        self.pt_dob = self.data[PT_DOB]
        self.lv = self.data[APPT_DATE]
        self.vcd = self.lv

    def test_save_and_deactivate_patient_demo(self):
        p = PatientDemographics(active_record=True, patient=self.pt, dob=self.pt_dob, homeland=self.h,
                                ethnicity=self.eth1,
                                language=self.l, visit_date=self.vcd)
        p.save()

        self.data[ETHNICITY] = 'Another_Eth'
        self.data[APPT_DATE] = '2013-1-2'

        eth2 = Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        self.assertEqual(PatientDemographics.objects.filter(active_record=True, ethnicity=self.eth1).count(), 1)

        save_and_deactivate_patient_demo(p, self.data)

        self.assertEqual(PatientDemographics.objects.filter(active_record=True, ethnicity=eth2).count(), 1)
        self.assertEqual(PatientDemographics.objects.filter(active_record=False, ethnicity=self.eth1).count(), 1)
        self.assertEqual(PatientDemographics.objects.all().count(), 2)

        #Make sure the two records are different
        p1 = PatientDemographics.objects.get(active_record=True, ethnicity=eth2)
        p2 = PatientDemographics.objects.get(active_record=False, ethnicity=self.eth1)
        self.assertFalse(p1.equal_patient_object_data(p2))

    def test_save_and_equal_case(self):
        load_patient_data(self.data)
        p = PatientDemographics.objects.get(active_record=True)
        self.assertTrue(equal_patient_data(p, self.data))


class TestInactivePatient(TestCase):
    def setUp(self):
        self.data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                     PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2"}

        e = Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        l = Language.objects.create(language=self.data[LANGUAGE])
        h = Homeland.objects.create(homeland=self.data[HOMELAND])
        p_id = self.data[PATIENT_ID]
        pt_dob = self.data[PT_DOB]
        lv = self.data[APPT_DATE]
        vcd = lv
        pt = Patient.objects.create(patient_id=self.data[PATIENT_ID])


        #Primary object
        self.p = PatientDemographics(active_record=False, patient=pt, dob=pt_dob, homeland=h, ethnicity=e,
                                     language=l, visit_date=vcd)
        self.p.save()

    def test_duplicate_inactive_data(self):
        self.assertEqual(PatientDemographics.objects.filter(active_record=False).count(), 1)
        save_inactive_patient_record(self.data)
        self.assertEqual(PatientDemographics.objects.filter(active_record=False).count(), 1)

    def test_new_inactive_data(self):
        self.assertEqual(PatientDemographics.objects.filter(active_record=False).count(), 1)
        other_home = Homeland.objects.create(homeland="Another Homeland")
        self.data[HOMELAND] = other_home
        save_inactive_patient_record(self.data)
        self.assertEqual(PatientDemographics.objects.filter(active_record=False).count(), 2)


class TestSetupLoadData(TestCase):
    def setUp(self):
        self.data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                     PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2", VISIT_STATUS: "Happened", VISIT_TYPE: "Some Type",
                     PROVIDER: "Dr. Strong"}

        Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        Language.objects.create(language=self.data[LANGUAGE])
        Homeland.objects.create(homeland=self.data[HOMELAND])
        VisitStatus.objects.create(visit_status=self.data[VISIT_STATUS])
        VisitType.objects.create(visit_type=self.data[VISIT_TYPE])
        ProviderName.objects.create(provider_name=self.data[PROVIDER])


    def test_missing_language(self):
        l = Language.objects.get(language=self.data[LANGUAGE])
        l.delete()
        self.assertEqual(Language.objects.filter(language=self.data[LANGUAGE]).count(), 0)
        setup_data_load(self.data, error_log=False)
        self.assertEqual(Language.objects.filter(language=self.data[LANGUAGE]).count(), 1)


        #Test the error type too
        l = Language.objects.get(language=self.data[LANGUAGE])
        l.delete()
        self.assertEqual(Language.objects.filter(language=self.data[LANGUAGE]).count(), 0)
        setup_data_load(self.data, error_log=True)
        self.assertEqual(Language.objects.filter(language=self.data[LANGUAGE]).count(), 1)


class TestErrorLogger(TestCase):
    def test_load_event(self):
        self.assertEquals(Event.objects.all().count(), 0)
        language = "Tokututu"
        log_error("New Language", "%s was added to Languages" % language, 2345, "Tokututu")
        self.assertEqual(EventType.objects.filter(event_type="New Language").count(), 1)
        self.assertEqual(Event.objects.all().count(), 1)


class TestPatient(TestCase):
    def setUp(self):
        data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2"}

        e = Ethnicity.objects.create(ethnicity=data[ETHNICITY])
        l = Language.objects.create(language=data[LANGUAGE])
        h = Homeland.objects.create(homeland=data[HOMELAND])
        pt = Patient.objects.create(patient_id=data[PATIENT_ID])
        pt_dob = data[PT_DOB]
        lv = data[APPT_DATE]
        vcd = lv



        #Primary object to be compared to
        self.p = PatientDemographics(active_record=True, patient=pt, dob=pt_dob, homeland=h, ethnicity=e,
                                     language=l, visit_date=vcd)
        self.p.save()

        #Object that is modified
        self.p2 = PatientDemographics(active_record=True, patient=pt, dob=pt_dob, homeland=h, ethnicity=e,
                                      language=l, visit_date=vcd)
        self.p2.save()

    def test_equal_patient_objects(self):
        self.assertTrue(self.p.equal_patient_object_data(self.p2))

    def test_not_equal_homeland(self):
        #Change each of the of the values to ensure it fails when compared to the primary case
        self.p2.homeland = Homeland.objects.create(homeland="Gibberish")
        self.p2.save()
        self.assertFalse(self.p.equal_patient_object_data(self.p2))

    def test_not_equal_language(self):
        self.p2.language = Language.objects.create(language="Test_Home_Other")
        self.p2.save()
        self.assertFalse(self.p.equal_patient_object_data(self.p2))

    def test_not_equal_ethnicity(self):
        self.p2.ethnicity = Ethnicity.objects.create(ethnicity="Gibberish")
        self.p2.save()
        self.assertFalse(self.p.equal_patient_object_data(self.p2))

    def test_not_equal_dob(self):
        self.p2.dob = "1957-10-8"
        self.p2.save()
        self.assertFalse(self.p.equal_patient_object_data(self.p2))


class TestLoadVisitData(TestCase):
    def setUp(self):
        self.data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                     PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2", VISIT_STATUS: "Happened", VISIT_TYPE: "Some Type",
                     PROVIDER: "Dr. Strong", VISIT_ID: "123456749"}

        e = Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        l = Language.objects.create(language=self.data[LANGUAGE])
        h = Homeland.objects.create(homeland=self.data[HOMELAND])
        VisitStatus.objects.create(visit_status=self.data[VISIT_STATUS])
        VisitType.objects.create(visit_type=self.data[VISIT_TYPE])
        ProviderName.objects.create(provider_name=self.data[PROVIDER])

        pt = Patient.objects.create(patient_id=self.data[PATIENT_ID])

        PatientDemographics.objects.create(ethnicity=e, language=l, homeland=h, patient=pt, dob=self.data[PT_DOB],
                                           visit_date=self.data[APPT_DATE], active_record=True)

    def test_add_new_visit(self):
        self.assertEquals(Visit.objects.all().count(), 0)
        load_visit_data(self.data)
        self.assertEquals(Visit.objects.all().count(), 1)

    def test_add_duplicate_visit(self):
        self.assertEquals(Visit.objects.all().count(), 0)
        load_visit_data(self.data)
        self.assertEquals(Visit.objects.all().count(), 1)
        load_visit_data(self.data)
        self.assertEquals(Visit.objects.all().count(), 1)


class TestPatientCreation(TestCase):
    def setUp(self):
        self.data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                     PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2", VISIT_STATUS: "Happened", VISIT_TYPE: "Some Type",
                     PROVIDER: "Dr. Strong", VISIT_ID: "123456749"}

        e = Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        l = Language.objects.create(language=self.data[LANGUAGE])
        h = Homeland.objects.create(homeland=self.data[HOMELAND])
        VisitStatus.objects.create(visit_status=self.data[VISIT_STATUS])
        VisitType.objects.create(visit_type=self.data[VISIT_TYPE])
        ProviderName.objects.create(provider_name=self.data[PROVIDER])

    def create_new_patient(self):
        self.assertEqual(Patient.objects.all().count(), 0)
        self.assertEqual(PatientDemographics.objects.all().count(), 1)
        load_patient_data(self.data)
        self.assertEqual(Patient.objects.all().count(), 1)
        self.assertEqual(PatientDemographics.objects.all().count(), 1)


class TestLoadingInsuranceData(TestCase):
    def setUp(self):
        self.data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                     PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2", VISIT_STATUS: "Happened", VISIT_TYPE: "Some Type",
                     PROVIDER: "Dr. Strong", VISIT_ID: "123456749"}

        e = Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        l = Language.objects.create(language=self.data[LANGUAGE])
        h = Homeland.objects.create(homeland=self.data[HOMELAND])
        vs = VisitStatus.objects.create(visit_status=self.data[VISIT_STATUS])
        vt = VisitType.objects.create(visit_type=self.data[VISIT_TYPE])
        pr = ProviderName.objects.create(provider_name=self.data[PROVIDER])

        pt = Patient.objects.create(patient_id=self.data[PATIENT_ID])

        PatientDemographics.objects.create(ethnicity=e, language=l, homeland=h, patient=pt, dob=self.data[PT_DOB],
                                           visit_date=self.data[APPT_DATE], active_record=True)
        self.v = Visit.objects.create(visit_date=self.data[APPT_DATE], visit_id=self.data[VISIT_ID], patient=pt,
                                      visit_type=vt, visit_status=vs, provider_name=pr)

    def test_add_insurance_type(self):
        self.assertEqual(InsuranceType.objects.all().count(), 0)
        add_insurance(self.data[VISIT_ID], 'SomeInsurance')
        self.assertEqual(InsuranceType.objects.all().count(), 1)

        # def test_add_insurance_to_visit_data(self):
        #     self.assertEqual(self.v.insurance_type, None)
        #     add_insurance(self.data[VISIT_ID], 'SomeInsurance')
        #     ins = InsuranceType.objects.get(insurance_type='SomeInsurance')
        #     v = Visit.objects.get(visit_id=self.data[VISIT_ID])
        #     self.assertEqual(v.insurance_type, ins)


class TestMultipleVisitsReturned(TestCase):
    def setUp(self):
        self.data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "51886",
                     PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2", VISIT_STATUS: "Happened", VISIT_TYPE: "Some Type",
                     PROVIDER: "Dr. Strong", VISIT_ID: "123456749"}

        e = Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        l = Language.objects.create(language=self.data[LANGUAGE])
        h = Homeland.objects.create(homeland=self.data[HOMELAND])
        vs = VisitStatus.objects.create(visit_status=self.data[VISIT_STATUS])
        vt = VisitType.objects.create(visit_type=self.data[VISIT_TYPE])
        prov = Provider.objects.create(name=self.data[PROVIDER], staff_provider=True, medical_provider=True)
        pr = ProviderName.objects.create(provider_name=self.data[PROVIDER], provider=prov)

        pt = Patient.objects.create(patient_id=self.data[PATIENT_ID])

        PatientDemographics.objects.create(ethnicity=e, language=l, homeland=h, patient=pt, dob=self.data[PT_DOB],
                                           visit_date=self.data[APPT_DATE], active_record=True)

        self.v = Visit.objects.create(visit_date=self.data[APPT_DATE], visit_id=self.data[VISIT_ID], patient=pt,
                                      visit_type=vt, visit_status=vs, provider_name=pr)

        self.prov2 = Provider.objects.create(name="Luke Skywalker", staff_provider=True, medical_provider=True)
        pr2 = ProviderName.objects.create(provider_name="Douglas P. Mann", provider=self.prov2)

        self.v2 = Visit.objects.create(visit_date="2011-3-1", visit_id=self.data[VISIT_ID], patient=pt,
                                       visit_type=vt, visit_status=vs, provider_name=pr2)

        self.prov3 = Provider.objects.create(name="Juan Valdez", staff_provider=True, medical_provider=True)
        pr3 = ProviderName.objects.create(provider_name="Juan Valdez", provider=self.prov3)

        self.v3 = Visit.objects.create(visit_date="2013-4-1", visit_id=self.data[VISIT_ID], patient=pt,
                                       visit_type=vt, visit_status=vs, provider_name=pr2)

    def test_one_visit_staff_medical(self):
        self.v2.delete()

        self.v.primary_visit = True
        self.v.save()

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 0)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)

        handle_multiple_visits(visit_id=self.data[VISIT_ID])

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 0)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)

        self.v.primary_visit = False
        self.v.save()

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 1)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 0)

        handle_multiple_visits(visit_id=self.data[VISIT_ID])

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 0)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)

    def test_one_staff_provider(self):
        self.assertTrue(False)
        self.v.primary_visit = True
        self.v.save()

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 2)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)

        handle_multiple_visits(visit_id=self.data[VISIT_ID])

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 2)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)

        self.v.primary_visit = False
        self.v.save()

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 1)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 0)

        handle_multiple_visits(visit_id=self.data[VISIT_ID])

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 0)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)


    def test_two_staff_providers(self):
        self.assertTrue(False)

    def test_all_staff_providers(self):
        self.assertTrue(False)






class TestVisitEquality(TestCase):
    def setUp(self):
        self.data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "51886",
                     PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2", VISIT_STATUS: "Happened", VISIT_TYPE: "Some Type",
                     PROVIDER: "Dr. Strong", VISIT_ID: "123456749"}

        e = Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        l = Language.objects.create(language=self.data[LANGUAGE])
        h = Homeland.objects.create(homeland=self.data[HOMELAND])
        vs = VisitStatus.objects.create(visit_status=self.data[VISIT_STATUS])
        vt = VisitType.objects.create(visit_type=self.data[VISIT_TYPE])
        prov = Provider.objects.create(name=self.data[PROVIDER], staff_provider=True, medical_provider=True)
        pr = ProviderName.objects.create(provider_name=self.data[PROVIDER], provider=prov)

        pt = Patient.objects.create(patient_id=self.data[PATIENT_ID])

        PatientDemographics.objects.create(ethnicity=e, language=l, homeland=h, patient=pt, dob=self.data[PT_DOB],
                                           visit_date=self.data[APPT_DATE], active_record=True)

        self.v = Visit.objects.create(visit_date=self.data[APPT_DATE], visit_id=self.data[VISIT_ID], patient=pt,
                                      visit_type=vt, visit_status=vs, provider_name=pr)

    def test_equal_visits(self):
        self.assertTrue(equal_visit_data(self.v, self.data))

    def test_not_equal_visit_date(self):
        self.assertTrue(equal_visit_data(self.v, self.data))
        self.v.visit_date = '2011-1-5'
        self.v.save()

        self.assertFalse(equal_visit_data(self.v, self.data))

    def test_not_equal_visit_id(self):
        self.assertTrue(equal_visit_data(self.v, self.data))

        self.v.visit_id = self.data[VISIT_ID][::-1]
        self.v.save()

        self.assertFalse(equal_visit_data(self.v, self.data))

    def test_not_equal_patient(self):
        self.assertTrue(equal_visit_data(self.v, self.data))

        rev_id = self.data[PATIENT_ID][::-1]
        pt = Patient.objects.create(patient_id=rev_id)
        self.v.patient = pt
        self.v.save()

        self.assertFalse(equal_visit_data(self.v, self.data))

    def test_not_equal_visit_type(self):
        self.assertTrue(equal_visit_data(self.v, self.data))

        temp_vt = self.data[VISIT_TYPE][::-1]
        vt = VisitType.objects.create(visit_type=temp_vt)
        self.v.visit_type = vt
        self.v.save()

        self.assertFalse(equal_visit_data(self.v, self.data))

    def test_not_equal_visit_status(self):
        self.assertTrue(equal_visit_data(self.v, self.data))

        temp_vs = self.data[VISIT_STATUS][::-1]
        vs = VisitStatus.objects.create(visit_status=temp_vs)
        self.v.visit_status = vs
        self.v.save()

        self.assertFalse(equal_visit_data(self.v, self.data))

    def test_not_equal_provider_name(self):
        self.assertTrue(equal_visit_data(self.v, self.data))

        temp_prov_nm = self.data[PROVIDER][::-1]
        vs = ProviderName.objects.create(provider_name=temp_prov_nm)
        self.v.provider_name = vs
        self.v.save()

        self.assertFalse(equal_visit_data(self.v, self.data))


class TestAllVisitsFalse(TestCase):
    def setUp(self):
        self.data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "51886",
                     PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2", VISIT_STATUS: "Happened", VISIT_TYPE: "Some Type",
                     PROVIDER: "Dr. Strong", VISIT_ID: "123456749"}

        e = Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        l = Language.objects.create(language=self.data[LANGUAGE])
        h = Homeland.objects.create(homeland=self.data[HOMELAND])
        vs = VisitStatus.objects.create(visit_status=self.data[VISIT_STATUS])
        vt = VisitType.objects.create(visit_type=self.data[VISIT_TYPE])
        prov = Provider.objects.create(name=self.data[PROVIDER], staff_provider=True, medical_provider=True)
        pr = ProviderName.objects.create(provider_name=self.data[PROVIDER], provider=prov)

        pt = Patient.objects.create(patient_id=self.data[PATIENT_ID])

        PatientDemographics.objects.create(ethnicity=e, language=l, homeland=h, patient=pt, dob=self.data[PT_DOB],
                                           visit_date=self.data[APPT_DATE], active_record=True)

        self.v = Visit.objects.create(visit_date=self.data[APPT_DATE], visit_id=self.data[VISIT_ID], patient=pt,
                                      visit_type=vt, visit_status=vs, provider_name=pr, primary_visit=True)

        self.two = Visit.objects.get(visit_id=self.data[VISIT_ID])
        self.two.pk = None
        self.two.primary_visit = False
        self.two.save()

        self.three = Visit.objects.filter(visit_id=self.data[VISIT_ID])[0]
        self.three.pk = None
        self.three.primary_visit = False
        self.three.save()

    def test_one_true(self):
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 2)

        set_all_primary_visit_false(Visit.objects.filter(visit_id=self.data[VISIT_ID]))

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 0)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 3)

    def test_one_false(self):
        self.two.primary_visit = True
        self.two.save()

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 2)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 1)

        set_all_primary_visit_false(Visit.objects.filter(visit_id=self.data[VISIT_ID]))

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 0)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 3)

    def test_all_true(self):
        self.two.primary_visit = True
        self.two.save()

        self.three.primary_visit = True
        self.three.save()

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 3)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 0)

        set_all_primary_visit_false(Visit.objects.filter(visit_id=self.data[VISIT_ID]))

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 0)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 3)

    def test_all_false(self):
        self.v.primary_visit = False
        self.v.save()

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 0)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 3)

        set_all_primary_visit_false(Visit.objects.filter(visit_id=self.data[VISIT_ID]))

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 0)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 3)



class TestSetMostRecentVisitToTrue(TestCase):
    def setUp(self):
        self.data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "51886",
                     PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2", VISIT_STATUS: "Happened", VISIT_TYPE: "Some Type",
                     PROVIDER: "Dr. Strong", VISIT_ID: "123456749"}

        e = Ethnicity.objects.create(ethnicity=self.data[ETHNICITY])
        l = Language.objects.create(language=self.data[LANGUAGE])
        h = Homeland.objects.create(homeland=self.data[HOMELAND])
        vs = VisitStatus.objects.create(visit_status=self.data[VISIT_STATUS])
        vt = VisitType.objects.create(visit_type=self.data[VISIT_TYPE])
        prov = Provider.objects.create(name=self.data[PROVIDER], staff_provider=True, medical_provider=True)
        pr = ProviderName.objects.create(provider_name=self.data[PROVIDER], provider=prov)

        pt = Patient.objects.create(patient_id=self.data[PATIENT_ID])

        PatientDemographics.objects.create(ethnicity=e, language=l, homeland=h, patient=pt, dob=self.data[PT_DOB],
                                           visit_date=self.data[APPT_DATE], active_record=True)

        self.v = Visit.objects.create(visit_date=self.data[APPT_DATE], visit_id=self.data[VISIT_ID], patient=pt,
                                      visit_type=vt, visit_status=vs, provider_name=pr, primary_visit=True)

        self.v.created_date = "2012-1-2"
        self.v.save()

        self.two = Visit.objects.get(visit_id=self.data[VISIT_ID])
        self.two.pk = None
        self.two.primary_visit = False
        self.two.created_date = '2011-6-8'
        self.two.save()

        self.three = Visit.objects.filter(visit_id=self.data[VISIT_ID])[0]
        self.three.pk = None
        self.three.primary_visit = False
        self.three.created_date = '2013-6-8'
        self.three.save()

    def test_none_section(self):
        self.two.delete()
        self.three.delete()
        self.v.primary_visit = False
        self.v.save()
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 1)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 0)

        set_most_recent_visit_to_true(Visit.objects.filter(visit_id=self.data[VISIT_ID]))

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 0)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)

        self.assertTrue( Visit.objects.get(visit_id=self.data[VISIT_ID], created_date=self.data[APPT_DATE]))

    def test_elif_section_two(self):
        self.three.delete()

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 1)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)

        set_most_recent_visit_to_true(Visit.objects.filter(visit_id=self.data[VISIT_ID]))

        self.assertTrue(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2012-1-2").primary_visit)
        self.assertFalse(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2011-6-8").primary_visit)

    def test_elif_section_three(self):
        self.three.created_date = "1991-1-9"
        self.three.save()

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 2)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)

        set_most_recent_visit_to_true(Visit.objects.filter(visit_id=self.data[VISIT_ID]))

        self.assertTrue(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2012-1-2").primary_visit)
        self.assertFalse(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2011-6-8").primary_visit)
        self.assertFalse(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="1991-1-9").primary_visit)

    def test_else_section_two(self):
        self.two.delete()

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 1)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)

        self.assertTrue(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2012-1-2").primary_visit)
        self.assertFalse(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2013-6-8").primary_visit)

        set_most_recent_visit_to_true(Visit.objects.filter(visit_id=self.data[VISIT_ID]))

        self.assertFalse(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2012-1-2").primary_visit)
        self.assertTrue(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2013-6-8").primary_visit)

    def test_else_section_three(self):

        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=False).count(), 2)
        self.assertEqual(Visit.objects.filter(visit_id=self.data[VISIT_ID], primary_visit=True).count(), 1)

        self.assertTrue(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2012-1-2").primary_visit)
        self.assertFalse(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2011-6-8").primary_visit)
        self.assertFalse(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2013-6-8").primary_visit)

        set_most_recent_visit_to_true(Visit.objects.filter(visit_id=self.data[VISIT_ID]))

        self.assertFalse(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2012-1-2").primary_visit)
        self.assertFalse(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2011-6-8").primary_visit)
        self.assertTrue(Visit.objects.get(visit_id=self.data[VISIT_ID], created_date="2013-6-8").primary_visit)








