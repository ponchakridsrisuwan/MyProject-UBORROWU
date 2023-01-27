from django import forms
from myapp.models import *
from myappstaff.models import *
from django.forms import ModelForm

class ListRecForm(ModelForm):
    class Meta:
        model = ListFromRec
        fields = ['name', 'brand', 'quantity','price', "link", 'description']
