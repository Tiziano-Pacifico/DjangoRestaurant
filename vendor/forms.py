from django import forms

from accounts.validators import allow_only_images_validator
from vendor.models import Vendor, OpeningHour

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    class Meta:
        model=Vendor
        fields = ['vendor_name', 'vendor_license']

class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day','from_hour','to_hour', 'is_closed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aggiungi una classe personalizzata per from_hour e to_hour
        self.fields['from_hour'].widget.attrs.update({'class': 'time-select'})
        self.fields['to_hour'].widget.attrs.update({'class': 'time-select'})