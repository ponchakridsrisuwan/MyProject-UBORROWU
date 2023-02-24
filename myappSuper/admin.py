from datetime import *
from django.contrib import admin
from myappSuper.models import *
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import Group, User        

RIGHT = (
        ('ผู้ดูแลระบบ', 'ผู้ดูแลระบบ'),
        ('เจ้าหน้าที่', 'เจ้าหน้าที่'),
        ('นักศึกษา', 'นักศึกษา'),
    )

STATUS = (
        ('ปกติ', 'ปกติ'),
        ('ถูกจำกัดสิทธิ์', 'ถูกจำกัดสิทธิ์'),
    )


User.add_to_class('right', models.CharField(max_length = 100, choices = RIGHT, default = 'ผู้ดูแลระบบ'))
User.add_to_class('status', models.CharField(max_length = 100, choices = STATUS, default = 'ปกติ'))
User.add_to_class('reason', models.CharField(max_length = 254, null=True, blank=True))
User.add_to_class('phone', models.CharField(max_length = 10, null=True, blank=True))
User.add_to_class('reasonfromstaff', models.CharField(max_length = 254, null=True, blank=True))
User.add_to_class('datestatus', models.DateTimeField(auto_now_add=True, null=True, blank=True))
User.add_to_class('deadline', models.DateTimeField(auto_now_add=False, null=True, blank=True))
User.add_to_class('token', models.CharField(max_length = 254, null=True, blank=True))