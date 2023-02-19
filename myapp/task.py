from celery import *
from datetime import *
from django.utils import timezone
from .models import CartParcel
from django.contrib.auth.models import User
from celery.decorators import task
from .views import admin_user_return   

@task
def remove_expired_cart_items():
    now = timezone.now()
    expired_cart_items = CartParcel.objects.filter(created_at__lte=now - timedelta(minutes=1))
    expired_cart_items.delete()

@task
def admin_user_return_task(user_id):
    admin_user_return(None, user_id)
