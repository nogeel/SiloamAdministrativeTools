from django.shortcuts import render, HttpResponse
from SiloamReportingTools.models import Provider
import datetime

MONTHS =('January', "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December")

# def provider_productivity_report(request, first_name, last_name):
#     prov_name = "%s %s" % (first_name, last_name)
#     p = Provider.objects.filter(name=prov_name)[0]


def reporting_navigation(request):

        now = datetime.datetime.now()

        year = now.year
        if now.month == 1:
            year -= 1

        data = {'year': year}

        return render(request, 'SiloamReportingTools/reports.html', data)

def provider_productivity_report(request, provider_id, year):

    prov = Provider.objects.get(id=provider_id)

    previous_year = year - 1
    next_year = year + 1

    no_shows = prov.no_show_count(year)
    work_ins =  prov.workin_count(year)
    no_show_rate = prov.no_show_rate(year)
    complete =  prov.complete_visits(year)
    complete_appointments = prov.complete_appointments(year)

    patient_rescheduled = prov.patient_rescheduled_count(year)
    office_rescheduled = prov.office_rescheduled_count(year)
    patient_canceled = prov.patient_canceled_count(year)
    office_canceled = prov.office_canceled_count(year)

    #Safety Net
    refugee_part_two = prov.ref_part_2_count(year)
    pap_smears = prov.papsmear_count(year)

    data = {'provider': prov, 'year': year, 'months': MONTHS, 'no_shows': no_shows, 'work_ins': work_ins,
            'no_show_rate': no_show_rate, 'complete': complete, 'patient_rescheduled':  patient_rescheduled,
            'office_rescheduled': office_rescheduled, 'patient_canceled': patient_canceled,
            'office_canceled': office_canceled, 'complete_appointments': complete_appointments,
            'refugee_part_two': refugee_part_two, 'pap_smears': pap_smears, 'previous_year': previous_year,
            'next_year': next_year}

    return render(request, 'SiloamReportingTools/provider_productivity_year.html', data)


def aggregate_staff_counts_by_year(request, year):

    prov = Provider.objects.order_by('?')[0]

    previous_year = int(year) - 1
    next_year = int(year) + 1

    no_shows = prov.no_show_count(year, medical_provider=True, staff_provider=True)
    work_ins =  prov.workin_count(year, medical_provider=True, staff_provider=True)
    no_show_rate = prov.no_show_rate(year, medical_provider=True, staff_provider=True)
    complete =  prov.complete_visits(year, medical_provider=True, staff_provider=True)
    complete_appointments = prov.complete_appointments(year, medical_provider=True, staff_provider=True)

    patient_rescheduled = prov.patient_rescheduled_count(year, medical_provider=True, staff_provider=True)
    office_rescheduled = prov.office_rescheduled_count(year, medical_provider=True, staff_provider=True)
    patient_canceled = prov.patient_canceled_count(year, medical_provider=True, staff_provider=True)
    office_canceled = prov.office_canceled_count(year, medical_provider=True, staff_provider=True)

    #Safety Net
    refugee_part_two = prov.ref_part_2_count(year, medical_provider=True, staff_provider=True)
    pap_smears = prov.papsmear_count(year, medical_provider=True, staff_provider=True)

    data = {'provider': prov, 'year': year, 'months': MONTHS, 'no_shows': no_shows, 'work_ins': work_ins,
            'no_show_rate': no_show_rate, 'complete': complete, 'patient_rescheduled':  patient_rescheduled,
            'office_rescheduled': office_rescheduled, 'patient_canceled': patient_canceled,
            'office_canceled': office_canceled, 'refugee_part_two': refugee_part_two, 'pap_smears': pap_smears,
            'complete_appointments': complete_appointments,  'previous_year': previous_year,
            'next_year': next_year}

    return render(request, 'SiloamReportingTools/productivity_by_year.html', data)


def aggregate_medical_count_by_year(request, year):
    prov = Provider.objects.order_by('?')[0]

    no_shows = prov.no_show_count(year, medical_provider=True)
    work_ins =  prov.workin_count(year, medical_provider=True)
    no_show_rate = prov.no_show_rate(year, medical_provider=True)
    complete = prov.complete_visits(year, medical_provider=True)
    complete_appointments = prov.complete_appointments(year, medical_provider=True)

    patient_rescheduled = prov.patient_rescheduled_count(year, medical_provider=True)
    office_rescheduled = prov.office_rescheduled_count(year, medical_provider=True)
    patient_canceled = prov.patient_canceled_count(year, medical_provider=True, staff_provider=True)
    office_canceled = prov.office_canceled_count(year, medical_provider=True, staff_provider=True)

    #Safety Net
    refugee_part_two = prov.ref_part_2_count(year, medical_provider=True, staff_provider=True)
    pap_smears = prov.papsmear_count(year, medical_provider=True, staff_provider=True)

    data = {'provider': prov, 'year': year, 'months': MONTHS, 'no_shows': no_shows, 'work_ins': work_ins,
            'no_show_rate': no_show_rate, 'complete': complete, 'patient_rescheduled':  patient_rescheduled,
            'office_rescheduled': office_rescheduled, 'patient_canceled': patient_canceled,
            'office_canceled': office_canceled, 'refugee_part_two': refugee_part_two, 'pap_smears': pap_smears,
            'complete_appointments': complete_appointments}

    return render(request, 'SiloamReportingTools/productivity_by_year.html', data)


def aggregate_all_encounters_by_year(request, year):
    prov = Provider.objects.order_by('?')[0]

    no_shows = prov.no_show_count(year, all_encounters=True)
    work_ins = prov.workin_count(year, all_encounters=True)
    no_show_rate = prov.no_show_rate(year, all_encounters=True)
    complete = prov.complete_visits(year, all_encounters=True)
    complete_appointments = prov.complete_appointments(year, all_encounters=True)

    patient_rescheduled = prov.patient_rescheduled_count(year, all_encounters=True)
    office_rescheduled = prov.office_rescheduled_count(year, all_encounters=True)
    patient_canceled = prov.patient_canceled_count(year, all_encounters=True)
    office_canceled = prov.office_canceled_count(year, all_encounters=True)

    #Safety Net
    refugee_part_two = prov.ref_part_2_count(year, all_encounters=True)
    pap_smears = prov.papsmear_count(year, all_encounters=True)

    data = { 'provider': prov, 'year': year, 'months': MONTHS, 'no_shows': no_shows, 'work_ins': work_ins,
             'no_show_rate': no_show_rate, 'complete': complete, 'patient_rescheduled':  patient_rescheduled,
             'office_rescheduled': office_rescheduled, 'patient_canceled': patient_canceled,
             'office_canceled': office_canceled, 'refugee_part_two': refugee_part_two, 'pap_smears': pap_smears,
             'complete_appointments': complete_appointments}

    return render(request, 'SiloamReportingTools/productivity_by_year.html', data)