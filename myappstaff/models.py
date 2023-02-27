from django.db import models
from django.db.models import *
from django.contrib.auth.models import User
from myapp.models import *
from myappSuper.models import *

STATUSTYPE = (
        ('ต้องคืน', 'ต้องคืน'),
        ('ไม่ต้องคืน', 'ไม่ต้องคืน'),
    )

NAMETYPE = (
        ('วัสดุ', 'วัสดุ'),
        ('ครุภัณฑ์', 'ครุภัณฑ์'),
    )

QUANTITYTYPE = (
        ('ต้องการระบุจำนวน', 'ต้องการระบุจำนวน'),
        ('∞', '∞'),
    )

STATUS = (
    ("พร้อมยืม","พร้อมยืม" ),
    ("ไม่พร้อมยืม","ไม่พร้อมยืม" ),
)

class SettingPosition(models.Model):
    nameposition = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return self.nameposition    

class CategoryType(models.Model):
    name_CategoryType = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return self.name_CategoryType              

class Add_Parcel(models.Model):
    # id วัสดุไม่ต้องคืน
    name = models.CharField(max_length=200, default="", blank=True)
    nametype = models.CharField(max_length=200, choices = NAMETYPE, default="วัสดุ")
    nameposition = models.ForeignKey(SettingPosition, on_delete=models.CASCADE, default="", blank=True,  related_name="position_parcel")
    category = models.ForeignKey(CategoryType, on_delete=models.CASCADE, default="", blank=True,  related_name="category_parcel")
    status = models.CharField(max_length=200, choices = STATUS, default="พร้อมยืม")
    statustype = models.CharField(max_length=200, choices = STATUSTYPE, default="ไม่ต้องคืน")
    quantitytype = models.CharField(max_length=200, choices = QUANTITYTYPE, default="ต้องการระบุจำนวน")
    quantity = models.IntegerField(default= 1 )
    description = models.TextField(default="", blank=True)
    image = models.ImageField(upload_to='Parcel', blank=True, null=True, default='broken_image.png')
    date = models.DateTimeField(auto_now_add=True)
    borrow_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class Add_Durable(models.Model):
    # id ครุภัณฑ์ต้องคืน
    name = models.CharField(max_length=200, default="", blank=True)
    nameposition = models.ForeignKey(SettingPosition, on_delete=models.CASCADE, default="", blank=True,  related_name="position_durable")
    nametype = models.CharField(max_length=200, choices = NAMETYPE, default="ครุภัณฑ์")
    category = models.ForeignKey(CategoryType, on_delete=models.CASCADE, default="", blank=True ,related_name="category_durable")
    status = models.CharField(max_length=200, choices = STATUS, default="พร้อมยืม")
    statustype = models.CharField(max_length=200, choices = STATUSTYPE, default="ต้องคืน")
    quantitytype = models.CharField(max_length=200, choices = QUANTITYTYPE, default="ต้องการระบุจำนวน")
    quantity = models.IntegerField(default=1 )
    numdate = models.PositiveIntegerField(default= 1 )
    description = models.TextField(default="", blank=True)
    image = models.ImageField(upload_to='Durable', blank=True, null=True, default='broken_image.png')
    date = models.DateTimeField(auto_now_add=True)
    borrow_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name