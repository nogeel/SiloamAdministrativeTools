import copy
from .utils import strip_and_replace_blank, equal_patient_data, save_and_deactivate_patient_demo, save_inactive_patient_record, UNKNOWN
from .models import Patient, Ethnicity, Language, Homeland


"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class TestUtils(TestCase):
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

        #Test Blank Text filled wiht value for UNKNOWN
        result = strip_and_replace_blank('')
        self.assertEqual(UNKNOWN, result)

    def test_equal_patient_data(self):
        """ Patient demographic data is equal (Homeland, Ethnicity, Language, PT_DOB

        """
        from SiloamReportingTools.utils import HOMELAND, ETHNICITY, LANGUAGE, APPT_DATE, PT_DOB, PATIENT_ID

        #Base copy for doing comparisons
        data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2"}

        #Builds the object in Django
        e = Ethnicity.objects.create(ethnicity=data[ETHNICITY])
        l = Language.objects.create(language=data[LANGUAGE])
        h = Homeland.objects.create(homeland=data[HOMELAND])
        p_id = data[PATIENT_ID]
        pt_dob = data[PT_DOB]
        lv = data[APPT_DATE]
        vcd = lv

        p = Patient(active_record=True, patient_id=p_id, dob=pt_dob, homeland=h, ethnicity=e,
            language=l,  visit_date=vcd)
        p.save()

        #Make sure they are equal
        self.assertTrue(equal_patient_data(p, data))

        # Test to make sure the method catches any changes between each of the fields.
        # Resets Back to original values
        otherData = copy.deepcopy(data)
        otherData[HOMELAND] = "Gibberish"
        self.assertFalse(equal_patient_data(p, otherData))

        otherData = copy.deepcopy(data)
        otherData[LANGUAGE] = ""
        self.assertFalse(equal_patient_data(p, otherData))

        otherData = copy.deepcopy(data)
        otherData[ETHNICITY] = "Gibberish"
        self.assertFalse(equal_patient_data(p, otherData))

        otherData = copy.deepcopy(data)
        otherData[PT_DOB] = "1983-3-30"
        self.assertFalse(equal_patient_data(p, otherData))

#    def test_save_inactive_patient_record(self):
#        #TODO make sure all cases are tested
#        from SiloamReportingTools.utils import HOMELAND, ETHNICITY, LANGUAGE, APPT_DATE, PT_DOB, PATIENT_ID
#
#        data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",\
#                PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2"}
#
#        e = Ethnicity.objects.create(ethnicity=data[ETHNICITY])
#        l = Language.objects.create(language=data[LANGUAGE])
#        h = Homeland.objects.create(homeland=data[HOMELAND])
#        p_id = data[PATIENT_ID]
#        pt_dob = data[PT_DOB]
#        lv = data[APPT_DATE]
#        vcd = lv
#
#        p1 = Patient(active_record=False, patient_id=p_id, dob=pt_dob, homeland=h, ethnicity=e,
#            language=l,  visit_date=vcd)
#        p1.save()
#
#        #Copy first patient and make a change to Ethnicity and appointment date
#        data2 = copy.deepcopy(data)
#        data2[ETHNICITY] = 'Alt_Eth'
#        data2[APPT_DATE] = "2012-6-1"
#
#        e = Ethnicity.objects.create(ethnicity=data2[ETHNICITY])
#        l = Language.objects.get(language=data[LANGUAGE])
#        h = Homeland.objects.get(homeland=data[HOMELAND])
#        p_id = data2[PATIENT_ID]
#        pt_dob = data2[PT_DOB]
#        lv = data2[APPT_DATE]
#        vcd = lv
#
#        p2 = Patient(active_record=False, patient_id=p_id, dob=pt_dob, homeland=h, ethnicity=e,
#            language=l, last_visit=lv, visit_created_date=vcd)
#        p2.save()
#
#        #Create a more recent copy of the base patient
#        data3 = copy.deepcopy(data)
#        data3[APPT_DATE] = '2013-1-2'
#        e = Ethnicity.objects.get(ethnicity=data[ETHNICITY])
#        lv = data3[APPT_DATE]
#
#        p3 = Patient(active_record=True, patient_id=p_id, dob=pt_dob, homeland=h, ethnicity=e,
#            language=l, last_visit=lv, visit_created_date=vcd)
#        p3.save()
#
#        #Make sure there are three records
#        self.assertEqual(Patient.objects.filter(patient_id=data[PATIENT_ID], active_record=False).count(), 2)
#        self.assertEqual(Patient.objects.filter(patient_id=data[PATIENT_ID], active_record=True).count(), 1)
#        self.assertTrue(p1.equal_patient_object_data(p3))
#
#        #Just Update the most recent record's visit date because they are the same
#        test_case_1 = copy.deepcopy(data)
#        test_case_1[APPT_DATE] = '2013-2-1'
#        save_inactive_patient_record(test_case_1)
#        self.assertEqual(p3.visit_created_date, "2013-1-2")
#        self.assertEqual(p3.last_visit, "2013-2-1")
#        self.assertTrue(equal_patient_data(p2, test_case_1))
#
#        #More Recent Visit of a Prior Case
#        test_case_2 = copy.deepcopy(data)
#        test_case_2[APPT_DATE] = "2013-5-1"
#        save_inactive_patient_record(test_case_2)
#        self.assertEqual(p1.last_visit, "2013-5-1")
#        self.assertEqual(p1.visit_created_date, "2013-1-2")



    def test_save_and_deactivate_patient_demo(self):
        from SiloamReportingTools.utils import HOMELAND, ETHNICITY, LANGUAGE, APPT_DATE, PT_DOB, PATIENT_ID

        data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2"}

        eth1 = Ethnicity.objects.create(ethnicity=data[ETHNICITY])
        l = Language.objects.create(language=data[LANGUAGE])
        h = Homeland.objects.create(homeland=data[HOMELAND])
        p_id = data[PATIENT_ID]
        pt_dob = data[PT_DOB]
        lv = data[APPT_DATE]
        vcd = lv

        p = Patient(active_record=True, patient_id=p_id, dob=pt_dob, homeland=h, ethnicity=eth1,
            language=l,  visit_date=vcd)
        p.save()

        data[ETHNICITY] = 'Another_Eth'
        data[APPT_DATE] = '2013-1-2'

        eth2 = Ethnicity.objects.create(ethnicity=data[ETHNICITY])
        self.assertEqual(Patient.objects.filter(active_record=True, ethnicity=eth1).count(), 1)

        save_and_deactivate_patient_demo(p, data)

        self.assertEqual(Patient.objects.filter(active_record=True, ethnicity=eth2).count(), 1)
        self.assertEqual(Patient.objects.filter(active_record=False, ethnicity=eth1).count(), 1)
        self.assertEqual(Patient.objects.all().count(), 2)

        #Make sure the two records are different
        p1 = Patient.objects.get(active_record=True, ethnicity=eth2)
        p2 = Patient.objects.get(active_record=False, ethnicity=eth1)
        self.assertFalse(p1.equal_patient_object_data(p2))

    def test_load_patient_data(self):
        #TODO Do Test
        self.assertTrue(True)


class TestPatient(TestCase):
    def test_Patient_equal_patient_object_data(self):
        """ Patient demographic data is equal (Homeland, Ethnicity, Language, PT_DOB

        """
        from SiloamReportingTools.utils import HOMELAND, ETHNICITY, LANGUAGE, APPT_DATE, PT_DOB, PATIENT_ID

        data = {ETHNICITY: 'Test_Eth', HOMELAND: 'Test_Home', LANGUAGE: 'Test_Lang', PATIENT_ID: "1234",
                PT_DOB: "1981-3-20", APPT_DATE: "2012-1-2"}

        e = Ethnicity.objects.create(ethnicity=data[ETHNICITY])
        l = Language.objects.create(language=data[LANGUAGE])
        h = Homeland.objects.create(homeland=data[HOMELAND])
        p_id = data[PATIENT_ID]
        pt_dob = data[PT_DOB]
        lv = data[APPT_DATE]
        vcd = lv

        #Primary object to be compared to
        p = Patient(active_record=True, patient_id=p_id, dob=pt_dob, homeland=h, ethnicity=e,
            language=l, visit_date=vcd)
        p.save()

        #Object that is modified
        p2 = Patient(active_record=True, patient_id=p_id, dob=pt_dob, homeland=h, ethnicity=e,
            language=l,  visit_date=vcd)
        p2.save()

        #Ensure both objects are equal
        self.assertTrue(p.equal_patient_object_data(p2))


        #Change each of the of the values to ensure it fails when compared to the primary case
        p2.homeland = Homeland.objects.create(homeland="Gibberish")
        p2.save()
        self.assertFalse(p.equal_patient_object_data(p2))
        p2.homeland = h
        #In reality this save isn't necessary since the lower one happens before the assertion
        #But I left it in here for knowing p2 is reset back to p1.
        p2.save()

        p2.language = Language.objects.create(language="Test_Home_Other")
        p2.save()
        self.assertFalse(p.equal_patient_object_data(p2))
        p2.language = l
        p2.save()

        p2.ethnicity = Ethnicity.objects.create(ethnicity="Gibberish")
        p2.save()
        self.assertFalse(p.equal_patient_object_data(p2))
        p2.ethnicity = e
        p2.save()

        p2.dob = "1947-10-4"
        p2.save()
        self.assertFalse(p.equal_patient_object_data(p2))
        p2.dob = pt_dob
        p2.save()

        #Ensure Everything had been set back to normal correctly
        self.assertTrue(p.equal_patient_object_data(p2))