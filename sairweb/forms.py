from django import forms
from django.forms import ClearableFileInput

from .models import *


class destinationForm(forms.ModelForm):
    class Meta:
        model = destination
        fields = ('dest_name', 'dest_desc','dest_img')


class packageForm(forms.ModelForm):
    class Meta:
        model = package
        fields = ('pkg_name', 'pkg_dest_name','pkg_rating', 'pkg_price','pkg_desc', 'pkg_img')

class visaInfoForm(forms.ModelForm):
    class Meta:
        model = visaInfo
        fields = ['fname','contactNo','passport_no', 'dob','visa_type','vCountry', 'visa_status']

class visaInfoFileForm(forms.ModelForm):
    class Meta:
        model = visaInfoFile
        fields = ['visa_img']
        widgets = {
            'visa_img': ClearableFileInput(attrs={'multiple': True}),
        }


class modaratorForm(forms.ModelForm):
    class Meta:
        model = wadmin
        fields = ('username', 'password', 'email', 'type')