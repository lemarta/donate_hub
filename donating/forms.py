from django import forms
from django.db import models
from django.forms import ModelForm

from donating.models import CustomUser, Donation

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


class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

