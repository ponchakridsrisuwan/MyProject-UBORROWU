from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from myappSuper.models import *
from myappstaff.models import *

BORROWSTATUS = (
        ('รออนุมัติ', 'รออนุมัติ'),
        ('อนุมัติ', 'อนุมัติ'),
        ('ไม่อนุมัติ', 'ไม่อนุมัติ'),
        ('รอยืนยันการรับ', 'รอยืนยันการรับ'),
        ('กำลังยืม', 'กำลังยืม'),
        ('รอยืนยันการคืน', 'รอยืนยันการคืน'),
        ('ยืมสำเร็จ', 'ยืมสำเร็จ'),
        ('คืนสำเร็จ', 'คืนสำเร็จ'),
        ('คืนไม่สำเร็จ', 'คืนไม่สำเร็จ'),
    )


class ListFromRec(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500, default="")
    brand = models.CharField(max_length=300, default="")
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0.0)
    link = models.URLField(max_length=200, default="")
    description = models.TextField(max_length=500, default="")
    datetime = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, choices = BORROWSTATUS, default="รออนุมัติ")
    reasonfromstaff = models.TextField(max_length=500, default="")
    
    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.name
    
class CartParcel(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date_add = models.DateTimeField(auto_now=True)
    parcel_item = models.ForeignKey(Add_Parcel, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    name = models.CharField(max_length=200, default="", blank=True) 
    type = models.CharField(max_length=200, default="", blank=True)    
    statusParcel = models.CharField(max_length=200, default="", blank=True)  
    quantitytype = models.CharField(max_length=200, default="", blank=True)  
    nameposition = models.CharField(max_length=200, default="", blank=True)  
    
    def __str__(self):
        return self.user    
    
class CartDurable(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date_add = models.DateTimeField(auto_now=True)
    durable_item = models.ForeignKey(Add_Durable, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    name = models.CharField(max_length=200, default="", blank=True)    
    type = models.CharField(max_length=200, default="", blank=True)    
    statusDurable = models.CharField(max_length=200, default="", blank=True)
    quantitytype = models.CharField(max_length=200, default="", blank=True)  
    nameposition = models.CharField(max_length=200, default="", blank=True)  
    
    def __str__(self):
        return self.user     

class QueueDurable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    queue_item = models.ForeignKey(Add_Durable, on_delete=models.CASCADE)
    date_q = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, default="", blank=True)
    type = models.CharField(max_length=200, default="", blank=True)    
    is_borrowed = models.BooleanField(default=False)

    
    def __str__(self):
        return self.name    
    
class QueueParcel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    queue_item = models.ForeignKey(Add_Parcel, on_delete=models.CASCADE)
    date_q = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, default="", blank=True)
    type = models.CharField(max_length=200, default="", blank=True)    
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return self.name        
    
class LoanParcel(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    parcel_item = models.ForeignKey(Add_Parcel, on_delete=models.CASCADE, related_name='loan_parcels', default=None, blank=True)
    date_add = models.DateTimeField(auto_now=True)
    start_date = models.DateField(auto_now=False)
    description = models.TextField(max_length=500)
    reasonfromstaff = models.TextField(max_length=500, default="")
    #datefromstaff = models.DateField(auto_now=False)
    status = models.CharField(max_length=200, choices = BORROWSTATUS, default="รออนุมัติ")
    name = models.CharField(max_length=200, default="", blank=True) 
    type = models.CharField(max_length=200, default="", blank=True)   
    quantity = models.IntegerField(default=1) 
    statusParcel = models.CharField(max_length=200, default="", blank=True)
    quantitytype = models.CharField(max_length=200, default="", blank=True)  
    nameposition = models.CharField(max_length=200, default="", blank=True)  
    
    def __str__(self):
        return self.user    
    
class LoanDurable(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    durable_item = models.ForeignKey(Add_Durable, on_delete=models.CASCADE, related_name='loan_durable', default=None, blank=True)
    date_add = models.DateTimeField(auto_now=True)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)
    description = models.TextField(max_length=500)
    reasonfromstaff = models.TextField(max_length=500, default="")
    #datefromstaff = models.DateField(auto_now=False)
    status = models.CharField(max_length=200, choices = BORROWSTATUS, default="รออนุมัติ")
    name = models.CharField(max_length=200, default="", blank=True) 
    type = models.CharField(max_length=200, default="", blank=True)    
    quantity = models.IntegerField(default=1)
    statusDurable = models.CharField(max_length=200, default="", blank=True)
    quantitytype = models.CharField(max_length=200, default="", blank=True)  
    nameposition = models.CharField(max_length=200, default="", blank=True)  
  
    def __str__(self):
        return self.user    
    



