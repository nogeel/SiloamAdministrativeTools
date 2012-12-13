from django.contrib import admin
from AssetManagement.models import ComputerAsset, OperatingSystem, Processor,\
    ProcessorSeries, ComputerCategory, HardDrive, ServicePack, PrinterAsset
from AssetManagement.models import Asset, Manufacturer, AssetModelNumber
from AssetManagement.models import Location, AssetCategory



class HardDriveInline(admin.TabularInline):
    model = HardDrive
    extra = 1

class ComputerAssetAdmin(admin.ModelAdmin):
    inlines = [
        HardDriveInline,
        ]


admin.site.register(ComputerAsset, ComputerAssetAdmin)
admin.site.register(OperatingSystem)
admin.site.register(Processor)
admin.site.register(ProcessorSeries)
admin.site.register(Asset)
admin.site.register(ComputerCategory)
admin.site.register(Manufacturer)
admin.site.register(AssetModelNumber)
admin.site.register(Location)
admin.site.register(AssetCategory)
admin.site.register(ServicePack)
admin.site.register(PrinterAsset)

