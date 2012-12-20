from django.forms import ModelForm
from AssetManagement.models import PrinterAsset

class PrinterAssetForm(ModelForm):
    class Meta:
        model = PrinterAsset