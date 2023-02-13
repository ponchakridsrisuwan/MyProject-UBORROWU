from celery import *
from datetime import *
from django.utils import timezone
from .models import CartParcel
from django.contrib.auth.models import User   

app = Celery('tasks', broker='redis://localhost:6379/0')

@task
def remove_expired_cart_items():
    now = timezone.now()
    expired_cart_items = CartParcel.objects.filter(created_at__lte=now - timedelta(minutes=1))
    expired_cart_items.delete()


@app.task
def update_user_status():
    users = User.objects.filter(status="ถูกจำกัดสิทธิ์")
    for user in users:
        if user.deadline <= datetime.now():
            user.status = "ปกติ"
            user.save()

app.conf.beat_schedule = {
    "update_user_status": {
        "task": "tasks.update_user_status",
        "schedule": 3600.0,
    },
}    