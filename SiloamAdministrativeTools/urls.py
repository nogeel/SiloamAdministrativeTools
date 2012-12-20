from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from AssetManagement.models import Asset, ComputerAsset, PrinterAsset
from AssetManagement.views import current_datetime

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SiloamAdministrativeTools.views.home', name='home'),
    # url(r'^SiloamAdministrativeTools/', include('SiloamAdministrativeTools.foo.urls')),
    (r'^(A|a)ssets/$', ListView.as_view(
        model=Asset,
    )),
    url(r'^(A|a)sset/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Asset,
            context_object_name='asset')),

    (r'^Computers/$', ListView.as_view(
        model=ComputerAsset,
        context_object_name="computers",
    )),
    url(r'^Computer/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=ComputerAsset,
            context_object_name='computer',
            template_name='computerasset_detail.html')),

    (r'^(p|P)rinters/$', ListView.as_view(
        model=PrinterAsset,
        context_object_name="printers"
    )),
    (r'CurrentTime/$', current_datetime),
    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^grappelli/', include('grappelli.urls')),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
