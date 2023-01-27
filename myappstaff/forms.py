
from django import forms
from myappstaff.models import *
from django.forms import ModelForm

class AllPositionForm(ModelForm):
    class Meta:
        model = SettingPosition
        fields = ["nameposition"]

class All_CategoryTypeForm(ModelForm):
    class Meta:
        model = CategoryType
        fields = ["name_CategoryType"]

class All_CategoryStatusForm(ModelForm):
    class Meta:
        model = CategoryStatus
        fields = ["name_CategoryStatus"]                   


class ParcelForm(forms.ModelForm):
    class Meta:
        model = Add_Parcel
        fields = [ "name", "nameposition", "statustype", "category", "status", "quantitytype","quantity", "description", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control rounded-pill"}),
            "nameposition": forms.Select(attrs={"class": "form-control rounded-pill"}),
            "statustype": forms.Select(attrs={"class": "form-control rounded-pill"}),
            "category": forms.Select(attrs={"class": "form-control rounded-pill"}),
            "status": forms.Select(attrs={"class": "form-control rounded-pill"}),
            "quantitytype": forms.Select(attrs={"class": "form-control rounded-pill"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control rounded-pill"}),
            "description": forms.Textarea(attrs={"class": "form-control rounded-5"}),
            "image": forms.FileInput(attrs={"class": "form-control rounded-pill"}),
        }
        labels = {
            "name" : "ระบุชื่อวัสดุ :",
            "nameposition" : "ตำแหน่งการวางวัสดุ",
            "statustype" : "เลือกประเภท",
            "category": "เลือกหมวดหมู่วัสดุ :",
            "status": "เลือกสถานะวัสดุ :",
            "quantitytype": "เลือกประเภทของจำนวน :",
            "quantity": "ระบุจำนวนวัสดุ :",
            "description": "รายละเอียดวัสดุ :",
            "image": "แนบไฟล์ภาพวัสดุ :",
        }

class DurableForm(forms.ModelForm):
    # CategoryType = forms.ModelChoiceField(queryset=CategoryType.objects.all(), empty_label="(Nothing)", to_field_name='name_CategoryType')
    class Meta:
        model = Add_Durable
        fields = ["name", "nameposition",  "statustype", "status", "category", "quantitytype", "quantity", "numdate", "description", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control rounded-pill"}),
            "nameposition": forms.Select(attrs={"class": "form-control rounded-pill"}),
            "statustype": forms.Select(attrs={"class": "form-control rounded-pill"}),
            "category": forms.Select(attrs={"class": "form-control rounded-pill"}),
            "status": forms.Select(attrs={"class": "form-control rounded-pill"}),
            "quantitytype": forms.Select(attrs={"class": "form-control rounded-pill"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control rounded-pill"}),
            "numdate": forms.NumberInput(attrs={"class": "form-control rounded-pill"}),
            "description": forms.Textarea(attrs={"class": "form-control rounded-5"}),
            "image": forms.FileInput(attrs={"class": "form-control rounded-pill"}),
        }
        
        labels = {
            "name" : "ระบุชื่อครุภัณฑ์ :",
            "nameposition" : "ตำแหน่งการวางครุภัณฑ์",
            "statustype" : "เลือกประเภท",
            "category": "เลือกหมวดหมู่ครุภัณฑ์ :",
            "status": "เลือกสถานะครุภัณฑ์ :",
            "quantitytype": "เลือกประเภทของจำนวน :",
            "quantity": "ระบุจำนวนครุภัณฑ์ :",
            "numdate": "ระบุจำนวนวันที่อนุญาตให้ยืม :",
            "description": "รายละเอียดครุภัณฑ์ :",
            "image": "แนบไฟล์ภาพครุภัณฑ์ :",
        }
