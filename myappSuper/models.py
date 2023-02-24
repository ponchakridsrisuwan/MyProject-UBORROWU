from django.db import models
from django.contrib.auth.models import User
from myapp.models import *
from myappstaff.models import *
from myappSuper.models import *
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class Profile(models.Model):
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    email = models.EmailField(blank=True)    
    def __str__(self):
        return self.firstname