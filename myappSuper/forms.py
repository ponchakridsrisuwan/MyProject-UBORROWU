from myappSuper.models import *
from django.forms import ModelForm
from django import forms

from django import forms
from myappSuper.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'email']
        labels = {
            'firstname': 'ชื่อ',
            'lastname': 'นามสกุล',
            'email': 'อีเมล',
        }
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill'}),
        }
