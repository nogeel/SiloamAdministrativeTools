from django.db import models
from taggit.managers import TaggableManager
from django_extensions.db import fields
from django.utils import timezone
import socket, datetime

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

class Location(models.Model):
    location = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.location

class AssetCategory(models.Model):
        class_name = models.CharField(max_length=255)

        def __unicode__(self):
            return u'%s' % self.class_name

        class Meta:
            verbose_name_plural="Asset categories"

class AssetModelNumber(models.Model):
    manufacturer = models.ForeignKey(Manufacturer)
    model_series = models.CharField(max_length=255, blank=True, null=True)
    model_number = models.CharField(max_length=255, blank=True, null=True)

    #TODO Handle more than one space in the string
    def __unicode__(self):
        temp = u'%s %s %s' % (self.manufacturer, self.model_series, self.model_number)
        temp = temp.strip()
        return temp


class Asset(models.Model):
    serial_no = models.CharField(max_length=255)
    asset_model = models.ForeignKey(AssetModelNumber)
    asset_class = models.ForeignKey(AssetCategory)
    acquisition_date = models.DateField()
    original_value = models.DecimalField(max_digits=20, decimal_places=2)
    location = models.ForeignKey(Location)
    short_description = models.CharField(max_length=160)
    description = models.TextField(blank=True, null=True)
    tags = TaggableManager()
    created_date = fields.CreationDateTimeField()
    modified_date = fields.ModificationDateTimeField()
    currently_used = models.BooleanField(default=True)

    """
        Return True if Asset is a ComputerAsset
    """
    def is_computer(self):
        try:
            self.computerasset
            return True
        except ComputerAsset.DoesNotExist:
            return False

    def __unicode__(self):
        return u'%s' % self.short_description

class Donor(models.Model):
    donor_name = models.CharField(max_length=255)
    fundraiser_id = models.CharField(max_length=128)
    asset = models.ForeignKey(Asset)

    def __unicode__(self):
        return u'%s' % self.donor_name


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255)
    asset = models.ForeignKey(Asset)

    def __unicode__(self):
        return u'%s' % self.vendor_name

class ServicePack(models.Model):
    sp = models.IntegerField()

    def __unicode__(self):
        return u'%s' % self.sp

# Start Computer Related Section
class OperatingSystem(models.Model):
    name = models.CharField(max_length=25)
    version = models.CharField(max_length=25)
    service_pack = models.ForeignKey(ServicePack)
    bit64 = models.BooleanField()

    def __unicode__(self):
        bitType = '64-bit' if self.bit64 else '32-bit'
        return u'%s %s %s, SP %s' % (self.name, self.version, bitType, self.service_pack )


class ServicePack(models.Model):
    service_pack = models.CharField()

    def __unicode__(self):
        return u'%s' % self.service_pack

class ProcessorSeries(models.Model):
    manufacturer = models.ForeignKey(Manufacturer)
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return u'%s %s' % (self.manufacturer, self.name)

    class Meta:
        verbose_name_plural="Processor series"

class Processor(models.Model):
    type = models.ForeignKey(ProcessorSeries)
    processor_model = models.CharField(max_length=25)
    speed_in_ghz = models.DecimalField(decimal_places=2, max_digits=5)
    cores = models.IntegerField()

    def __unicode__(self):
        return u'%s %s' % ( self.type, self.processor_model)


class ComputerCategory(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name_plural="Computer categories"


class ComputerAsset(Asset):
    network_name = models.CharField(max_length=25)
    computer_type = models.ForeignKey(ComputerCategory)
    processor = models.ForeignKey(Processor)
    no_of_processors = models.IntegerField()
    ram_in_gb = models.DecimalField(decimal_places=2, max_digits=9)
    max_ram_in_gb = models.DecimalField(decimal_places=2, max_digits=9)
    mac_address = models.CharField(max_length=25)
    operating_system = models.ForeignKey(OperatingSystem)
    comment = models.TextField(null=True, blank=True)
    last_known_ip = models.IPAddressField(blank=True, null=True)
    last_ip_update = models.DateTimeField(blank=True, null=True)

    """

    Returns the current IP address if the computer is online or the last known IP address.
    If the computer is online the method updates the last_known_ip fields and provides the
    current time for the last_ip_update with the current time. The method only looks for the update

    """
    def get_current_ip(self, update_age_seconds=60):

        if  not self.last_ip_update or (timezone.now() - self.last_ip_update) > datetime.timedelta(seconds = update_age_seconds):
            try:
                ip = socket.gethostbyname(self.network_name)
                self.last_known_ip = ip
                self.last_ip_update = timezone.now()
                self.save()
                return ip
            except socket.gaierror:
                return False
        else:
            return  self.last_known_ip

    def __unicode__(self):
        return self.network_name


class HardDrive(models.Model):
    size_in_GB = models.DecimalField(decimal_places=4, max_digits=24)
    description = models.TextField()
    computer = models.ForeignKey(ComputerAsset)

    def __unicode__(self):
#        if self.size_in_GB < 1024:
#            adjusted_size = u'%s GB' % self.size_in_GB
#        else:
#            tmp_size = round((self.size_in_GB / 1024.0), 2)
#            adjusted_size = u'%s TB' % tmp_size
        return u'%s' % self.size_in_GB

class PrinterType(models.Model):
    printer_type = models.CharField(max_length=255)

    def __unicode__(self):
        return self.printer_type

class PrinterCartridge(models.Model):
    printer_cartridge_model = models.CharField(max_length=255)
    cartridge_cost = models.DecimalField(decimal_places=2, max_digits=9)
    page_yield = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField()
    last_ordered = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.printer_cartridge_model

class PrinterAsset(Asset):
    printer_type = models.ForeignKey(PrinterType)
    printer_ip = models.CharField(max_length=20, null=True)
    cartridges = models.ManyToManyField(PrinterCartridge)
    personal_printer = models.BooleanField()

    def get_printer_catridges(self):
        p = PrinterAsset.objects.get(id=self.id)
        return p.cartridges.all()

    def __unicode__(self):
        return self.short_description


class PrinterPrinterCartridgeType(models.Model):
    cartridge_type = models.CharField(max_length=255)

    def __unicode__(self):
        return self.cartridge_type

# End Computer Section

class DepreciationRate(models.Model):
    depreciation_in_years = models.IntegerField()
    asset_class = models.ForeignKey(AssetCategory)



class Disposition_Type(models.Model):
    name = models.CharField(max_length=128)

class Disposition(models.Model):
    date = models.DateField()
    disposition_type = models.ForeignKey(Disposition_Type)