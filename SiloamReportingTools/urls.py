from django.conf.urls import patterns, url
from SiloamReportingTools.views import provider_productivity_report, aggregate_staff_counts_by_year,\
    aggregate_medical_count_by_year, aggregate_all_encounters_by_year, reporting_navigation

urlpatterns = patterns('',
    url(r'^(?P<provider_id>\d+)/(?P<year>\d{4})/$', provider_productivity_report),
    url(r'^Staff/(?P<year>\d{4})/$', aggregate_staff_counts_by_year),
    url(r'^Medical/(?P<year>\d{4})/$', aggregate_medical_count_by_year),
    url(r'^All/(?P<year>\d{4})/$', aggregate_all_encounters_by_year),
    url(r'^$', reporting_navigation),
)