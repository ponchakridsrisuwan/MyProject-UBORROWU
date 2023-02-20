
from celery import *
from datetime import *
from django.utils import timezone
from myapp.models import CartParcel
from django.contrib.auth.models import User   

@task
def remove_expired_cart_items():
    now = timezone.now()
    expired_cart_items = CartParcel.objects.filter(created_at__lte=now - timedelta(minutes=1))
    expired_cart_items.delete()
