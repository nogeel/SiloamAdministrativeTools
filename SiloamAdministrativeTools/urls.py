from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from AssetManagement.models import Asset, ComputerAsset, PrinterAsset

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SiloamAdministrativeTools.views.home', name='home'),
    # url(r'^SiloamAdministrativeTools/', include('SiloamAdministrativeTools.foo.urls')),
    (r'^Asset/$', ListView.as_view(
        model=Asset,
    )),
    (r'^Computers/$', ListView.as_view(
        model=ComputerAsset,
        context_object_name="asset_list",
    )),
    (r'^(p|P)rinters/$', ListView.as_view(
        model=PrinterAsset,
        context_object_name="printers"
    )),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^grappelli/', include('grappelli.urls')),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
