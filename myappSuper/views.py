from datetime import *
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from myappSuper.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone
from celery import Celery
from celery.schedules import crontab
from django.db.models import Q
from django.contrib import messages
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from pytz import timezone as timezonenow
th_tz = timezonenow('Asia/Bangkok')
from datetime import datetime


@login_required
def admin_detail(req, id):
    if req.user.right != "ผู้ดูแลระบบ" or req.user.token == None:
        return redirect('/') 
    AllUser = User.objects.filter(id=id).first()
    context = {
        "AllUser" : AllUser,
    }
    return render(req, "pages/admin_detail.html", context)

@login_required
def admin_user_setting_detail(req, id):
    if req.user.right != "ผู้ดูแลระบบ" or req.user.token == None:
        return redirect('/') 
    context = {
        "navbar" : "admin_user_setting_detail",
        "AllUser" : AllUser,
    }
    AllUser = User.objects.filter(id=id).first()
    return render(req, "pages/admin_user_setting_detail.html", context)

@login_required
def delete_user(req, id):
    if req.user.right != "ผู้ดูแลระบบ" or req.user.token == None:
        return redirect('/') 
    obj = User.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบผู้ใช้สำเร็จ!')
    return redirect('/admin_user')

@login_required
def admin_user_status(req,id):
    if req.user.right != "ผู้ดูแลระบบ" or req.user.token == None:
        return redirect('/') 
    obj = User.objects.get(id=id)
    obj.right = req.POST['right']
    obj.save()
    messages.success(req, 'เปลี่ยนสถานะสำเร็จ!')
    return redirect('/admin_user') 

scheduler = BackgroundScheduler()
scheduler.start()

def update_user_status(user_id):
    user = User.objects.get(id=user_id)
    user.status = 'ปกติ'
    user.save()

@login_required
def admin_user_deadline(req, id):
    if req.user.right != "ผู้ดูแลระบบ" or req.user.token == None:
        return redirect('/') 
    obj = User.objects.get(id=id)
    deadline_str = req.POST['deadline']
    if deadline_str == '':
        obj.deadline = datetime.now() + timedelta(days=7)
    else:
        obj.deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
    obj.reason = req.POST['reason']
    obj.status = req.POST['status']
    obj.save()
    scheduler.add_job(update_user_status, 'date', run_date=obj.deadline, args=[id])
    messages.success(req, 'เปลี่ยนสถานะสำเร็จ!')
    users = User.objects.filter(Q(right="นักศึกษา")|Q(right="เจ้าหน้าที่")|Q(right="ผู้ดูแลระบบ"))
    datetime_th = th_tz.localize(datetime.now())
    if scheduler.exists():
        for user in users:
            if user.token:
                url = 'https://notify-api.line.me/api/notify'
                token = user.token 
                headers = {
                            'content-type': 'application/x-www-form-urlencoded',
                            'Authorization': 'Bearer ' + token 
                            }
                msg = ['คุณถูกระงับสิทธิ์เป็นระยะเวลา ', obj.deadline, 'วัน เหตุผล : ', obj.reason, 'วันที่ถูกระงับ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
                msg = ' '.join(map(str, msg)) 
                requests.post(url, headers=headers, data={'message': msg})
    return redirect('/admin_block') 

scheduler.shutdown()


@login_required
def admin_user(req):
    if req.user.right != "ผู้ดูแลระบบ" or req.user.token == None:
        return redirect('/') 
    #gg_id = User.objects.filter(user=req.user, provider='google')[0].uid
    AllUserStudent = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
    AllUserStudent_count = User.objects.filter(right = "นักศึกษา", status = "ปกติ") #count การแนะนำ
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllUserStudent = AllUserStudent.order_by('-last_login')
        elif req.GET['sort'] == 'first_name':
            AllUserStudent = AllUserStudent.order_by('first_name')    
        elif req.GET['sort'] == 'email':
            AllUserStudent = AllUserStudent.order_by('email')      
        elif req.GET['sort'] == 'default':
            AllUserStudent = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
        else:
            last_sort = 'default'
            AllUserStudent = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
    else:
        last_sort = 'default'
        AllUserStudent = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
    search_user = ""
    if 'search_user' in req.GET:
        search_user = req.GET['search_user']
        AllUserStudent = AllUserStudent.filter(Q(first_name__contains=search_user)|Q(last_name__contains=search_user)
                                             |Q(email__contains=search_user)|Q(phone__contains=search_user))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllUserStudent, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)  
    context = {
        "navbar" : "admin_user",
        "AllUserStudent_count" :  AllUserStudent_count,
        "page" : page,
        "last_sort" : last_sort,
        "search_user" : search_user,
    }
    return render(req, "pages/admin_user.html", context)

@login_required
def admin_staff(req):
    if req.user.right != "ผู้ดูแลระบบ" or req.user.token == None:
        return redirect('/') 
    AllUserStaff = User.objects.filter(Q(right = "เจ้าหน้าที่")  | Q(right = "ผู้ดูแลระบบ")  | Q(status = "ปกติ"))
    AllUser_count = User.objects.filter(right = "เจ้าหน้าที่", status = "ปกติ")
    AllUser_count_admin = User.objects.filter(right = "ผู้ดูแลระบบ", status = "ปกติ")
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllUserStaff = AllUserStaff.order_by('-last_login')
        elif req.GET['sort'] == 'first_name':
            AllUserStaff = AllUserStaff.order_by('first_name')    
        elif req.GET['sort'] == 'email':
            AllUserStaff = AllUserStaff.order_by('email')      
        elif req.GET['sort'] == 'right':
            AllUserStaff = AllUserStaff.order_by('right')      
        elif req.GET['sort'] == 'default':
            AllUserStaff = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
        else:
            last_sort = 'default'
            AllUserStaff = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
    else:
        last_sort = 'default'
        AllUserStaff = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
    search_user = ""
    if 'search_user' in req.GET:
        search_user = req.GET['search_user']
        AllUserStaff = AllUserStaff.filter(Q(first_name__contains=search_user)|Q(last_name__contains=search_user)
                                             |Q(email__contains=search_user)|Q(phone__contains=search_user))
    context = {
        "navbar" : "admin_staff",
        "AllUserStaff" : AllUserStaff,
        "AllUserStaff_count" : AllUser_count,
        "AllUser_count_admin" : AllUser_count_admin,
        "last_sort" : last_sort,
        "search_user" : search_user,
    }
    return render(req, "pages/admin_staff.html", context)

@login_required
def admin_block(req):
    if req.user.right != "ผู้ดูแลระบบ" or req.user.token == None:
        return redirect('/') 
    AllUser = User.objects.filter(status = "ถูกจำกัดสิทธิ์")
    AllUser_count = User.objects.filter(status = "ถูกจำกัดสิทธิ์")
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllUser = AllUser.order_by('-last_login')
        elif req.GET['sort'] == 'first_name':
            AllUser = AllUser.order_by('first_name')    
        elif req.GET['sort'] == 'dealine':
            AllUser = AllUser.order_by('dealine')          
        elif req.GET['sort'] == 'default':
            AllUser = User.objects.filter(status = "ถูกจำกัดสิทธิ์")
        else:
            last_sort = 'default'
            AllUser = User.objects.filter(status = "ถูกจำกัดสิทธิ์")
    else:
        last_sort = 'default'
        AllUser = User.objects.filter(status = "ถูกจำกัดสิทธิ์")
    search_user = ""
    if 'search_user' in req.GET:
        search_user = req.GET['search_user']
        AllUser = AllUser.filter(Q(first_name__contains=search_user)|Q(last_name__contains=search_user))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllUser, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)  
    context = {
        "navbar" : "admin_block",
        "AllUser_count" : AllUser_count,
        "page" : page,
        "last_sort" : last_sort,
        "search_user" : search_user,
    }
    return render(req, "pages/admin_block.html", context)
