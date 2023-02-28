from datetime import *
from django.contrib import admin
from myappSuper.models import *
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import Group, User   
from django.db.models.signals import pre_save
from django.dispatch import receiver     

RIGHT = (
        ('เจ้าหน้าที่', 'เจ้าหน้าที่'),
        ('นักศึกษา', 'นักศึกษา'),
    )

STATUS = (
        ('ปกติ', 'ปกติ'),
        ('ถูกจำกัดสิทธิ์', 'ถูกจำกัดสิทธิ์'),
    )

User.add_to_class('right', models.CharField(max_length = 100, default = 'นักศึกษา'))
User.add_to_class('status', models.CharField(max_length = 100, choices = STATUS, default = 'ปกติ'))
User.add_to_class('phone', models.CharField(max_length = 10, null=True, blank=True))
User.add_to_class('reasonfromstaff', models.CharField(max_length = 254, null=True, blank=True))
User.add_to_class('datestatus', models.DateTimeField(auto_now_add=True, null=True, blank=True))
User.add_to_class('deadline', models.DateTimeField(auto_now_add=False, null=True, blank=True))
User.add_to_class('token', models.CharField(max_length = 254, null=True, blank=True))


@receiver(pre_save, sender=User)
def set_user_right(sender, instance, **kwargs):
    if instance.email.endswith('wancharoen.up.63@ubu.ac.th'):
        instance.right = 'ผู้ดูแลระบบ'
    else:
        try:
            profile = Profile.objects.get(email=instance.email)
            instance.right = 'นักศึกษา'
        except Profile.DoesNotExist:
            try:
                staff_profile = ProfileStaff.objects.get(email=instance.email)
                instance.right = 'เจ้าหน้าที่'
            except ProfileStaff.DoesNotExist:
                instance.right = ''