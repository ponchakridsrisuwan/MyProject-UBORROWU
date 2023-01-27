from asyncio import Queue
from datetime import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myapp import forms
from myapp.admin import *
from django.utils import timezone
from django.core.paginator import Paginator
from myapp.forms import *
from myappSuper.models import *
from myappstaff.models import *
import datetime
from django.contrib import messages
import requests
from datetime import datetime
from pytz import timezone as timezonenow
th_tz = timezonenow('Asia/Bangkok')
from datetime import datetime


#หน้าหลัก
def HomePage(req):
    if req.user.is_anonymous:
        return redirect('login/')
    if req.user.phone is None:
        return redirect('/phone_add_number')
    
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    AllParcel = Add_Parcel.objects.all()
    AllDurable = Add_Durable.objects.all()
    AllLoanParcel = LoanParcel.objects.filter(Q(status='รออนุมัติ') | Q(status='รอยืนยันการรับ'), user=req.user)
    AllLoanDurable = LoanDurable.objects.filter(Q(status='รออนุมัติ') | Q(status='รอยืนยันการรับ') | Q(status='กำลังยืม') 
                                                | Q(status='รอยืนยันการคืน')| Q(status='คืนไม่สำเร็จ') , user=req.user)
    selected_category = req.GET.get('category', None)
    AllCategoryType = CategoryType.objects.all()
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'category':
            AllDurable = AllDurable.filter(category=req.GET['category']).order_by('category__name_CategoryType')
            AllParcel = AllParcel.filter(category=req.GET['category']).order_by('category__name_CategoryType')
        else:
            last_sort = 'default'
            AllDurable = Add_Durable.objects.all()
            AllParcel = Add_Parcel.objects.all()
    else:
        last_sort = 'default'
        AllDurable = Add_Durable.objects.all()
        AllParcel = Add_Parcel.objects.all() 
    p_listparcel = Paginator(AllParcel, 8)
    
    p_listdurable = Paginator(AllDurable, 8)
    page_num = req.GET.get('page', 1)
    try:
        pageparcel = p_listparcel.page(page_num)
        pagedurable = p_listdurable.page(page_num)
    except:
        pageparcel = p_listparcel.page(1)  
        pagedurable = p_listdurable.page(1)     
    context = {
        "navbar" : "user_index",
        "AllParcel" : AllParcel,
        "AllDurable" : AllDurable,
        "pageparcel" : pageparcel,
        "pagedurable" : pagedurable,
        "AllLoanParcel" : AllLoanParcel,
        "AllLoanDurable" : AllLoanDurable,
        "Total" : Total,
        "last_sort" : last_sort,
        "selected_category" : selected_category,
        "AllCategoryType" : AllCategoryType,
    }    
    return render(req, 'pages/user_index.html', context)

def phone_add_number(req):
    if req.method == 'POST':
        phone = req.POST['phone']
        token = req.POST['token']
        if phone is not None or token is not None :
            req.user.phone = phone
            req.user.token = token
            req.user.save()
            messages.success(req, 'เพิ่มเบอร์โทรศัพท์และเชื่อมต่อไลน์สำเร็จ!')
            return redirect('/')
        else: 
            return redirect('/phone_add_number')
    else:
        return render(req, 'pages/phone_add_number.html') 
    
def user_personal_info(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    context = {
        "Total" : Total,
    }
    return render(req, 'pages/user_personal_info.html', context)

#หน้ายืม
@login_required
def user_borrow(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    AllLoanParcel = LoanParcel.objects.filter(Q(status='รออนุมัติ') | Q(status='รอยืนยันการรับ'), user=req.user).order_by('status')
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
            AllLoanParcel = LoanParcel.objects.filter(Q(status='รออนุมัติ') | Q(status='รอยืนยันการรับ'), user=req.user).order_by('status')
        else:
            last_sort = 'default'
            AllLoanParcel = LoanParcel.objects.filter(Q(status='รออนุมัติ') | Q(status='รอยืนยันการรับ'), user=req.user).order_by('status')
    else:
        last_sort = 'default'
        AllLoanParcel = LoanParcel.objects.filter(Q(status='รออนุมัติ') | Q(status='รอยืนยันการรับ'), user=req.user).order_by('status')
    search_parcel = ""
    if 'search_parcel' in req.GET:
        search_parcel = req.GET['search_parcel']
        AllLoanParcel = AllLoanParcel.filter(Q(name__contains=search_parcel)|Q(quantity__contains=search_parcel)
                                             |Q(status__contains=search_parcel)|Q(description__contains=search_parcel)
                                             |Q(start_date__contains=search_parcel)|Q(date_add__contains=search_parcel)
                                             |Q(type__contains=search_parcel)|Q(statusParcel__contains=search_parcel)
                                             |Q(nameposition__contains=search_parcel))
    p_listparcel = Paginator(AllLoanParcel, 8)
    page_num = req.GET.get('page', 1)
    try:
        pageparcel = p_listparcel.page(page_num)
    except:
        pageparcel = p_listparcel.page(1)  
    context = {
        "navbar" : "user_borrow",
        "AllLoanParcel" : AllLoanParcel,
        "pageparcel" : pageparcel,
        "Total" : Total,
        "last_sort" : last_sort,
        "search_parcel" : search_parcel,
    }
    return render(req,'pages/user_borrow.html', context)
    
def user_borrow_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable 
    AllLoanDurable = LoanDurable.objects.filter(
        Q(status='รอยืนยันการรับ') | Q(status='รออนุมัติ') | Q(status='คืนไม่สำเร็จ'), user=req.user).order_by('status')
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
            AllLoanDurable = LoanDurable.objects.filter(Q(status='รออนุมัติ') | Q(status='รอยืนยันการรับ'), user=req.user).order_by('status')
        else:
            last_sort = 'default'
            AllLoanDurable = LoanDurable.objects.filter(Q(status='รออนุมัติ') | Q(status='รอยืนยันการรับ'), user=req.user).order_by('status')
    else:
        last_sort = 'default'
        AllLoanDurable = LoanDurable.objects.filter(Q(status='รออนุมัติ') | Q(status='รอยืนยันการรับ'), user=req.user).order_by('status')
    search_durable = ""
    if 'search_durable' in req.GET:
        search_durable = req.GET['search_durable']
        AllLoanDurable = AllLoanDurable.filter(Q(name__contains=search_durable)|Q(quantity__contains=search_durable)
                                             |Q(status__contains=search_durable)|Q(description__contains=search_durable)
                                             |Q(start_date__contains=search_durable)|Q(date_add__contains=search_durable)
                                             |Q(type__contains=search_durable)|Q(statusDurable__contains=search_durable)
                                             |Q(nameposition__contains=search_durable))
    p_listdurable = Paginator(AllLoanDurable, 8)
    page_num = req.GET.get('page', 1)
    try:
        pagedurable = p_listdurable.page(page_num)
    except:
        pagedurable = p_listdurable.page(1)  
    context = {
        "navbar" : "user_borrow_durable",
        "AllLoanDurable" : AllLoanDurable,
        "pagedurable" : pagedurable,
        "Total" : Total,
        "last_sort" : last_sort,
        "search_durable" : search_durable,
    }
    return render(req,'pages/user_borrow_durable.html', context)    

def confirm_parcel(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllLoanParcel = LoanParcel.objects.filter(id=id).first()
    AllLoanParcel.status = 'ยืมสำเร็จ'
    AllLoanParcel.save()
    messages.success(req, 'ยืมสำเร็จ!')
    return redirect('/user_history')

def confirm_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    AllLoanDurable.status = 'กำลังยืม'
    AllLoanDurable.save()
    messages.success(req, 'กำลังยืม!')
    return redirect('/user_borrowed')

def return_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    AllLoanDurable.status = 'รอยืนยันการคืน'
    AllLoanDurable.save()
    users = User.objects.filter(Q(right="นักศึกษา")|Q(right="เจ้าหน้าที่")|Q(right="ผู้ดูแลระบบ"))
    datetime_th = th_tz.localize(datetime.now())
    if LoanDurable.objects.filter(id=id).exists():
        for user in users:
            if user.token:
                url = 'https://notify-api.line.me/api/notify'
                token = user.token 
                headers = {
                            'content-type': 'application/x-www-form-urlencoded',
                            'Authorization': 'Bearer ' + token 
                            }
                msg = [AllLoanDurable.user.email ,'ทำรายการคืน : ', AllLoanDurable.name, 'วันที่ทำรายการ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
                msg = ' '.join(map(str, msg)) 
                requests.post(url, headers=headers, data={'message': msg})
    return redirect('/user_borrowed')

#หน้าคืน
@login_required
def user_borrowed(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    AllLoanDurable = LoanDurable.objects.filter(Q(status='รอยืนยันการคืน')| Q(status='คืนไม่สำเร็จ') | Q(status='กำลังยืม' ), user=req.user) 
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
            AllLoanDurable = LoanDurable.objects.filter(Q(status='รอยืนยันการคืน')| Q(status='คืนไม่สำเร็จ') | Q(status='กำลังยืม' ), user=req.user)
        else:
            last_sort = 'default'
            AllLoanDurable = LoanDurable.objects.filter(Q(status='รอยืนยันการคืน')| Q(status='คืนไม่สำเร็จ') | Q(status='กำลังยืม' ), user=req.user)
    else:
        last_sort = 'default'
        AllLoanDurable = LoanDurable.objects.filter(Q(status='รอยืนยันการคืน')| Q(status='คืนไม่สำเร็จ') | Q(status='กำลังยืม' ), user=req.user)
    search_durable = ""
    if 'search_durable' in req.GET:
        search_durable = req.GET['search_durable']
        AllLoanDurable = AllLoanDurable.filter(Q(name__contains=search_durable)|Q(quantity__contains=search_durable)
                                             |Q(status__contains=search_durable)|Q(description__contains=search_durable)
                                             |Q(start_date__contains=search_durable)|Q(date_add__contains=search_durable)
                                             |Q(type__contains=search_durable)|Q(statusDurable__contains=search_durable)
                                             |Q(nameposition__contains=search_durable))    
    def send_loan_durable(user, loan_durable):
        today = datetime.now().date()
        end_date = loan_durable.end_date
        if end_date == today:
            url = 'https://notify-api.line.me/api/notify'
            token = user.token
            headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'Authorization': 'Bearer ' + token
                }
            msg = f"แจ้งเตือน : วันนี้วันสุดท้ายการยืม {loan_durable.name} กรุณาคืน {loan_durable.name} ด้วยครับ"
            requests.post(url, headers=headers, data={'message': msg})    
        for loan_durable in AllLoanDurable:
            send_loan_durable(req.user, loan_durable)   
    p_listdurable = Paginator(AllLoanDurable, 8)
    page_num = req.GET.get('page', 1)
    try:
        pagedurable = p_listdurable.page(page_num)
    except:
        pagedurable = p_listdurable.page(1)  
    context = {
        'navbar' : 'user_borrowed',
        "AllLoanDurable" : AllLoanDurable,
        "pagedurable" : pagedurable,
        "Total" : Total,
        "last_sort" : last_sort,
        "search_durable" : search_durable,
    }
    return render(req,'pages/user_borrowed.html', context)

#หน้าประวัติ
@login_required
def user_history(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllLoanParcel = LoanParcel.objects.filter(Q(status='ไม่อนุมัติ')| Q(status='ยืมสำเร็จ'), user=req.user)
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
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
                AllLoanParcel = LoanParcel.objects.filter(Q(status='ไม่อนุมัติ')| Q(status='ยืมสำเร็จ'), user=req.user)
        else:
            last_sort = 'default'
            AllLoanParcel = LoanParcel.objects.filter(Q(status='ไม่อนุมัติ')| Q(status='ยืมสำเร็จ'), user=req.user)
    else:
        last_sort = 'default'
        AllLoanParcel = LoanParcel.objects.filter(Q(status='ไม่อนุมัติ')| Q(status='ยืมสำเร็จ'), user=req.user)
    search_parcel = ""
    if 'search_parcel' in req.GET:
        search_parcel = req.GET['search_parcel']
        AllLoanParcel = AllLoanParcel.filter(Q(name__contains=search_parcel)|Q(quantity__contains=search_parcel)
                                             |Q(status__contains=search_parcel)|Q(description__contains=search_parcel)
                                             |Q(start_date__contains=search_parcel)|Q(date_add__contains=search_parcel)
                                             |Q(type__contains=search_parcel)|Q(statusParcel__contains=search_parcel)
                                             |Q(nameposition__contains=search_parcel))
    p_listparcel = Paginator(AllLoanParcel, 8)
    page_num = req.GET.get('page', 1)
    try:
        pageparcel = p_listparcel.page(page_num)
    except:
        pageparcel = p_listparcel.page(1)  
    context = {
        'navbar' : 'user_history',
        "AllLoanParcel" : AllLoanParcel,
        "pageparcel" : pageparcel,
        "Total" : Total,
        "last_sort" : last_sort,
        "search_parcel" : search_parcel,
    }
    return render(req,'pages/user_history.html', context)
    
@login_required
def user_history_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    AllLoanDurable = LoanDurable.objects.filter(Q(status='คืนสำเร็จ') | Q(status='ไม่อนุมัติ'), user=req.user)
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
            AllLoanDurable = LoanDurable.objects.filter(Q(status='คืนสำเร็จ') | Q(status='ไม่อนุมัติ'), user=req.user)
        else:
            last_sort = 'default'
            AllLoanDurable = LoanDurable.objects.filter(Q(status='คืนสำเร็จ') | Q(status='ไม่อนุมัติ'), user=req.user)
    else:
        last_sort = 'default'
        AllLoanDurable = LoanDurable.objects.filter(Q(status='คืนสำเร็จ') | Q(status='ไม่อนุมัติ'), user=req.user)
    search_durable = ""
    if 'search_durable' in req.GET:
        search_durable = req.GET['search_durable']
        AllLoanDurable = AllLoanDurable.filter(Q(name__contains=search_durable)|Q(quantity__contains=search_durable)
                                             |Q(status__contains=search_durable)|Q(description__contains=search_durable)
                                             |Q(start_date__contains=search_durable)|Q(date_add__contains=search_durable)
                                             |Q(type__contains=search_durable)|Q(statusDurable__contains=search_durable)
                                             |Q(nameposition__contains=search_durable))
    p_listdurable = Paginator(AllLoanDurable, 8)
    page_num = req.GET.get('page', 1)
    try:
        pagedurable = p_listdurable.page(page_num)
    except:
        pagedurable = p_listdurable.page(1)  
    context = {
        'navbar' : 'user_history',
        "AllLoanDurable" : AllLoanDurable,
        "pagedurable" : pagedurable,
        "Total" : Total,
        "last_sort" : last_sort,
        "search_durable" : search_durable,
    }
    return render(req,'pages/user_history_durable.html', context)    

#หน้ายืม
def user_cart(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel = CartParcel.objects.filter(user = req.user)
    AllCartDurable = CartDurable.objects.filter(user = req.user)
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable

    context = {
        "AllCartParcel" : AllCartParcel,
        "AllCartDurable" : AllCartDurable,
        "TotalParcel" : TotalParcel,
        "TotalDurable" : TotalDurable,
        "Total" : Total,
    }
    return render(req, 'pages/user_cart.html',context)

def add_to_cart(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None:
        return redirect('/')
    parcel_item = Add_Parcel.objects.get(id=id)
    queue_item = QueueParcel.objects.filter(user=req.user, queue_item=parcel_item).first()
    if parcel_item.quantity > 0 or parcel_item.quantitytype == "∞":
        if parcel_item.quantitytype == "∞":
            parcel_item.borrow_count += 1  
            parcel_item.save()
            queue_item.delete()
            messages.success(req, 'เพิ่มรายการสำเร็จ!')
        else :    
            parcel_item.quantity -= 1
            parcel_item.borrow_count += 1  
            parcel_item.save()
            queue_item.delete()
            messages.success(req, 'เพิ่มรายการสำเร็จ!')
        ex_cart_parcel = CartParcel.objects.filter(parcel_item=parcel_item, user=req.user)
        if ex_cart_parcel.exists():
            cart_parcel = ex_cart_parcel.first()
            cart_parcel.quantity += 1
            cart_parcel.name = parcel_item.name
            cart_parcel.type = parcel_item.nametype
            cart_parcel.statusParcel = parcel_item.statustype
            cart_parcel.nameposition = parcel_item.nameposition.nameposition
            if cart_parcel.quantity < 3:
                cart_parcel.save()
        else:
            cart_parcel = CartParcel.objects.create(user=req.user, parcel_item=parcel_item)
            cart_parcel.quantity = 1  
            cart_parcel.name = parcel_item.name
            cart_parcel.type = parcel_item.nametype
            cart_parcel.statusParcel = parcel_item.statustype
            cart_parcel.nameposition = parcel_item.nameposition.nameposition
            if cart_parcel.quantity < 3:
                cart_parcel.save()
        return redirect('/user_cart')
    else:
        if queue_item:
            if parcel_item.quantity > 0 :    
                parcel_item.quantity -= 1
                parcel_item.borrow_count += 1  
                parcel_item.save()
                ex_cart_parcel = CartParcel.objects.filter(parcel_item=parcel_item, user=req.user)
                if ex_cart_parcel.exists():
                    cart_parcel = ex_cart_parcel.first()
                    cart_parcel.quantity += 1
                    cart_parcel.name = parcel_item.name
                    cart_parcel.type = parcel_item.nametype
                    cart_parcel.statusParcel = parcel_item.statustype
                    cart_parcel.nameposition = parcel_item.nameposition.nameposition
                    if cart_parcel.quantity < 3:
                        cart_parcel.save()
                else:
                    cart_parcel = CartParcel.objects.create(user=req.user, parcel_item=parcel_item)
                    cart_parcel.quantity = 1
                    cart_parcel.name = parcel_item.name
                    cart_parcel.type = parcel_item.nametype
                    cart_parcel.statusParcel = parcel_item
                    cart_parcel.statusParcel = parcel_item.statustype
                    cart_parcel.nameposition = parcel_item.nameposition.nameposition
                    cart_parcel.borrow_count += 1
                    if cart_parcel.quantity < 3:
                        cart_parcel.save()
                queue_item.delete()
                return redirect('/user_cart')
        else:
            queue_item = QueueParcel.objects.create(user=req.user, queue_item=parcel_item, name=parcel_item.name, type=parcel_item.nametype)
            queue_item.name = parcel_item.name
            queue_item.type = parcel_item.nametype
            #queue_item.statusParcel = parcel_item.statusParcel
            queue_item.save()
            messages.success(req, 'จองคิวสำเร็จ!')
        return redirect('/user_queue')
    
    
def cart_update(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None:
        return redirect('/')
    parcel_item = Add_Parcel.objects.get(id=id)
    if parcel_item.quantity > 0 or parcel_item.quantitytype == "∞":
        cart_parcel = CartParcel.objects.get(parcel_item=parcel_item, user=req.user)
        if cart_parcel.quantity < 3:
            cart_parcel.quantity += 1
            cart_parcel.save()
            if parcel_item.quantitytype == "∞":  
                parcel_item.borrow_count += 1
                parcel_item.save()
            else:
                parcel_item.quantity -= 1
                parcel_item.save()
    return redirect('/user_cart')

def cart_notupdate(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None:
        return redirect('/')
    parcel_item = Add_Parcel.objects.get(id=id)
    if parcel_item.quantity > 0 or parcel_item.quantitytype == "∞":
        cart_parcel = CartParcel.objects.get(parcel_item=parcel_item, user=req.user)
        if cart_parcel.quantity > 0 or parcel_item.quantitytype == "∞":
            parcel_item.quantity += 1
            cart_parcel.quantity -= 1
            parcel_item.save()
            cart_parcel.save()
        elif cart_parcel.quantity > 0 or parcel_item.quantitytype == "∞":  
            parcel_item.borrow_count -= 1
            parcel_item.save()
        elif cart_parcel.quantity < 1 or parcel_item.quantitytype == "∞":
            cart_parcel.delete()
    return redirect('/user_cart')

def cart_notupdate(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None:
        return redirect('/')
    parcel_item = Add_Parcel.objects.get(id=id)
    if parcel_item.quantity > 0 or parcel_item.quantitytype == "∞":
        cart_parcel = CartParcel.objects.get(parcel_item=parcel_item, user=req.user)
        if cart_parcel.quantity > 0 or parcel_item.quantitytype == "∞":
            if cart_parcel.quantity > 0 and parcel_item.quantitytype == "∞":
                parcel_item.borrow_count -= 1
                cart_parcel.quantity -= 1
                cart_parcel.save()
                parcel_item.save()  
            else:
                parcel_item.quantity += 1
                cart_parcel.quantity -= 1
                parcel_item.borrow_count -= 1
                cart_parcel.save()
                parcel_item.save()  
        elif cart_parcel.quantity < 1:
            cart_parcel.delete()
    return redirect('/user_cart')

def user_queue(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    AllQueueParcel = QueueParcel.objects.filter(user=req.user)
    AllQueueParcelList = QueueParcel.objects.filter(user=req.user)
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllQueueParcel = AllQueueParcel.order_by('-date_q')
        elif req.GET['sort'] == 'name':
            AllQueueParcel = AllQueueParcel.order_by('name')    
        elif req.GET['sort'] == 'type':
            AllQueueParcel = AllQueueParcel.order_by('type')    
        elif req.GET['sort'] == 'default':
            AllQueueParcel = QueueParcel.objects.filter(user=req.user).order_by('date_q')
        else:
            last_sort = 'default'
            AllQueueParcel = QueueParcel.objects.filter(user=req.user).order_by('date_q')
    else:
        last_sort = 'default'
        AllQueueParcel = QueueParcel.objects.filter(user=req.user).order_by('date_q')
    search_q = ""
    if 'search_q' in req.GET:
        search_q = req.GET['search_q']
        AllQueueParcel = AllQueueParcel.filter(Q(name__contains=search_q)|Q(type__contains=search_q))
    p_listqueue = Paginator(AllQueueParcelList, 8)
    page_num = req.GET.get('page', 1)
    try:
        pagequeue = p_listqueue.page(page_num)
    except:
        pagequeue = p_listqueue.page(1)  
    context ={
        'navbar' : 'user_queue',
        "AllQueueParcel" : AllQueueParcel,
        "pagequeue" : pagequeue,
        "Total" : Total,
        "search_q" : search_q,
        "last_sort" : last_sort,
    }
    return render(req, 'pages/user_queue.html', context)

def add_multiple_to_borrow_parcel(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    description = req.POST.get('description')
    if not description or description == "":
        return redirect('/user_cart') 
    cart_parcels = CartParcel.objects.filter(user=req.user)
    start_date = req.POST.get('start_date')
    if start_date is None or start_date == "":
        start_date = date.today()
    else:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    for cart_parcel in cart_parcels:
        add_parcel = Add_Parcel.objects.get(id=cart_parcel.parcel_item.id)
        if start_date < date.today():
            pass
        else:
            loan_parcel = LoanParcel()
            loan_parcel.user = req.user
            loan_parcel.start_date = start_date
            loan_parcel.description = description
            loan_parcel.name = cart_parcel.name
            loan_parcel.parcel_item = add_parcel
            loan_parcel.quantity = cart_parcel.quantity
            loan_parcel.type = cart_parcel.type
            loan_parcel.statusParcel = cart_parcel.statusParcel
            loan_parcel.nameposition = cart_parcel.nameposition
            loan_parcel.save()
            cart_parcel.delete()
            messages.success(req, 'รอการอนุมัติ!')
            users = User.objects.filter(Q(right="เจ้าหน้าที่")|Q(right="ผู้ดูแลระบบ"))
            datetime_th = th_tz.localize(datetime.now())
            for user in users:
                if user.token:
                    url = 'https://notify-api.line.me/api/notify'
                    token = user.token 
                    headers = {
                            'content-type': 'application/x-www-form-urlencoded',
                            'Authorization': 'Bearer ' + token 
                        }
                    msg = [loan_parcel.user.email, 'ยืมวัสดุรายการ : ', loan_parcel.name, 'จำนวน : ', loan_parcel.quantity, "วันที่ต้องการยืม : ", loan_parcel.start_date, 'เหตุผลการยืม : ', loan_parcel.description,'วันที่ทำรายการ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
                    msg = ' '.join(map(str, msg)) 
                    requests.post(url, headers=headers, data={'message': msg})
    return redirect('/user_borrow')

def delete_borrow_parcel(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    try:
        loan_parcel = LoanParcel.objects.get(id=id)
        parcel = loan_parcel.parcel_item
        if parcel.quantitytype == "∞":
            parcel.borrow_count -= loan_parcel.quantity
            parcel.save()
            loan_parcel.delete()
            messages.success(req, 'ยกเลิกการยืม!')
            return redirect('/')
        else:
            parcel.quantity += loan_parcel.quantity
            parcel.borrow_count -= loan_parcel.quantity
            parcel.save()
            loan_parcel.delete()
            messages.success(req, 'ยกเลิกการยืม!')
            return redirect('/')
    except LoanParcel.DoesNotExist:
        return redirect('/user_cart')
    
    
def delete_add_to_cart(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    if CartParcel.objects.filter(id=id).exists():
        obj = CartParcel.objects.get(id=id)
        parcel_obj = obj.parcel_item
        if parcel_obj.quantitytype == "∞":
            parcel_obj.borrow_count -= obj.quantity
            parcel_obj.save()
            obj.delete()
            messages.success(req, 'ลบรายการสำเร็จ!')
            return redirect('/user_cart')
        else:
            parcel_obj.quantity += obj.quantity
            parcel_obj.borrow_count -= obj.quantity
            parcel_obj.save()
            obj.delete()   
            messages.success(req, 'ลบรายการสำเร็จ!')
            return redirect('/user_cart')
    else:
        return redirect('/user_cart')
    
def delete_queue(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    obj = QueueParcel.objects.get(id=id)
    obj.delete()
    return redirect('/user_queue')          

def add_to_cart_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    durable_item = Add_Durable.objects.get(id=id)
    queue_item = QueueDurable.objects.filter(user=req.user, queue_item=durable_item).first()
    if durable_item.quantity > 0 or durable_item.quantitytype == "∞":
        if durable_item.quantitytype == "∞":
            durable_item.borrow_count += 1  
            durable_item.save()
            queue_item.delete()
            messages.success(req, 'เพิ่มรายการสำเร็จ!')
        else:
            durable_item.quantity -= 1
            durable_item.borrow_count += 1  
            durable_item.save()
            queue_item.delete()
            messages.success(req, 'เพิ่มรายการสำเร็จ!')
        existing_cart_durable = CartDurable.objects.filter(durable_item=durable_item, user=req.user)
        if existing_cart_durable.exists():
            cart_durable = existing_cart_durable.first()
            cart_durable.quantity += 1
            cart_durable.name = durable_item.name
            cart_durable.type = durable_item.nametype
            cart_durable.statusDurable = durable_item.statustype
            cart_durable.nameposition = durable_item.nameposition.nameposition
            if cart_durable.quantity < 3:
                cart_durable.save()
        else:
            cart_durable = CartDurable.objects.create(user=req.user, durable_item=durable_item)
            cart_durable.quantity = 1  
            cart_durable.name = durable_item.name
            cart_durable.type = durable_item.nametype
            cart_durable.statusDurable = durable_item.statustype
            cart_durable.nameposition = durable_item.nameposition.nameposition
            if cart_durable.quantity < 3:
                cart_durable.save()
        return redirect('/user_cart')
    else:
        if queue_item:
            if durable_item.quantity > 0 or durable_item.quantitytype == "∞":
                if durable_item.quantitytype == "∞":
                    durable_item.borrow_count += 1  
                    durable_item.save()
                else:    
                    durable_item.quantity -= 1
                    durable_item.borrow_count += 1  
                    durable_item.save()
                existing_cart_durable = CartDurable.objects.filter(durable_item=durable_item, user=req.user)
                if existing_cart_durable.exists():
                    cart_durable = existing_cart_durable.first()
                    cart_durable.quantity += 1
                    cart_durable.name = durable_item.name
                    cart_durable.type = durable_item.nametype
                    cart_durable.statusDurable = durable_item.statustype
                    cart_durable.nameposition = durable_item.nameposition.nameposition
                    if cart_durable.quantity < 3:
                        cart_durable.save()
                else:
                    cart_durable = CartDurable.objects.create(user=req.user, durable_item=durable_item)
                    cart_durable.quantity = 1
                    cart_durable.name = durable_item.name
                    cart_durable.type = durable_item.nametype
                    cart_durable.statusDurable = durable_item
                    cart_durable.statusDurable = durable_item.statustype
                    cart_durable.nameposition = durable_item.nameposition.nameposition
                    cart_durable.borrow_count += 1
                    if cart_durable.quantity < 3:
                        cart_durable.save()
                queue_item.delete()
                return redirect('/user_cart')
        else:
            queue_item = QueueDurable.objects.create(user=req.user, queue_item=durable_item, name=durable_item.name, type=durable_item.nametype)
            queue_item.name = durable_item.name
            queue_item.type = durable_item.nametype
            queue_item.statusDurable = durable_item.statusDurable
            queue_item.save()
            messages.success(req, 'จองคิวสำเร็จ!')
        return redirect('/user_queue_durable')

def cart_update_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None:
        return redirect('/')
    durable_item = Add_Durable.objects.get(id=id)
    if durable_item.quantity > 0 or durable_item.quantitytype == "∞":
        cart_durable = CartDurable.objects.get(durable_item=durable_item, user=req.user)
        if cart_durable.quantity < 3:
            cart_durable.quantity += 1
            cart_durable.save()
            if durable_item.quantitytype == "∞":  
                durable_item.borrow_count += 1
                durable_item.save()
            else:
                durable_item.quantity -= 1
                durable_item.save()
    return redirect('/user_cart')

def cart_notupdate_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None:
        return redirect('/')
    durable_item = Add_Durable.objects.get(id=id)
    if durable_item.quantity > 0 or durable_item.quantitytype == "∞":
        cart_durable = CartDurable.objects.get(durable_item=durable_item, user=req.user)
        if cart_durable.quantity > 0 or durable_item.quantitytype == "∞":
            if cart_durable.quantity > 0 and durable_item.quantitytype == "∞":
                durable_item.borrow_count -= 1
                cart_durable.quantity -= 1
                cart_durable.save()
                durable_item.save()  
            else:
                durable_item.quantity += 1
                cart_durable.quantity -= 1
                durable_item.borrow_count -= 1
                cart_durable.save()
                durable_item.save()  
        elif cart_durable.quantity < 1:
            cart_durable.delete()
    return redirect('/user_cart')
    
def user_queue_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    AllQueueDurable = QueueDurable.objects.filter(user=req.user)
    AllQueueDurableList = QueueDurable.objects.all()
    if 'sort' in req.GET:
        last_sort = req.GET.get('sort', 'default')
        if req.GET['sort'] == 'latest':
            AllQueueDurable = AllQueueDurable.order_by('-date_q')
        elif req.GET['sort'] == 'name':
            AllQueueDurable = AllQueueDurable.order_by('name')    
        elif req.GET['sort'] == 'type':
            AllQueueDurable = AllQueueDurable.order_by('type')    
        elif req.GET['sort'] == 'default':
            AllQueueDurable = QueueDurable.objects.filter(user=req.user).order_by('date_q')
        else:
            last_sort = 'default'
            AllQueueDurable = QueueDurable.objects.filter(user=req.user).order_by('date_q')
    else:
        last_sort = 'default'
        AllQueueDurable = QueueDurable.objects.filter(user=req.user).order_by('date_q')
    search_q = ""
    if 'search_q' in req.GET:
        search_q = req.GET['search_q']
        AllQueueDurable = AllQueueDurable.filter(Q(name__contains=search_q)|Q(type__contains=search_q))
    p_listqueuedurable = Paginator(AllQueueDurableList, 8)
    page_num = req.GET.get('page', 1)
    try:
        pagequeuedurable = p_listqueuedurable.page(page_num)
    except:
        pagequeuedurable = p_listqueuedurable.page(1)  
    context = {
        'navbar' : 'user_queue_durable',
        "AllQueueDurable" : AllQueueDurable,
        "pagequeuedurable" : pagequeuedurable,
        "Total" : Total,
        "last_sort" : last_sort,
        "search_q" : search_q,
    }
    return render(req, 'pages/user_queue_durable.html', context)    
    
def add_multiple_to_borrow_durable(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    description = req.POST.get('description')
    if not description or description == "":
        return redirect('/user_cart') 
    cart_durable = CartDurable.objects.filter(user=req.user)
    start_date_input = req.POST.get('start_date')
    start_date = datetime.strptime(start_date_input, '%Y-%m-%d').date() if start_date_input else date.today()
    end_date_input = req.POST.get('end_date')
    for cart_durable in cart_durable:
        add_durable = Add_Durable.objects.get(id=cart_durable.durable_item.id)
        if end_date_input:
            end_date = datetime.strptime(end_date_input, '%Y-%m-%d').date()
        else:
            end_date = start_date + timedelta(days=add_durable.numdate)
        if start_date < date.today():
            pass
        elif end_date < start_date:
            pass
        else:
            loan_durable = LoanDurable()
            loan_durable.user = req.user
            loan_durable.start_date = start_date
            loan_durable.end_date = end_date
            loan_durable.description = description
            loan_durable.name = cart_durable.name
            loan_durable.durable_item = add_durable
            loan_durable.quantity = cart_durable.quantity
            loan_durable.type = cart_durable.type
            loan_durable.statusDurable = cart_durable.statusDurable
            loan_durable.nameposition = cart_durable.nameposition
            loan_durable.save()
            cart_durable.delete()
            messages.success(req, 'รออนุมัติการยืม!')
            users = User.objects.filter(Q(right="เจ้าหน้าที่")|Q(right="ผู้ดูแลระบบ"))
            datetime_th = th_tz.localize(datetime.now())
            for user in users:
                if user.token:
                    url = 'https://notify-api.line.me/api/notify'
                    token = user.token 
                    headers = {
                            'content-type': 'application/x-www-form-urlencoded',
                            'Authorization': 'Bearer ' + token 
                        }
                    msg = [loan_durable.user.email, 'ยืมวัสดุรายการ : ', loan_durable.name, 'จำนวน : ', loan_durable.quantity, "วันที่ต้องการยืม : ", 
                           loan_durable.start_date, 'กำหนดคืน : ', loan_durable.end_date, 'เหตุผลการยืม : ', loan_durable.description,'วันที่ทำรายการ : ', 
                           datetime_th.strftime("%Y-%m-%d %H:%M") ] 
                    msg = ' '.join(map(str, msg)) 
                    requests.post(url, headers=headers, data={'message': msg})
    return redirect('/user_borrow_durable')

def delete_borrow_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    try:
        loan_durable = LoanDurable.objects.get(id=id)
        durable = loan_durable.durable_item
        if durable.quantitytype == "∞":
            durable.borrow_count -= loan_durable.quantity
            durable.save()
            loan_durable.delete()
            messages.success(req, 'ยกเลิกการยืม!')
            return redirect('/')
        else:
            durable.quantity += loan_durable.quantity
            durable.borrow_count -= loan_durable.quantity
            durable.save()
            loan_durable.delete()
            messages.success(req, 'ยกเลิกการยืม!')
            return redirect('/')
    except LoanParcel.DoesNotExist:
        return redirect('/user_cart')
    
def delete_durable_add_to_cart(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    if CartDurable.objects.filter(id=id).exists():
        obj = CartDurable.objects.get(id=id)
        durable_obj = obj.durable_item
        if durable_obj.quantitytype == "∞":
            durable_obj.borrow_count -= obj.quantity
            durable_obj.save()
            obj.delete()
            messages.success(req, 'ลบรายการสำเร็จ!')
            return redirect('/user_cart')
        else:
            durable_obj.quantity += obj.quantity
            durable_obj.borrow_count -= obj.quantity
            durable_obj.save()
            obj.delete()
            messages.success(req, 'ลบรายการสำเร็จ!')
            return redirect('/user_cart')
    else:
        return redirect('/user_cart')  
    
def delete_queue_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    obj = QueueDurable.objects.get(id=id)
    obj.delete()
    return redirect('/user_queue_durable')      
    
#หน้ารายละเอียดวัสดุ
@login_required
def user_detail(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    AllParcelAll = Add_Parcel.objects.all()
    AllDurableAll = Add_Durable.objects.all()
    AllParcel = Add_Parcel.objects.filter(id=id).first()
    waiting_qParcel = QueueParcel.objects.filter(queue_item=AllParcel).count()
    context = {
        "AllParcel" : AllParcel,
        "waiting_qParcel" : waiting_qParcel,
        "AllParcelAll" : AllParcelAll,
        "AllDurableAll" : AllDurableAll,
        "Total" : Total,
    }
    return render(req,'pages/user_detail.html',context)

def user_detail_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    AllDurableAll = Add_Durable.objects.all()
    AllParcelAll = Add_Parcel.objects.all()
    AllDurable = Add_Durable.objects.filter(id=id).first()
    waiting_qDurable = QueueDurable.objects.filter(queue_item=AllDurable).count()
    if AllDurable is not None:
        waiting_period = waiting_qDurable * AllDurable.numdate
    else:
        waiting_period = None
    context = {
        "AllDurable" : AllDurable,
        "waiting_qDurable" : waiting_qDurable,
        "waiting_period": waiting_period,
        "AllDurableAll" : AllDurableAll,
        "AllParcelAll" : AllParcelAll,
        "Total" : Total,
    }
    return render(req,'pages/user_detail_durable.html',context)


#หน้ารายการวัสดุ
def user_durable_articles(req):
    if req.user.is_anonymous:
        selected_category = req.GET.get('category', None)
        AllDurable = Add_Durable.objects.all()
        AllParcel = Add_Parcel.objects.all()
        AllCategoryType = CategoryType.objects.all()
        if 'sort' in req.GET:
            last_sort = req.GET.get('sort', 'default')
            if req.GET['sort'] == 'name':
                AllParcel = AllParcel.order_by('name')
                AllDurable = AllDurable.order_by('name')
            elif req.GET['sort'] == 'quantity':
                AllParcel = AllParcel.order_by('-quantity')
                AllDurable = AllDurable.order_by('-quantity')    
            elif 'sort' in req.GET and req.GET['sort'] == 'statustype' and 'statustype' in req.GET:
                AllDurable = AllDurable.filter(statustype=req.GET['statustype']).order_by('statustype')
                AllParcel = AllParcel.filter(statustype=req.GET['statustype']).order_by('statustype')
            elif 'sort' in req.GET and req.GET['sort'] == 'nametype' and 'nametype' in req.GET:
                AllDurable = AllDurable.filter(nametype=req.GET['nametype']).order_by('nametype')
                AllParcel = AllParcel.filter(nametype=req.GET['nametype']).order_by('nametype')    
            elif req.GET['sort'] == 'category':
                AllDurable = AllDurable.filter(category=req.GET['category']).order_by('category__name_CategoryType')
                AllParcel = AllParcel.filter(category=req.GET['category']).order_by('category__name_CategoryType')
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
        context = {
            "navbar" : "user_durable_articles",
            "last_sort" : last_sort,
            "AllParcel" : AllParcel,
            "AllDurable" : AllDurable,
            "search_query" : search_query,
            "AllCategoryType" : AllCategoryType,
            "selected_category" : selected_category,
        }
        return render(req, 'pages/user_durable_articles.html', context)     
    else:          
        AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
        AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
        TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
        TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
        Total = TotalParcel + TotalDurable
        statustype_list = [i[0] for i in STATUSTYPE]
        nametype_list = [i[0] for i in NAMETYPE] 
        context = {
            "navbar" : "user_durable_articles",
            "Total" : Total,
            "nametype" : nametype_list,
        }
        return render(req, 'pages/user_durable_articles.html', context)

@login_required
def user_recommend_history(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    AllRecList = ListFromRec.objects.filter(Q(status='อนุมัติ'), user = req.user)
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
            AllRecList = ListFromRec.objects.filter(Q(status='อนุมัติ'), user = req.user).order_by('name', 'datetime')
        else:
            last_sort = 'default'
            AllRecList = ListFromRec.objects.filter(Q(status='อนุมัติ'), user = req.user).order_by('name', 'datetime')
    else:
        last_sort = 'default'
        AllRecList = ListFromRec.objects.filter(Q(status='อนุมัติ'), user = req.user).order_by('name', 'datetime')
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
        "page" : page,
        "Total" : Total,
        "last_sort" : last_sort,
        "search_rec" : search_rec,
    }
    return render(req, 'pages/user_recommend_history.html', context)     

#หน้าแนะนำวัสดุ
@login_required
def user_recommend(req):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    if req.method == "POST":
        user = req.user
        name = req.POST.get('name')
        brand = req.POST.get('brand')
        quantity = req.POST.get('quantity')
        price = req.POST.get('price')
        link = req.POST.get('link')
        description = req.POST.get('description')
        datetime = timezone.now()
        obj = ListFromRec(user=user, name=name, brand=brand, quantity=quantity, 
                          price=price, link=link, description=description, datetime=datetime)
        obj.save()
        messages.success(req, 'แนะนำรายการสำเร็จ!')
        users = User.objects.filter(Q(right="เจ้าหน้าที่")|Q(right="ผู้ดูแลระบบ"))
        datetime_th = th_tz.localize(datetime.now())
        for user in users:
            if user.token:
                url = 'https://notify-api.line.me/api/notify'
                token = user.token 
                headers = {
                    'content-type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Bearer ' + token 
                }
                msg = ['ผู้แนะนำรายการเข้าระบบ : ', obj.user.email ,'รายการ : ', name, 'วันที่ทำรายการ : ', datetime_th.strftime("%Y-%m-%d %H:%M") ] 
                msg = ' '.join(map(str, msg)) 
                requests.post(url, headers=headers, data={'message': msg})
        return redirect('/user_recommend')   
    else:
        obj = ListFromRec()   
    obj = ListFromRec.objects.all()   
    AllRecList = ListFromRec.objects.filter(Q(status='รออนุมัติ'), user = req.user)
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
            AllRecList = ListFromRec.objects.filter(Q(status='รออนุมัติ'), user = req.user)
        else:
            last_sort = 'default'
            AllRecList = ListFromRec.objects.filter(Q(status='รออนุมัติ'), user = req.user)
    else:
        last_sort = 'default'
        AllRecList = ListFromRec.objects.filter(Q(status='รออนุมัติ'), user = req.user)
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
        "AllRecList" : ListFromRec.objects.filter(Q(status='รออนุมัติ'), user = req.user),
        "page" : page,
        "Total" : Total,
        "last_sort" : last_sort,
        "search_rec" : search_rec,
    }
    return render(req, 'pages/user_recommend.html', context)   

@login_required
def user_recommend_edit(req,id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    obj = ListFromRec.objects.get(id=id)
    obj.name = req.POST['name']
    obj.brand = req.POST['brand']
    obj.quantity = req.POST['quantity']
    obj.price = req.POST['price']
    obj.link = req.POST['link']
    obj.description = req.POST['description']
    obj.datetime = timezone.now()
    obj.save()
    messages.success(req, 'แก้ไขการแนะนำรายการสำเร็จ!')
    return redirect('/user_recommend') 

# รายงานสถานะข้อมูลการแนะนำวัสดุเข้าสู่ระบบ
@login_required
def user_recommend_detail(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
    TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
    Total = TotalParcel + TotalDurable
    AllRecList = ListFromRec.objects.filter(id=id).first()
    context = {
        "AllRecList" : AllRecList,
        "Total" : Total,
    }
    return render( req, 'pages/user_recommend_detail.html', context)

def deleteRecList(req, id):
    if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.phone is None or req.user.token is None:
        return redirect('/')
    obj = ListFromRec.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบการแนะนำรายการสำเร็จ!')
    return redirect('/user_recommend')

def user_position(req):
    if req.user.is_anonymous:
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
                'navbar' : 'user_position',
                "items_position": items_position,
                "AllPosition" : AllPosition,
                "search_query" : search_query,
                "last_sort" : last_sort,
                }    
        return render(req, 'pages/user_position.html', context)
    else:
        AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
        AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
        TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
        TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
        Total = TotalParcel + TotalDurable
        context ={
                    'navbar' : 'user_position',
                    "Total" : Total,
                }
    return render(req, 'pages/user_position.html', context)

def pdf_print_position(req):
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