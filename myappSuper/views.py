from datetime import *
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
#from myapp.task import admin_user_return_task
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
#from celery.task import periodic_task
import csv, io
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.conf import settings
import os



@login_required
def admin_detail(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
        return redirect('/')
    if req.user.phone is None or req.user.token is None:
        return redirect('/phone_add_number')
    AllUser = User.objects.filter(id=id).first()
    context = {
        "AllUser" : AllUser,
    }
    return render(req, "pages/admin_detail.html", context)

@login_required
def delete_user(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
        return redirect('/')
    if req.user.phone is None or req.user.token is None:
        return redirect('/phone_add_number')
    obj = User.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบผู้ใช้สำเร็จ!')
    return redirect('/admin_user')

@login_required
def admin_user_status(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
        return redirect('/')
    if req.user.phone is None or req.user.token is None:
        return redirect('/phone_add_number')
    obj = User.objects.get(id=id)
    obj.right = req.POST['right']
    obj.save()
    messages.success(req, 'เปลี่ยนสถานะสำเร็จ!')
    return redirect('/admin_user') 

@login_required
def admin_user_deadline(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
        return redirect('/')
    if req.user.phone is None or req.user.token is None:
        return redirect('/phone_add_number')
    obj = User.objects.get(id=id)
    deadline_str = req.POST['deadline']
    if deadline_str == '':
        obj.deadline = datetime.now() + timedelta(days=7)
    else:
        obj.deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
    obj.reasonfromstaff = req.POST['reasonfromstaff']
    obj.status = "ถูกจำกัดสิทธิ์"
    obj.save()
    messages.success(req, 'เปลี่ยนสถานะสำเร็จ!')
    #admin_user_return_task.apply_async(args=[obj.id], eta=obj.deadline)
    users = User.objects.filter(Q(status="ถูกจำกัดสิทธิ์"))
    datetime_th = th_tz.localize(datetime.now())
    for user in users:
        if user.token:
            url = 'https://notify-api.line.me/api/notify'
            token = user.token 
            headers = {
                            'content-type': 'application/x-www-form-urlencoded',
                            'Authorization': 'Bearer ' + token 
                            }
            msg = ['คุณถูกระงับสิทธิ์เป็นระยะเวลา ', obj.deadline, 'วัน เหตุผล : ', obj.reasonfromstaff, 'วันที่ถูกระงับ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
            msg = ' '.join(map(str, msg)) 
            requests.post(url, headers=headers, data={'message': msg})
    return redirect('/admin_block') 

@login_required
def admin_user_return(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    if req.user.phone is None or req.user.token is None:
        return redirect('/phone_add_number')
    obj = User.objects.get(id=id)
    obj.status = "ปกติ"
    obj.save()
    messages.success(req, 'เปลี่ยนสถานะสำเร็จ!')
    users = User.objects.filter(right="นักศึกษา")
    datetime_th = th_tz.localize(datetime.now())
    for user in users:
        if user.token:
            url = 'https://notify-api.line.me/api/notify'
            token = user.token 
            headers = {
                            'content-type': 'application/x-www-form-urlencoded',
                            'Authorization': 'Bearer ' + token 
                            }
            msg = ['สถานะการใช้งานของคุณกลับสู่สถานะปกติเมื่อ ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
            msg = ' '.join(map(str, msg)) 
            requests.post(url, headers=headers, data={'message': msg})
    return redirect('/admin_block') 

@login_required
def admin_user(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
        return redirect('/')
    if req.user.phone is None or req.user.token is None:
        return redirect('/phone_add_number')
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
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
        return redirect('/')
    if req.user.phone is None or req.user.token is None:
        return redirect('/phone_add_number')
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
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
        return redirect('/')
    if req.user.phone is None or req.user.token is None:
        return redirect('/phone_add_number')
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

def person_upload(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
        return redirect('/')
    if req.user.phone is None or req.user.token is None:
        return redirect('/phone_add_number')
    data = Profile.objects.all()    
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'firstname':
            data = Profile.objects.order_by('firstname')
        elif req.GET['sort'] == 'lastname':
            data = Profile.objects.order_by('-lastname')      
        elif req.GET['sort'] == 'email':
            data = Profile.objects.order_by('email')       
        elif req.GET['sort'] == 'default':
            data = Profile.objects.all()
        else:
            last_sort = 'default'
            data = Profile.objects.all()
    else:
        last_sort = 'default'
        data = Profile.objects.all()
    search_rec = ""
    if 'search_rec' in req.GET:
        search_rec = req.GET['search_rec']
        data = Profile.objects.filter(Q(firstname=search_rec)|Q(lastname=search_rec)
                                             |Q(email=search_rec))   
    form = ProfileForm() 
    if req.method == 'POST':
        form = ProfileForm(req.POST or None)
        if form.is_valid():
            form.save()
            messages.success(req, 'เพิ่มรายการเร็จ!')
            return redirect('person_upload')
    else:
        form = ProfileForm()
    context = {
        "navbar" : "person_upload",
        'profiles': data,
        "search_rec" : search_rec,
        "last_sort" : last_sort, 
        "form" : form
    }

    if req.method == "GET":
        return render(req, "pages/person_upload.html", context)    
    
    csv_file = req.FILES['file'] 
    if not csv_file.name.endswith('.csv'):
        messages.error(req, 'THIS IS NOT A CSV FILE')    
    data_set = csv_file.read().decode('UTF-8') 
    data_set = data_set.replace('"', '') 
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        Profile.objects.create(
            firstname=column[0],
            lastname=column[1],
            email=column[2],
        )

    return redirect('person_upload')

@login_required
def deleteProfile(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
        return redirect('/')
    if req.user.phone is None or req.user.token is None:
        return redirect('/phone_add_number')
    obj = Profile.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบสำเร็จ!')
    return redirect("person_upload")

@login_required
def delete_profiles(req):
    if req.method == 'POST':
        ids = req.POST.getlist('id')
        Profile.objects.filter(id__in=ids).delete()
        return redirect('person_upload')

@login_required
def csv_person_download(req):
    file_path = os.path.join(settings.MEDIA_ROOT, 'flies/csv_person.csv')
    if not os.path.exists(file_path):
        raise Http404('File not found')
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
