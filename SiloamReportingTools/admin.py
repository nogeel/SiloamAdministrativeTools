from django.contrib import admin
from .models import Language, Ethnicity, Homeland, VisitStatus, VisitType, Patient

admin.site.register(Language)
admin.site.register(Ethnicity)
admin.site.register(Homeland)
admin.site.register(VisitStatus)
admin.site.register(VisitType)
admin.site.register(Patient)

