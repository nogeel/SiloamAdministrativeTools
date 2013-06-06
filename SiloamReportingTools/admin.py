from django.contrib import admin
from .models import Language, Ethnicity, Homeland, VisitStatus, VisitType, VisitTypeClass, Patient, ProviderName, Provider, Event, EventType

admin.site.register(Language)
admin.site.register(Ethnicity)
admin.site.register(Homeland)
admin.site.register(VisitStatus)
admin.site.register(VisitType)
admin.site.register(Patient)
admin.site.register(ProviderName)
admin.site.register(Provider)
admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(VisitTypeClass)

