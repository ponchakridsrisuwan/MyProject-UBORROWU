from datetime import *
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.contrib.auth.decorators import login_required
from myappstaff.forms import *
from django.utils import timezone
from django.core.paginator import Paginator
from myappstaff.models import *
from myapp.models import *
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from django.db.models import Max
from django.contrib import messages
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
import requests
from datetime import datetime
from pytz import timezone as timezonenow
th_tz = timezonenow('Asia/Bangkok')


def staff_setting_position(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    if req.method == "POST":
        nameposition = req.POST.get('nameposition')
        obj = SettingPosition(nameposition=nameposition)
        obj.save()
        messages.success(req, 'เพิ่มชั้นวางสำเร็จ!')
        return redirect('/staff_setting_position')   
    else:
        obj = SettingPosition()   
    obj = SettingPosition.objects.all()   
    AllPosition = SettingPosition.objects.all()
    page_num = req.GET.get('page', 1)
    p = Paginator(AllPosition, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)        
    context = {
        "navbar" : "staff_setting_position",
        "AllSettingPosition": SettingPosition.objects.all(),
        "page" : page
    }
    return render(req, 'pages/staff_setting_position.html', context)

@login_required
def deletePosition(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    obj = SettingPosition.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบสำเร็จ!')
    return redirect('/staff_setting_position')

@login_required
def edit_position(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    obj = SettingPosition.objects.get(id=id)
    obj.nameposition = req.POST['nameposition']
    obj.save()
    messages.success(req, 'แก้ไขสำเร็จ!')
    return redirect('/staff_setting_position')


@login_required
def staff_setting(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    if req.method == "POST":
        name_CategoryType = req.POST.get('name_CategoryType')
        obj = CategoryType(name_CategoryType=name_CategoryType)
        obj.save()
        messages.success(req, 'เพิ่มหมวดหมู่สำเร็จ!')
        return redirect('/staff_setting')   
    else:
        obj = CategoryType()   
    obj = CategoryType.objects.all()   
    AllCategoryType = CategoryType.objects.all()
    page_num = req.GET.get('page', 1)
    p = Paginator(AllCategoryType, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)        
    context = {
        "navbar" : "staff_setting",
        "All_CategoryType": CategoryType.objects.all(),
        "page" : page
    }
    return render(req, 'pages/staff_setting.html', context)    

@login_required
def deleteCategoryType(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    obj = CategoryType.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบสำเร็จ!')
    return redirect('/staff_setting')

@login_required
def edit_staff_setting(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    obj = CategoryType.objects.get(id=id)
    obj.name_CategoryType = req.POST['name_CategoryType']
    obj.save()
    messages.success(req, 'แก้ไขสำเร็จ!')
    return redirect('/staff_setting')

# การตั้งค่าสถานะ
@login_required
def staff_setting_status(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    if req.method == "POST":
        name_CategoryStatus = req.POST.get('name_CategoryStatus')
        obj = CategoryStatus(name_CategoryStatus=name_CategoryStatus)
        obj.save()
        messages.success(req, 'เพิ่มสถานะสำเร็จ!')
        return redirect('/staff_setting_status')   
    else:
        obj = CategoryStatus()   
    obj = CategoryStatus.objects.all()   
    AllCategoryStatus = CategoryStatus.objects.all()
    page_num = req.GET.get('page', 1)
    p = Paginator(AllCategoryStatus, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)
    context = {
        "navbar" : "staff_setting_status",
        "All_CategoryStatus": CategoryStatus.objects.all(),
        "page" : page
    }    
    return render(req, 'pages/staff_setting_status.html', context)  

@login_required
def DeleteCategoryStatus(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    obj = CategoryStatus.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบสำเร็จ!')
    return redirect('/staff_setting_status')

@login_required
def edit_staff_setting_status(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    obj = CategoryStatus.objects.get(id=id)
    obj.name_CategoryStatus = req.POST['name_CategoryStatus']
    obj.save()
    messages.success(req, 'แก้ไขสำเร็จ!')
    return redirect('/staff_setting_status')

# การแนะนำวัสดุเข้าสู่ระบบ    
@login_required
def staff_introduction(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllRecList = ListFromRec.objects.filter(status='รออนุมัติ').order_by('name', 'datetime')
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllRecList = AllRecList.order_by('-datetime')
        elif req.GET['sort'] == 'brand':
            AllRecList = AllRecList.order_by('brand')    
        elif req.GET['sort'] == 'name':
            AllRecList = AllRecList.order_by('name')      
        elif req.GET['sort'] == 'quantity':
            AllRecList = AllRecList.order_by('-quantity')   
        elif req.GET['sort'] == 'price':
            AllRecList = AllRecList.order_by('-price')       
        elif req.GET['sort'] == 'default':
            AllRecList = ListFromRec.objects.filter(status='รออนุมัติ').order_by('name', 'datetime')
        else:
            last_sort = 'default'
            AllRecList = ListFromRec.objects.filter(status='รออนุมัติ').order_by('name', 'datetime')
    else:
        last_sort = 'default'
        AllRecList = ListFromRec.objects.filter(status='รออนุมัติ').order_by('name', 'datetime')
    search_rec = ""
    if 'search_rec' in req.GET:
        search_rec = req.GET['search_rec']
        AllRecList = AllRecList.filter(Q(name__contains=search_rec)|Q(quantity__contains=search_rec)
                                             |Q(status__contains=search_rec)|Q(brand__contains=search_rec))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllRecList, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)    
    context = {
        "navbar" : "staff_introduction",
        'page' :page,
        "search_rec" : search_rec,
        "last_sort" : last_sort,
    }            
    return render( req, 'pages/staff_introduction.html', context)

@login_required
def staff_introduction_update(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllRecList = ListFromRec.objects.filter(id=id).first()
    AllRecList.reasonfromstaff = req.POST['reasonfromstaff']
    AllRecList.status = 'อนุมัติ'
    AllRecList.save()
    messages.success(req, 'อนุมัติสำเร็จ!')
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
            msg = ['รายการ : ', AllRecList.name, "สถานะ : ", AllRecList.status, AllRecList.reasonfromstaff,'วันที่อนุมัติ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
            msg = ' '.join(map(str, msg)) 
            requests.post(url, headers=headers, data={'message': msg})
    context = {
        "AllRecList" : AllRecList,
    }
    return redirect('/staff_introduction', context)

@login_required
def staff_introduction_history(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllRecList = ListFromRec.objects.filter(status='อนุมัติ').order_by('name', 'datetime')
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllRecList = AllRecList.order_by('-datetime')
        elif req.GET['sort'] == 'brand':
            AllRecList = AllRecList.order_by('brand')    
        elif req.GET['sort'] == 'name':
            AllRecList = AllRecList.order_by('name')      
        elif req.GET['sort'] == 'quantity':
            AllRecList = AllRecList.order_by('-quantity')   
        elif req.GET['sort'] == 'price':
            AllRecList = AllRecList.order_by('-price')       
        elif req.GET['sort'] == 'default':
            AllRecList = ListFromRec.objects.filter(status='อนุมัติ').order_by('name', 'datetime')
        else:
            last_sort = 'default'
            AllRecList = ListFromRec.objects.filter(status='อนุมัติ').order_by('name', 'datetime')
    else:
        last_sort = 'default'
        AllRecList = ListFromRec.objects.filter(status='อนุมัติ').order_by('name', 'datetime')
    search_rec = ""
    if 'search_rec' in req.GET:
        search_rec = req.GET['search_rec']
        AllRecList = AllRecList.filter(Q(name__contains=search_rec)|Q(quantity__contains=search_rec)
                                             |Q(status__contains=search_rec)|Q(brand__contains=search_rec))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllRecList, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)    
    context =  {
        "navbar" : "staff_introduction_history",
        'page' : page,
        "last_sort" : last_sort,
        "search_rec" : search_rec,
    }            
    return render( req, 'pages/staff_introduction_history.html', context)

# จัดการข้อมูลการแนะนำวัสดุเข้าสู่ระบบ
@login_required
def staff_introduction_detail(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllRecList = ListFromRec.objects.filter(id=id).first()
    context = {
        "AllRecList" : AllRecList,
    }
    return render( req, 'pages/staff_introduction_detail.html', context)

# ประวัติการยืม
@login_required
def staff_borrowing_history(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanParcel = LoanParcel.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='ยืมสำเร็จ'))
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllLoanParcel = AllLoanParcel.order_by('-date_add')
        elif req.GET['sort'] == 'start_date':
            AllLoanParcel = AllLoanParcel.order_by('start_date')    
        elif req.GET['sort'] == 'name':
            AllLoanParcel = AllLoanParcel.order_by('name')      
        elif req.GET['sort'] == 'quantity':
            AllLoanParcel = AllLoanParcel.order_by('-quantity')   
        elif req.GET['sort'] == 'status':
            AllLoanParcel = AllLoanParcel.order_by('status')   
        elif req.GET['sort'] == 'default':
                AllLoanParcel = LoanParcel.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='ยืมสำเร็จ'))
        else:
            last_sort = 'default'
            AllLoanParcel = LoanParcel.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='ยืมสำเร็จ'))
    else:
        last_sort = 'default'
        AllLoanParcel = LoanParcel.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='ยืมสำเร็จ'))
    search_parcel = ""
    if 'search_parcel' in req.GET:
        search_parcel = req.GET['search_parcel']
        AllLoanParcel = AllLoanParcel.filter(Q(name__contains=search_parcel)|Q(quantity__contains=search_parcel)
                                             |Q(status__contains=search_parcel)|Q(description__contains=search_parcel)
                                             |Q(start_date__contains=search_parcel)|Q(date_add__contains=search_parcel)
                                             |Q(type__contains=search_parcel)|Q(statusParcel__contains=search_parcel)
                                             |Q(nameposition__contains=search_parcel))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllLoanParcel, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)    
    context = {
        "navbar" : "staff_borrowing_history",
        "AllLoanParcel" : AllLoanParcel,
        "page" : page,
        "last_sort" : last_sort,
        "search_parcel" : search_parcel,
    }
    return render(req,'pages/staff_borrowing_history.html', context)
    
@login_required
def staff_borrowing_history_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='คืนสำเร็จ'))
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllLoanDurable = AllLoanDurable.order_by('-date_add')
        elif req.GET['sort'] == 'start_date':
            AllLoanDurable = AllLoanDurable.order_by('start_date')    
        elif req.GET['sort'] == 'end_date':
            AllLoanDurable = AllLoanDurable.order_by('-end_date')    
        elif req.GET['sort'] == 'name':
            AllLoanDurable = AllLoanDurable.order_by('name')      
        elif req.GET['sort'] == 'quantity':
            AllLoanDurable = AllLoanDurable.order_by('-quantity')  
        elif req.GET['sort'] == 'status':
            AllLoanDurable = AllLoanDurable.order_by('status')        
        elif req.GET['sort'] == 'default':
            AllLoanDurable = LoanDurable.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='คืนสำเร็จ'))
        else:
            last_sort = 'default'
            AllLoanDurable = LoanDurable.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='คืนสำเร็จ'))
    else:
        last_sort = 'default'
        AllLoanDurable = LoanDurable.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='คืนสำเร็จ'))
    search_durable = ""
    if 'search_durable' in req.GET:
        search_durable = req.GET['search_durable']
        AllLoanDurable = AllLoanDurable.filter(Q(name__contains=search_durable)|Q(quantity__contains=search_durable)
                                             |Q(status__contains=search_durable)|Q(description__contains=search_durable)
                                             |Q(start_date__contains=search_durable)|Q(date_add__contains=search_durable)
                                             |Q(type__contains=search_durable)|Q(statusDurable__contains=search_durable)
                                             |Q(nameposition__contains=search_durable))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllLoanDurable, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)    
    context =  {
        "navbar" : "staff_borrowing_history_durable",
        "AllLoanDurable" : AllLoanDurable,
        "page" : page,
        "last_sort" : last_sort,
        "search_durable" : search_durable,
    }
    return render(req,'pages/staff_borrowing_history_durable.html', context)    

# จัดการรายการยืม
@login_required
def staff_index_borrow(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanParcel = LoanParcel.objects.filter(status='รออนุมัติ').order_by('name', 'date_add')
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllLoanParcel = AllLoanParcel.order_by('-date_add')
        elif req.GET['sort'] == 'start_date':
            AllLoanParcel = AllLoanParcel.order_by('start_date')    
        elif req.GET['sort'] == 'name':
            AllLoanParcel = AllLoanParcel.order_by('name')      
        elif req.GET['sort'] == 'quantity':
            AllLoanParcel = AllLoanParcel.order_by('-quantity')   
        elif req.GET['sort'] == 'default':
             AllLoanParcel = LoanParcel.objects.filter(status='รออนุมัติ').order_by('name', 'date_add')
        else:
            last_sort = 'default'
            AllLoanParcel = LoanParcel.objects.filter(status='รออนุมัติ').order_by('name', 'date_add')
    else:
        last_sort = 'default'
        AllLoanParcel = LoanParcel.objects.filter(status='รออนุมัติ').order_by('name', 'date_add')
    search_parcel = ""
    if 'search_parcel' in req.GET:
        search_parcel = req.GET['search_parcel']
        AllLoanParcel = AllLoanParcel.filter(Q(name__contains=search_parcel)|Q(quantity__contains=search_parcel)
                                             |Q(status__contains=search_parcel)|Q(description__contains=search_parcel)
                                             |Q(start_date__contains=search_parcel)|Q(date_add__contains=search_parcel)
                                             |Q(type__contains=search_parcel)|Q(statusParcel__contains=search_parcel)
                                             |Q(nameposition__contains=search_parcel))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllLoanParcel, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)    
    context = {
        "navbar" : "staff_index_borrow",
        "AllLoanParcel" : AllLoanParcel,
        "page" : page,
        "last_sort" : last_sort,
        "search_parcel" : search_parcel,
    }
    return render(req,'pages/staff_index_borrow.html', context)

@login_required
def staff_index_borrow_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(status='รออนุมัติ').order_by('name', 'date_add')
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllLoanDurable = AllLoanDurable.order_by('-date_add')
        elif req.GET['sort'] == 'start_date':
            AllLoanDurable = AllLoanDurable.order_by('start_date')    
        elif req.GET['sort'] == 'name':
            AllLoanDurable = AllLoanDurable.order_by('name')      
        elif req.GET['sort'] == 'quantity':
            AllLoanDurable = AllLoanDurable.order_by('-quantity')   
        elif req.GET['sort'] == 'default':
            AllLoanDurable = LoanDurable.objects.filter(status='รออนุมัติ').order_by('name', 'date_add')
        else:
            last_sort = 'default'
            AllLoanDurable = LoanDurable.objects.filter(status='รออนุมัติ').order_by('name', 'date_add')
    else:
        last_sort = 'default'
        AllLoanDurable = LoanDurable.objects.filter(status='รออนุมัติ').order_by('name', 'date_add')
    search_durable = ""
    if 'search_durable' in req.GET:
        search_durable = req.GET['search_durable']
        AllLoanDurable = AllLoanDurable.filter(Q(name__contains=search_durable)|Q(quantity__contains=search_durable)
                                             |Q(status__contains=search_durable)|Q(description__contains=search_durable)
                                             |Q(start_date__contains=search_durable)|Q(date_add__contains=search_durable)
                                             |Q(type__contains=search_durable)|Q(statusDurable__contains=search_durable)
                                             |Q(nameposition__contains=search_durable))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllLoanDurable, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1) 
    context =  {
        "navbar" : "staff_index_borrow_durable",
        "AllLoanDurable" : AllLoanDurable,
        "page" : page,
        "last_sort" : last_sort,
        "search_durable" : search_durable,
    }
    return render(req,'pages/staff_index_borrow_durable.html', context)

# จัดการรายการยืม
@login_required
def staff_index_borrownow(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(Q(status='กำลังยืม'))
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllLoanDurable = AllLoanDurable.order_by('-date_add')
        elif req.GET['sort'] == 'start_date':
            AllLoanDurable = AllLoanDurable.order_by('start_date')    
        elif req.GET['sort'] == 'end_date':
            AllLoanDurable = AllLoanDurable.order_by('-end_date')    
        elif req.GET['sort'] == 'name':
            AllLoanDurable = AllLoanDurable.order_by('name')      
        elif req.GET['sort'] == 'quantity':
            AllLoanDurable = AllLoanDurable.order_by('-quantity')   
        elif req.GET['sort'] == 'default':
            AllLoanDurable = LoanDurable.objects.filter(Q(status='กำลังยืม'))
        else:
            last_sort = 'default'
            AllLoanDurable = LoanDurable.objects.filter(Q(status='กำลังยืม'))
    else:
        last_sort = 'default'
        AllLoanDurable = LoanDurable.objects.filter(Q(status='กำลังยืม'))
    search_durable = ""
    if 'search_durable' in req.GET:
        search_durable = req.GET['search_durable']
        AllLoanDurable = AllLoanDurable.filter(Q(name__contains=search_durable)|Q(quantity__contains=search_durable)
                                             |Q(status__contains=search_durable)|Q(description__contains=search_durable)
                                             |Q(start_date__contains=search_durable)|Q(date_add__contains=search_durable)
                                             |Q(type__contains=search_durable)|Q(statusDurable__contains=search_durable)
                                             |Q(nameposition__contains=search_durable))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllLoanDurable, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1) 
    context = {
        "navbar" : "staff_index_borrownow",
        "AllLoanDurable" : AllLoanDurable,
        "page" : page,
        "last_sort" : last_sort,
        "search_durable" : search_durable,
    }
    return render(req,'pages/staff_index_borrownow.html', context)

# จัดการรายการกำลังยืม
def staff_index_return(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(Q(status='รอยืนยันการคืน'))
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllLoanDurable = AllLoanDurable.order_by('-date_add')
        elif req.GET['sort'] == 'start_date':
            AllLoanDurable = AllLoanDurable.order_by('start_date')    
        elif req.GET['sort'] == 'end_date':
            AllLoanDurable = AllLoanDurable.order_by('-end_date')    
        elif req.GET['sort'] == 'name':
            AllLoanDurable = AllLoanDurable.order_by('name')      
        elif req.GET['sort'] == 'quantity':
            AllLoanDurable = AllLoanDurable.order_by('-quantity')   
        elif req.GET['sort'] == 'default':
            AllLoanDurable = LoanDurable.objects.filter(Q(status='รอยืนยันการคืน'))
        else:
            last_sort = 'default'
            AllLoanDurable = LoanDurable.objects.filter(Q(status='รอยืนยันการคืน'))
    else:
        last_sort = 'default'
        AllLoanDurable = LoanDurable.objects.filter(Q(status='รอยืนยันการคืน'))
    search_durable = ""
    if 'search_durable' in req.GET:
        search_durable = req.GET['search_durable']
        AllLoanDurable = AllLoanDurable.filter(Q(name__contains=search_durable)|Q(quantity__contains=search_durable)
                                             |Q(status__contains=search_durable)|Q(description__contains=search_durable)
                                             |Q(start_date__contains=search_durable)|Q(date_add__contains=search_durable)
                                             |Q(type__contains=search_durable)|Q(statusDurable__contains=search_durable)
                                             |Q(nameposition__contains=search_durable))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllLoanDurable, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1) 
    context = {
        "navbar" : "staff_index_return",
        "AllLoanDurable" : AllLoanDurable,
        "page" : page,
        "last_sort" : last_sort,
        "search_durable" : search_durable,
    }
    return render(req,'pages/staff_index_return.html', context)

def staff_return_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    if AllLoanDurable is None:
        return redirect('/staff_index_return')
    AllLoanDurable.status = 'คืนสำเร็จ'
    AllLoanDurable.save()
    messages.success(req, 'คืนสำเร็จ!')
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
            msg = ['รายการ : ', AllLoanDurable.name, "สถานะ : ", AllLoanDurable.status, 'วันที่อนุมัติ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
            msg = ' '.join(map(str, msg)) 
            requests.post(url, headers=headers, data={'message': msg})
    return redirect('/staff_index_return')

def staff_unreturn_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    if AllLoanDurable is None:
        return redirect('/staff_index_return')
    AllLoanDurable.reasonfromstaff = req.POST['reasonfromstaff']
    AllLoanDurable.status = 'คืนไม่สำเร็จ'
    AllLoanDurable.save()
    messages.warning(req, 'คืนไม่สำเร็จ!')
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
            msg = ['รายการ : ', AllLoanDurable.name, "สถานะ : ", AllLoanDurable.status, AllLoanDurable.reasonfromstaff,'วันที่อนุมัติ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
            msg = ' '.join(map(str, msg)) 
            requests.post(url, headers=headers, data={'message': msg})
    return redirect('/staff_index_return')

def staff_borrow_parcel(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanParcel = LoanParcel.objects.filter(id=id).first()
    if AllLoanParcel is None :
        return redirect('/staff_index_borrow')
    AllLoanParcel.reasonfromstaff = req.POST['reasonfromstaff']
    AllLoanParcel.status = 'รอยืนยันการรับ'
    AllLoanParcel.save()
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
            msg = ['รายการ : ', AllLoanParcel.name, "สถานะ : ", AllLoanParcel.status, AllLoanParcel.reasonfromstaff,'วันที่อนุมัติ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
            msg = ' '.join(map(str, msg)) 
            requests.post(url, headers=headers, data={'message': msg})
    return redirect('/staff_index_borrow')

def staff_borrow_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    if AllLoanDurable is None:
        return redirect('/staff_index_borrow_durable')
    AllLoanDurable.reasonfromstaff = req.POST['reasonfromstaff']
    AllLoanDurable.status = 'รอยืนยันการรับ'
    AllLoanDurable.save()
    messages.success(req, 'รอยืนยันการรับ!')
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
            msg = ['รายการ : ', AllLoanDurable.name, "สถานะ : ", AllLoanDurable.status, AllLoanDurable.reasonfromstaff,'วันที่อนุมัติ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
            msg = ' '.join(map(str, msg)) 
            requests.post(url, headers=headers, data={'message': msg})
    return redirect('/staff_index_borrow_durable')

def staff_unborrow_parcel(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanParcel = LoanParcel.objects.filter(id=id).first()
    if AllLoanParcel is None:
        return redirect('/staff_index_borrow')
    AllLoanParcel.reasonfromstaff = req.POST['reasonfromstaff']
    AllLoanParcel.status = 'ไม่อนุมัติ'
    AllLoanParcel.save()
    messages.success(req, 'ไม่อนุมัติ!')
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
            msg = ['รายการ : ', AllLoanParcel.name, "สถานะ : ", AllLoanParcel.status, AllLoanParcel.reasonfromstaff,'วันที่อนุมัติ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
            msg = ' '.join(map(str, msg)) 
            requests.post(url, headers=headers, data={'message': msg})
    return redirect('/staff_index_borrow')

def staff_unborrow_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    if AllLoanDurable is None:
        return redirect('/staff_index_borrow_durable')
    AllLoanDurable.reasonfromstaff = req.POST['reasonfromstaff']
    AllLoanDurable.status = 'ไม่อนุมัติ'
    AllLoanDurable.save()
    messages.success(req, 'ไม่อนุมัติ!')
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
            msg = ['รายการ : ', AllLoanDurable.name, "สถานะ : ", AllLoanDurable.status, AllLoanDurable.reasonfromstaff,'วันที่อนุมัติ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
            msg = ' '.join(map(str, msg)) 
            requests.post(url, headers=headers, data={'message': msg})
    return redirect('/staff_index_borrow_durable')

# รายละเอียดจัดการวัสดุ-ครุภัณฑ์
@login_required
def staff_manage_detail(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllParcel = Add_Parcel.objects.filter(id=id).first()
    waiting_qParcel = QueueParcel.objects.filter(queue_item=AllParcel).count()
    context = {
        "AllParcel" : AllParcel,
        "waiting_qParcel" : waiting_qParcel,
    }
    return render(req,'pages/staff_manage_detail.html', context)

@login_required
def staff_manage_detail_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllDurable = Add_Durable.objects.filter(id=id).first()
    waiting_qDurable = QueueDurable.objects.filter(queue_item=AllDurable).count()
    waiting_period = waiting_qDurable * AllDurable.numdate
    context = {
        "AllDurable" : AllDurable,
        "waiting_qDurable" : waiting_qDurable,
        "waiting_period": waiting_period
    }
    return render(req,'pages/staff_manage_detail_durable.html', context)

# จัดการวัสดุ
@login_required
def staff_manage_parcel(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    form = ParcelForm()
    form.fields['name'].initial = 'test'
    if req.method == 'POST':
        form = ParcelForm(req.POST or None, req.FILES or None)
        if form.is_valid():
            if form.cleaned_data['quantitytype'] == "∞":
                form.cleaned_data['quantity'] += 1
            form.save()
            messages.success(req, 'เพิ่มรายการวัสดุสำเร็จ!')
            return redirect('/staff_manage_parcel')
    else:
        form = ParcelForm()
    AllParcel = Add_Parcel.objects.all()
    categoryType = CategoryType.objects.all()
    categoryStatus = CategoryStatus.objects.all()
    settingPosition = SettingPosition.objects.all()
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'name':
            AllParcel = AllParcel.order_by('name')
        elif req.GET['sort'] == 'quantity':
            AllParcel = AllParcel.order_by('-quantity')    
        elif req.GET['sort'] == 'date':
            AllParcel = AllParcel.order_by('-date')        
        elif req.GET['sort'] == 'numdate':
            AllParcel = AllParcel.order_by('-numdate')    
        elif req.GET['sort'] == 'borrow_count':
            AllParcel = AllParcel.order_by('-borrow_count')
        elif req.GET['sort'] == 'default':
            AllParcel = Add_Parcel.objects.all()
        else:
            last_sort = 'default'
            AllParcel = Add_Parcel.objects.all()
    else:
        last_sort = 'default'
        AllParcel = Add_Parcel.objects.all()
    search_query = ""
    if 'search_query' in req.GET:
        search_query = req.GET['search_query']
        AllParcel = AllParcel.filter(name__icontains=search_query)         
    page_num = req.GET.get('page', 1)
    p = Paginator(AllParcel, 20)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)        
    context = {
        "navbar" : "staff_manage_parcel",
        "page" : page,
        "form" : form,
        "last_sort" : last_sort,
        "search_query" : search_query,
        "categoryType" : categoryType,
        "categoryStatus" : categoryStatus,
        "settingPosition" : settingPosition
    }    
    return render(req, 'pages/staff_manage_parcel.html', context)


@login_required
def delete_staff_manage_detail(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    obj = Add_Parcel.objects.get(id=id)
    obj.delete()
    return redirect('staff_manage_parcel')

@login_required
def edit_staff_manage_parcel(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllParcel = Add_Parcel.objects.get(id=id)
    form = ParcelForm(req.POST or None, req.FILES or None, instance=AllParcel) 
    if form.is_valid():
        form.save()
        messages.success(req, 'แก้ไขรายการวัสดุสำเร็จ!')
    return redirect('staff_manage_parcel')
    

@login_required
def delete_staff_manage_parcel(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    obj = Add_Parcel.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบรายการวัสดุสำเร็จ!')
    return redirect('staff_manage_parcel')

# จัดการครุภัณฑ์
@login_required
def staff_manage_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    form = DurableForm()

    if req.method == 'POST':
        form = DurableForm(req.POST, req.FILES)
        if form.is_valid():
            if form.cleaned_data.get('quantitytype') == "∞":
                form.cleaned_data['quantity'] = float("inf")
            form.save()
            messages.success(req, 'เพิ่มรายการครุภัณฑ์สำเร็จ!')
            return redirect('/staff_manage_durable')
    else:
        form = DurableForm()
    AllDurable = Add_Durable.objects.all()
    categoryType = CategoryType.objects.all()
    categoryStatus = CategoryStatus.objects.all()
    settingPosition = SettingPosition.objects.all()
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'name':
            AllDurable = AllDurable.order_by('name')
        elif req.GET['sort'] == 'quantity':
            AllDurable = AllDurable.order_by('-quantity')    
        elif req.GET['sort'] == 'date':
            AllDurable = AllDurable.order_by('-date')     
        elif req.GET['sort'] == 'borrow_count':
            AllDurable = AllDurable.order_by('-borrow_count')       
        elif req.GET['sort'] == 'numdate':
            AllDurable = AllDurable.order_by('-numdate')          
        elif req.GET['sort'] == 'default':
            AllDurable = Add_Durable.objects.all()
        else:
            last_sort = 'default'
            AllDurable = Add_Durable.objects.all()
    else:
        last_sort = 'default'
        AllDurable = Add_Durable.objects.all()
    search_query = ""
    if 'search_query' in req.GET:
        search_query = req.GET['search_query']
        AllDurable = AllDurable.filter(name__icontains=search_query)        
    page_num = req.GET.get('page', 1)
    p = Paginator(AllDurable, 20)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)   
    context =  {
        "navbar" : "staff_manage_durable",
        "page" : page,
        "form" : form,
        "last_sort" : last_sort,
        "search_query" : search_query,
        "categoryType" : categoryType,
        "categoryStatus" : categoryStatus,
        "settingPosition" : settingPosition
    }    
    return render(req, 'pages/staff_manage_durable.html', context) 


@login_required
def delete_staff_manage_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    obj = Add_Durable.objects.get(id=id)
    obj.delete()
    return redirect('staff_manage_durable') 

@login_required
def edit_staff_manage_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllDurable = Add_Durable.objects.get(id=id)
    form = DurableForm(req.POST or None, req.FILES or None, instance=AllDurable) 
    if form.is_valid():
        for field in form.fields:
            if not form.cleaned_data[field]:
                form.cleaned_data[field] = getattr(AllDurable, field)
        form.save()
        messages.success(req, 'แก้ไขรายการครุภัณฑ์สำเร็จ!')
    context = {
        "AllDurable" : AllDurable,
        "form" : form
    }
    return redirect('/staff_manage_durable', context)


def pdf_print(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllRecList = ListFromRec.objects.all()             
    context = {
        "AllRecList" : AllRecList,
    }
    return render( req, 'pages/pdf.html', context)

def pdf_staff_queue(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllQueueParcel = QueueParcel.objects.all()
    context = {
        "AllQueueParcel" : AllQueueParcel,
    }
    return render( req, 'pages/pdf_staff_queue.html', context)

def pdf_staff_queue_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllQueueDurable = QueueDurable.objects.all()
    context = {
        "AllQueueDurable" : AllQueueDurable,
    }
    return render( req, 'pages/pdf_staff_queue_durable.html', context)

def pdf_staff_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllDurable = Add_Durable.objects.all()
    context = {
        "AllDurable" : AllDurable,
    }
    return render( req, 'pages/pdf_staff_durable.html', context)

def pdf_staff_parcel(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllParcel = Add_Parcel.objects.all()
    context = {
        "AllParcel" : AllParcel,
    }
    return render( req, 'pages/pdf_staff_parcel.html', context)

def pdf_staff_max_borrow(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    MaxLoanParcel = Add_Parcel.objects.values("statustype","nametype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
    context = {
        "MaxLoanParcel" : MaxLoanParcel,
    }
    return render( req, 'pages/pdf_staff_max_borrow.html', context)

def pdf_staff_max_borrow_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    MaxLoanDurable = Add_Durable.objects.values("statustype","nametype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
    context = {
        "MaxLoanDurable" : MaxLoanDurable,
    }
    return render( req, 'pages/pdf_staff_max_borrow_durable.html', context)


def pdf_print_position(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllDurable = Add_Durable.objects.all()
    AllParcel = Add_Parcel.objects.all()
    AllPosition =  SettingPosition.objects.all()   
    items_position = {}
    for position in AllPosition:
        items_position[position] = []
    for AllParcel in AllParcel:
        items_position[AllParcel.nameposition].append(AllParcel)
    for AllDurable in AllDurable:
        items_position[AllDurable.nameposition].append(AllDurable)        
    context = {
        "items_position" : items_position,
        "AllPosition" : AllPosition,
    }
    return render( req, 'pages/pdf_print_position.html', context)

def pdf_borrow(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')  
    AllLoanParcel = LoanParcel.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='ยืมสำเร็จ')) 
    context = {
        "AllLoanParcel" : AllLoanParcel,
    }
    return render( req, 'pages/pdf_borrow.html', context)

def pdf_borrow_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')  
    AllLoanDurable = LoanDurable.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='คืนสำเร็จ'))
    context = {
        "AllLoanDurable" : AllLoanDurable,
    }
    return render( req, 'pages/pdf_borrow_durable.html', context)

@login_required
def staff_admin_user(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllUser = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
    AllUser_count = User.objects.filter(right = "นักศึกษา", status = "ปกติ") 
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllUser = AllUser.order_by('-last_login')
        elif req.GET['sort'] == 'first_name':
            AllUser = AllUser.order_by('first_name')    
        elif req.GET['sort'] == 'email':
            AllUser = AllUser.order_by('email')      
        elif req.GET['sort'] == 'default':
            AllUser = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
        else:
            last_sort = 'default'
            AllUser = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
    else:
        last_sort = 'default'
        AllUser = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
    search_user = ""
    if 'search_user' in req.GET:
        search_user = req.GET['search_user']
        AllUser = AllUser.filter(Q(first_name__contains=search_user)|Q(last_name__contains=search_user)
                                             |Q(email__contains=search_user)|Q(phone__contains=search_user))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllUser, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)  
    context = {
        "navbar" : "staff_admin_user",
        "AllUser_count" : AllUser_count,
        "page" : page,
        "last_sort" : last_sort,
        "search_user" : search_user,
    }
    return render(req, "pages/staff_admin_user.html", context)

@login_required
def staff_admin_user_block(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllUser = User.objects.filter(status = "ถูกจำกัดสิทธิ์", right = "นักศึกษา")
    AllUser_count = User.objects.filter(status = "ถูกจำกัดสิทธิ์", right = "นักศึกษา")
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllUser = AllUser.order_by('-last_login')
        elif req.GET['sort'] == 'first_name':
            AllUser = AllUser.order_by('first_name')    
        elif req.GET['sort'] == 'dealine':
            AllUser = AllUser.order_by('dealine')          
        elif req.GET['sort'] == 'default':
            AllUser = User.objects.filter(status = "ถูกจำกัดสิทธิ์", right = "นักศึกษา")
        else:
            last_sort = 'default'
            AllUser = User.objects.filter(status = "ถูกจำกัดสิทธิ์", right = "นักศึกษา")
    else:
        last_sort = 'default'
        AllUser = User.objects.filter(status = "ถูกจำกัดสิทธิ์", right = "นักศึกษา")
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
    for AllUser in AllUser:
        if AllUser.deadline == 0:
            AllUser.status == "ปกติ"
        AllUser.save()    
    context = {
        "navbar" : "staff_admin_user_block",
        "AllUser_count" : AllUser_count,
        "page" : page,
        "last_sort" : last_sort,
        "search_user" : search_user,
    }    
    return render(req, "pages/staff_admin_user_block.html", context)

"""@login_required
def staff_user_deadline(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    obj = User.objects.get(id=id)
    obj.status = req.POST['status']
    obj.reasonfromstaff = req.POST['reasonfromstaff']
    deadline_str = req.POST['deadline']
    if deadline_str == '':
        obj.deadline = datetime.now() + timedelta(days=7)
    else:
        obj.deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
    obj.save()
    messages.success(req, 'จำกัดสิทธิ์!')
    return redirect('/staff_admin_user_block')"""

scheduler = BackgroundScheduler()
scheduler.start()

def update_user_status(user_id):
    user = User.objects.get(id=user_id)
    user.status = 'ปกติ'
    user.save()

@login_required
def staff_user_deadline(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
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
    users = User.objects.filter(right="นักศึกษา")
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
    return redirect('/staff_admin_user_block') 

scheduler.shutdown()

@login_required
def staff_personal_info(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    return render(req,'pages/staff_personal_info.html')

# รายงานภาพรวมวัสดุ
@login_required
def staff_report(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllRecList_count = ListFromRec.objects.filter(status='รออนุมัติ') 
    AllLoanDurable_count = LoanDurable.objects.filter(status='รอยืนยันการคืน')
    AllLoanParcel_count_borrow = LoanParcel.objects.filter(status='รออนุมัติ')
    AllLoanDurable_count_borrow = LoanDurable.objects.filter(status='รออนุมัติ')
    AllLoanDurable_count_borrownow = LoanDurable.objects.filter(status='กำลังยืม')
    AllUser_count = User.objects.filter(right = "นักศึกษา", status = "ปกติ") 
    AllUser_count_block = User.objects.filter(status = "ถูกจำกัดสิทธิ์", right = "นักศึกษา")
    AllParcel_report = Add_Parcel.objects.all().aggregate(models.Count('id'))['id__count']
    AllDurable_report = Add_Durable.objects.all().aggregate(models.Count('id'))['id__count']
    MaxLoanParcel = Add_Parcel.objects.values("statustype","nametype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')[:3]
    MaxLoanDurable = Add_Durable.objects.values("statustype","nametype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')[:3]
    context = {
        "navbar" : "staff_report",
        "AllRecList_count" : AllRecList_count,
        "AllLoanDurable_count" : AllLoanDurable_count,
        "AllLoanParcel_count_borrow" : AllLoanParcel_count_borrow,
        "AllLoanDurable_count_borrow" : AllLoanDurable_count_borrow,
        "AllLoanDurable_count_borrownow" : AllLoanDurable_count_borrownow,
        "AllUser_count" :AllUser_count,
        "AllUser_count_block" : AllUser_count_block,
        "AllParcel_report" : AllParcel_report,
        "AllDurable_report" : AllDurable_report,
        "MaxLoanParcel" : MaxLoanParcel,
        "MaxLoanDurable" : MaxLoanDurable,
        
    }
    return render( req, 'pages/staff_report.html', context)

# รายงานการยืมทั้งหมด
@login_required
def staff_max_borrow(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    MaxLoanParcel = Add_Parcel.objects.values("statustype","nametype","quantitytype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'name':
            MaxLoanParcel = MaxLoanParcel.order_by('name')
        elif req.GET['sort'] == 'quantity':
            MaxLoanParcel = MaxLoanParcel.order_by('-quantity')    
        elif req.GET['sort'] == 'default':
            MaxLoanParcel  = Add_Parcel.objects.values("statustype","nametype","quantitytype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
        else:
            last_sort = 'default'
            MaxLoanParcel  = Add_Parcel.objects.values("statustype","nametype","quantitytype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
    else:
        last_sort = 'default'
        MaxLoanParcel  = Add_Parcel.objects.values("statustype","nametype","quantitytype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
    search_query = ""
    if 'search_query' in req.GET:
        search_query = req.GET['search_query']
        MaxLoanParcel = MaxLoanParcel.filter(name__icontains=search_query)     
    context = {
        "MaxLoanParcel" : MaxLoanParcel,
        "search_query" : search_query,
        "last_sort" : last_sort,
    }
    return render(req,'pages/staff_max_borrow.html', context )

def staff_max_borrow_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    MaxLoanDurable = Add_Durable.objects.values("statustype","nametype","quantitytype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'name':
            MaxLoanDurable = MaxLoanDurable.order_by('name')
        elif req.GET['sort'] == 'quantity':
            MaxLoanDurable = MaxLoanDurable.order_by('-quantity')    
        elif req.GET['sort'] == 'default':
            MaxLoanDurable = Add_Durable.objects.values("statustype","nametype","quantitytype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
        else:
            last_sort = 'default'
            MaxLoanDurable = Add_Durable.objects.values("statustype","nametype","quantitytype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
    else:
        last_sort = 'default'
        MaxLoanDurable = Add_Durable.objects.values("statustype","nametype","quantitytype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
    search_query = ""
    if 'search_query' in req.GET:
        search_query = req.GET['search_query']
        MaxLoanDurable = MaxLoanDurable.filter(name__icontains=search_query)     
    context = {
        "MaxLoanDurable" : MaxLoanDurable,
        "last_sort" : last_sort,
        "search_query" : search_query,
    }
    return render(req,'pages/staff_max_borrow_durable.html', context )

def staff_queue(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllQueueParcel = QueueParcel.objects.all()
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default') 
        if req.GET['sort'] == 'latest':
            AllQueueParcel = AllQueueParcel.order_by('-date_q')
        elif req.GET['sort'] == 'name':
            AllQueueParcel = AllQueueParcel.order_by('name')    
        elif req.GET['sort'] == 'type':
            AllQueueParcel = AllQueueParcel.order_by('type')    
        elif req.GET['sort'] == 'default':
            AllQueueParcel = QueueParcel.objects.all().order_by('date_q')
        else:
            last_sort = 'default'
            AllQueueParcel = QueueParcel.objects.all().order_by('date_q')
    else:
        last_sort = 'default'
        AllQueueParcel = QueueParcel.objects.all().order_by('date_q')
    search_q = ""
    if 'search_q' in req.GET:
        search_q = req.GET['search_q']
        AllQueueParcel = AllQueueParcel.filter(Q(name__contains=search_q)|Q(type__contains=search_q))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllQueueParcel, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)   
    context ={
        'navbar' : 'staff_queue',
        "AllQueueParcel" : AllQueueParcel,
        "page" : page,
        "last_sort" : last_sort,
        "search_q" : search_q,
        
    }
    return render(req, 'pages/staff_queue.html', context)

def staff_queue_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllQueueDurable = QueueDurable.objects.all()
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllQueueDurable = AllQueueDurable.order_by('-date_q')
        elif req.GET['sort'] == 'name':
            AllQueueDurable = AllQueueDurable.order_by('name')    
        elif req.GET['sort'] == 'type':
            AllQueueDurable = AllQueueDurable.order_by('type')    
        elif req.GET['sort'] == 'default':
            AllQueueDurable = QueueDurable.objects.all().order_by('date_q')
        else:
            last_sort = 'default'
            AllQueueDurable = QueueDurable.objects.all().order_by('date_q')
    else:
        last_sort = 'default'
        AllQueueDurable = QueueDurable.objects.all().order_by('date_q')
    search_q = ""
    if 'search_q' in req.GET:
        search_q = req.GET['search_q']
        AllQueueDurable = AllQueueDurable.filter(Q(name__contains=search_q)|Q(type__contains=search_q))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllQueueDurable, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)   
    context ={
        'navbar' : 'staff_queue_durable',
        "AllQueueDurable" : AllQueueDurable,
        "page" : page,
        "last_sort" : last_sort,
        "search_q" : search_q,
    }
    return render(req, 'pages/staff_queue_durable.html', context)

def staff_position(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา" or req.user.token == None:
        return redirect('/')
    AllDurable = Add_Durable.objects.all()
    AllParcel = Add_Parcel.objects.all()
    AllPosition =  SettingPosition.objects.all()   
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'name':
            AllParcel = AllParcel.order_by('name')
            AllDurable = AllDurable.order_by('name')
        elif req.GET['sort'] == 'category':
            AllParcel = AllParcel.order_by('category')
            AllDurable = AllDurable.order_by('category')    
        elif req.GET['sort'] == 'statustype':
            AllParcel = AllParcel.order_by('statustype')
            AllDurable = AllDurable.order_by('statustype')
        elif req.GET['sort'] == 'status':
            AllParcel = AllParcel.order_by('status')
            AllDurable = AllDurable.order_by('status')    
        elif req.GET['sort'] == 'quantity':
            AllParcel = AllParcel.order_by('-quantity')
            AllDurable = AllDurable.order_by('-quantity')    
        elif req.GET['sort'] == 'borrow_count':
            AllParcel = AllParcel.order_by('-borrow_count')
            AllDurable = AllDurable.order_by('-borrow_count')    
        elif req.GET['sort'] == 'default':
            AllDurable = Add_Durable.objects.all()
            AllParcel = Add_Parcel.objects.all()
        else:
            last_sort = 'default'
            AllDurable = Add_Durable.objects.all()
            AllParcel = Add_Parcel.objects.all()
    else:
        last_sort = 'default'
        AllDurable = Add_Durable.objects.all()
        AllParcel = Add_Parcel.objects.all()
    search_query = ""
    if 'query' in req.GET:
        search_query = req.GET['query']
        AllParcel = AllParcel.filter(name__icontains=search_query)
        AllDurable = AllDurable.filter(name__icontains=search_query)    
    items_position = {}
    for position in AllPosition:
        items_position[position] = []
    for AllParcel in AllParcel:
        items_position[AllParcel.nameposition].append(AllParcel)
    for AllDurable in AllDurable:
        items_position[AllDurable.nameposition].append(AllDurable)
    
    context ={
        'navbar' : 'staff_position',
        "items_position": items_position,
        "AllPosition" : AllPosition,
        "last_sort" : last_sort,
        "search_query" : search_query,
    }
    return render(req, 'pages/staff_position.html', context)
