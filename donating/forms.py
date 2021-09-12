from django import forms
from django.forms import ModelForm

from donating.models import Donation

class DonationForm(forms.Form):
    bags = forms.IntegerField() 
    categories = forms.ChoiceField()
    organisation = forms.MultipleChoiceField()
    address = forms.CharField()
    phone_number = forms.IntegerField() 
    city = forms.CharField()
    zip_code = forms.IntegerField()
    pick_up_date = forms.DateField()
    pick_up_time = forms.TimeField()
    pick_up_comment = forms.CharField()

