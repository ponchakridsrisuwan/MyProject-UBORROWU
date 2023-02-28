from asyncio import Queue
from datetime import *
from http.client import HTTPResponse
from django.http import HttpResponseServerError, Http404
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
import csv
import pickle
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd


def handler404(req, exception):
    return render(req, '404_Error_Page.html', status=404)
    
#หน้าหลัก
def HomePage(req):
    try:
        AllParcel = Add_Parcel.objects.all()
        AllDurable = Add_Durable.objects.all()
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
                "navbar" : "login_user_index",
                "last_sort" : last_sort,
                "selected_category" : selected_category,
                "AllCategoryType" : AllCategoryType,
                "AllParcel" : AllParcel,
                "AllDurable" : AllDurable,
                "pageparcel" : pageparcel,
                "pagedurable" : pagedurable,
                }     
        return render(req, 'pages/user_index.html', context)
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})     

def Home(req):
    try:
        if req.user.is_authenticated:
            AllParcel = Add_Parcel.objects.all()
            AllDurable = Add_Durable.objects.all()
            AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
            AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
            TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
            TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
            Total = TotalParcel + TotalDurable
            AllLoanParcel = LoanParcel.objects.filter(Q(status='รอยืนยันการรับ'), user=req.user)
            AllLoanDurable = LoanDurable.objects.filter(Q(status='รอยืนยันการรับ') , user=req.user)
            if req.user:
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
                    "navbar" : "Home",
                    "last_sort" : last_sort,
                    "Total" : Total,
                    "selected_category" : selected_category,
                    "AllCategoryType" : AllCategoryType,
                    "AllParcel" : AllParcel,
                    "AllDurable" : AllDurable,
                    "pageparcel" : pageparcel,
                    "pagedurable" : pagedurable,
                    "AllLoanParcel" : AllLoanParcel,
                    "AllLoanDurable" : AllLoanDurable,
                }    
            return render(req, 'pages/Home.html', context)
        else:
            return redirect('login')
    except Http404:
        return render(req, '404_Error_Page.html')        
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})


def phone_add_number(req):
    try:
        if req.user.is_authenticated:
            if req.method == 'POST':
                tellphone = req.POST.get('tellphone')
                token = req.POST.get('token')
                if tellphone or token:
                    req.user.tellphone = tellphone
                    req.user.token = token
                    req.user.save()
                    messages.success(req, 'เพิ่มเบอร์โทรศัพท์และเชื่อมต่อไลน์สำเร็จ!')
                    return redirect('Home')
                else:
                    messages.error(req, 'กรุณากรอกเบอร์โทรศัพท์และ Token')
                    return redirect('/phone_add_number')
            else:
                return render(req, 'phone_add_number.html') 
        else:
            return redirect('login')    
    except Http404:
        return render(req, '404_Error_Page.html')        
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})

@login_required    
def user_personal_info(req):
    try:
        if req.user.is_authenticated:
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
            AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
            TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
            TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
            Total = TotalParcel + TotalDurable
            context = {
                "Total" : Total,
            }
            return render(req, 'pages/user_personal_info.html', context)
        else:
            return redirect('login')
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})     

#หน้ายืม
@login_required
def user_borrow(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
                AllLoanParcel = AllLoanParcel.filter(Q(name__contains=search_parcel))
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
        else:
            return redirect('login')
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})

@login_required    
def user_borrow_durable(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
                AllLoanDurable = AllLoanDurable.filter(Q(name__contains=search_durable))
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
        else:
            return redirect('login')
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})

@login_required
def confirm_parcel(req,id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            AllLoanParcel = LoanParcel.objects.filter(id=id).first()
            AllLoanParcel.status = 'ยืมสำเร็จ'
            AllLoanParcel.save()
            messages.success(req, 'ยืมสำเร็จ!')
            return redirect('/user_history')
        else:
            return redirect('login')
    except Http404:
        return render(req, '404_Error_Page.html')        
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})
  

@login_required
def confirm_durable(req,id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            AllLoanDurable = LoanDurable.objects.filter(id=id).first()
            AllLoanDurable.status = 'กำลังยืม'
            AllLoanDurable.save()
            messages.success(req, 'กำลังยืม!')
            return redirect('/user_borrowed')
        return redirect('login')
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})


@login_required
def return_durable(req,id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect('login')
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})

#หน้าคืน
@login_required
def user_borrowed(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
                AllLoanDurable = AllLoanDurable.filter(Q(name__contains=search_durable))    
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})

#หน้าประวัติ
@login_required
def user_history(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
                AllLoanParcel = AllLoanParcel.filter(Q(name__contains=search_parcel))
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})
    
@login_required
def user_history_durable(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
                AllLoanDurable = AllLoanDurable.filter(Q(name__contains=search_durable))
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})

#หน้ายืม
@login_required
def user_cart(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})      

@login_required
def add_to_cart(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            parcel_item = Add_Parcel.objects.get(id=id)
            if parcel_item.quantity > 0 or parcel_item.quantitytype == "∞":
                if parcel_item.quantitytype == "∞":
                    cart_parcel = CartParcel.objects.create(user=req.user, parcel_item=parcel_item)
                    parcel_item.borrow_count += 1  
                    cart_parcel.quantity = 1  
                    cart_parcel.name = parcel_item.name
                    cart_parcel.type = parcel_item.nametype
                    cart_parcel.statusParcel = parcel_item.statustype
                    cart_parcel.nameposition = parcel_item.nameposition.nameposition
                    if cart_parcel.quantity < 3:
                        cart_parcel.save()
                    parcel_item.save()
                    messages.success(req, 'เพิ่มรายการสำเร็จ!')
                else:
                    cart_parcel = CartParcel.objects.create(user=req.user, parcel_item=parcel_item)
                    parcel_item.quantity -= 1
                    parcel_item.borrow_count += 1  
                    cart_parcel.quantity = 1  
                    cart_parcel.name = parcel_item.name
                    cart_parcel.type = parcel_item.nametype
                    cart_parcel.statusDurable = parcel_item.statustype
                    cart_parcel.nameposition = parcel_item.nameposition.nameposition
                    if cart_parcel.quantity < 3:
                        cart_parcel.save()
                    parcel_item.save()
                    messages.success(req, 'เพิ่มรายการสำเร็จ!')
                queue_parcel = QueueParcel.objects.filter(user=req.user, queue_item=parcel_item).delete()
            return redirect('/user_cart')
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})   


@login_required
def add_to_queue(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            parcel_item = Add_Parcel.objects.get(id=id)
            queue_parcel = QueueParcel.objects.create(user=req.user, queue_item=parcel_item)
            queue_parcel.name = parcel_item.name
            queue_parcel.type = parcel_item.nametype
            queue_parcel.is_borrowed = False
            queue_parcel.save()
            messages.success(req, 'จองคิวสำเร็จ!')
            return redirect('/user_queue')
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

 
@login_required    
def cart_update(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required
def cart_notupdate(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
                if cart_parcel.quantity < 0:
                    cart_parcel.delete()
            return redirect('/user_cart')
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required
def user_queue(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required
def add_multiple_to_borrow_parcel(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required
def delete_borrow_parcel(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            try:
                loan_parcel = LoanParcel.objects.get(id=id)
                parcel = loan_parcel.parcel_item
                if parcel.quantitytype == "∞":
                    parcel.borrow_count -= loan_parcel.quantity
                    parcel.save()
                    loan_parcel.delete()
                    messages.success(req, 'ยกเลิกการยืม!')
                    return redirect('Home')
                else:
                    parcel.quantity += loan_parcel.quantity
                    parcel.borrow_count -= loan_parcel.quantity
                    parcel.save()
                    loan_parcel.delete()
                    messages.success(req, 'ยกเลิกการยืม!')
                    return redirect('Home')
            except LoanParcel.DoesNotExist:
                return redirect('/user_cart')
        else:
            return redirect("login")    
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         
    

@login_required    
def delete_add_to_cart(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")    
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         
 
@login_required    
def delete_queue(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            obj = QueueParcel.objects.get(id=id)
            obj.delete()
            return redirect('/user_queue')          
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required
def add_to_cart_durable(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            durable_item = Add_Durable.objects.get(id=id)
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
                    messages.success(req, 'เพิ่มรายการสำเร็จ!')    
                else:
                    cart_durable = CartDurable.objects.create(user=req.user, durable_item=durable_item)
                    cart_durable.quantity = 1  
                    cart_durable.name = durable_item.name
                    cart_durable.type = durable_item.nametype
                    cart_durable.statusDurable = durable_item.statustype
                    cart_durable.nameposition = durable_item.nameposition.nameposition
                    if cart_durable.quantity < 3:
                        cart_durable.save()
                    messages.success(req, 'เพิ่มรายการสำเร็จ!')    
                queue_durable = QueueDurable.objects.filter(user=req.user, queue_item=durable_item).delete()    
            return redirect('/user_cart')
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         
    
@login_required
def add_to_queue_durable(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            durable_item = Add_Durable.objects.get(id=id)
            queue_durable = QueueDurable.objects.create(user=req.user, queue_item=durable_item)
            queue_durable.name = durable_item.name
            queue_durable.type = durable_item.nametype
            queue_durable.is_borrowed = False
            queue_durable.save()
            messages.success(req, 'จองคิวสำเร็จ!')
            return redirect('/user_queue_durable')    
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required
def cart_update_durable(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         


@login_required
def cart_notupdate_durable(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
                if cart_durable.quantity < 1:
                    cart_durable.delete()
            return redirect('/user_cart')
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required    
def user_queue_durable(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         
 
@login_required    
def add_multiple_to_borrow_durable(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required
def delete_borrow_durable(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            try:
                loan_durable = LoanDurable.objects.get(id=id)
                durable = loan_durable.durable_item
                if durable.quantitytype == "∞":
                    durable.borrow_count -= loan_durable.quantity
                    durable.save()
                    loan_durable.delete()
                    messages.success(req, 'ยกเลิกการยืม!')
                    return redirect('Home')
                else:
                    durable.quantity += loan_durable.quantity
                    durable.borrow_count -= loan_durable.quantity
                    durable.save()
                    loan_durable.delete()
                    messages.success(req, 'ยกเลิกการยืม!')
                    return redirect('Home')
            except LoanParcel.DoesNotExist:
                return redirect('/user_cart')
        else:
            return redirect("login")    
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required    
def delete_durable_add_to_cart(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")    
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required    
def delete_queue_durable(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            obj = QueueDurable.objects.get(id=id)
            obj.delete()
            return redirect('/user_queue_durable')      
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         
    
#หน้ารายละเอียดวัสดุ
@login_required
def user_detail(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
            AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
            TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
            TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
            Total = TotalParcel + TotalDurable
            AllParcel = Add_Parcel.objects.filter(id=id).first()
            OnlyParcel = Add_Parcel.objects.first()
            category = OnlyParcel.category
            AllParcelAll = Add_Parcel.objects.filter(category=category).exclude(id=AllParcel.id)
            waiting_qParcel = QueueParcel.objects.filter(queue_item=AllParcel).count()
            df = pd.read_csv('myapp/myapp_loanparcel.csv')
            df = df.drop(["id","date_add","start_date","description","reasonfromstaff","status","name"
                        ,"type","quantity","statusParcel","quantitytype","nameposition"], axis = 1)
            df = df.drop_duplicates().reset_index(drop=True)
            df = df.pivot(index='parcel_item_id', columns='user_id', values='user_id')
            df = df.notnull().astype(int)
            freq_item = apriori(df, min_support=0.03, use_colnames=True)
            rules = association_rules(freq_item, metric="confidence", min_threshold=0.03)
            high_sc = rules[(rules['support'] >= 0.03) & (rules['confidence'] >= 0.03)]
            items = high_sc[(high_sc['support'] >= 0.03) & (high_sc['confidence'] >= 0.03)]['antecedents'].tolist()
            item_ids = set([int(i) for i in [item for sublist in items for item in sublist]])
            rec_parcels = Add_Parcel.objects.filter(id__in=item_ids).exclude(id=AllParcel.id)
            
            p_listparcel = Paginator(AllParcelAll, 8)
            page_num = req.GET.get('page', 1)
            try:
                pageparcel = p_listparcel.page(page_num)
            except:
                pageparcel = p_listparcel.page(1)     
                
            context = {
                "AllParcel": AllParcel,
                "waiting_qParcel" : waiting_qParcel,
                "AllParcelAll" : AllParcelAll,
                "Total" : Total,
                "rec_parcels": rec_parcels,
                "pageparcel" : pageparcel,
            }
            return render(req,'pages/user_detail.html',context)
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required
def user_detail_durable(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
            AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
            TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
            TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
            Total = TotalParcel + TotalDurable
            AllDurable = Add_Durable.objects.filter(id=id).first()
            OnlyDurable = Add_Durable.objects.first()
            category = OnlyDurable.category
            AllDurableAll = Add_Durable.objects.filter(category=category).exclude(id=AllDurable.id)
            waiting_qDurable = QueueDurable.objects.filter(queue_item=AllDurable).count()
            df = pd.read_csv('myapp/myapp_loandurable.csv')
            df = df.drop(["id","date_add","start_date","end_date","description","reasonfromstaff","status"
                        ,"name","type","quantity","statusDurable","quantitytype","nameposition"], axis = 1)
            df = df.drop_duplicates().reset_index(drop=True)
            df = df.pivot(index='durable_item_id', columns='user_id', values='user_id')
            df = df.notnull().astype(int)
            freq_item = apriori(df, min_support=0.3, use_colnames=True)
            rules = association_rules(freq_item, metric="confidence", min_threshold=0.6)
            high_sc = rules[(rules['support'] >= 0.7) & (rules['confidence'] >= 0.7)]
            items = high_sc[(high_sc['support'] >= 0.7) & (high_sc['confidence'] >= 0.7)]['antecedents'].tolist()
            item_ids = set([int(i) for i in [item for sublist in items for item in sublist]])
            rec_durable = Add_Durable.objects.filter(id__in=item_ids).exclude(id=AllDurable.id)
            if AllDurable is not None:
                waiting_period = waiting_qDurable * AllDurable.numdate
            else:
                waiting_period = None
                
            p_listparcel = Paginator(AllDurableAll, 8)
            page_num = req.GET.get('page', 1)
            try:
                pagedurable = p_listparcel.page(page_num)
            except:
                pagedurable = p_listparcel.page(1)             
            context = {
                "AllDurable" : AllDurable,
                "waiting_qDurable" : waiting_qDurable,
                "waiting_period": waiting_period,
                "AllDurableAll" : AllDurableAll,
                "Total" : Total,
                "rec_durable" : rec_durable,
                "pagedurable" : pagedurable,
            }
            return render(req,'pages/user_detail_durable.html',context)
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         


# หน้ารายการวัสดุ
def user_durable_articles(req):
    try:
        if req.user.is_authenticated:
            selected_category = req.GET.get('category', None)
            AllDurable = Add_Durable.objects.all()
            AllParcel = Add_Parcel.objects.all()
            AllCategoryType = CategoryType.objects.all()
            statustype_list = [i[0] for i in STATUSTYPE]
            nametype_list = [i[0] for i in NAMETYPE] 
            AllCartParcel_sum = CartParcel.objects.filter(user=req.user).aggregate(Sum('quantity'))
            AllCartDurabl_sum = CartDurable.objects.filter(user=req.user).aggregate(Sum('quantity'))
            TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
            TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
            Total = TotalParcel + TotalDurable
            if 'sort' in req.GET:
                last_sort = req.GET.get('sort', 'default')
                if req.GET['sort'] == 'name':
                    AllParcel = AllParcel.order_by('name')
                    AllDurable = AllDurable.order_by('name')
                elif req.GET['sort'] == 'quantity':
                    AllParcel = AllParcel.order_by('-quantity')
                    AllDurable = AllDurable.order_by('-quantity')
                elif 'sort' in req.GET and req.GET['sort'] == 'statustype' and 'statustype' in req.GET:
                    AllDurable = AllDurable.filter(
                        statustype=req.GET['statustype']).order_by('statustype')
                    AllParcel = AllParcel.filter(
                        statustype=req.GET['statustype']).order_by('statustype')
                elif 'sort' in req.GET and req.GET['sort'] == 'nametype' and 'nametype' in req.GET:
                    AllDurable = AllDurable.filter(
                        nametype=req.GET['nametype']).order_by('nametype')
                    AllParcel = AllParcel.filter(
                        nametype=req.GET['nametype']).order_by('nametype')
                elif req.GET['sort'] == 'category':
                    AllDurable = AllDurable.filter(category=req.GET['category']).order_by(
                        'category__name_CategoryType')
                    AllParcel = AllParcel.filter(category=req.GET['category']).order_by(
                        'category__name_CategoryType')
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
                "navbar": "user_durable_articles",
                "last_sort": last_sort,
                "AllParcel": AllParcel,
                "AllDurable": AllDurable,
                "statustype": statustype_list,
                "nametype": nametype_list,
                "search_query": search_query,
                "AllCategoryType": AllCategoryType,
                "selected_category": selected_category,
                "Total": Total,
            }
            return render(req, 'pages/user_durable_articles.html', context)  
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         
    
def login_user_durable_articles(req):
    try:
        selected_category = req.GET.get('category', None)
        AllDurable = Add_Durable.objects.all()
        AllParcel = Add_Parcel.objects.all()
        AllCategoryType = CategoryType.objects.all()
        statustype_list = [i[0] for i in STATUSTYPE]
        nametype_list = [i[0] for i in NAMETYPE] 
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
            "statustype": statustype_list,
            "nametype": nametype_list,
        }
        return render(req, 'pages/login_user_durable_articles.html', context)   
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})     

@login_required
def user_recommend_history(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required
def user_recommend(req):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})     

@login_required
def user_recommend_edit(req,id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

# รายงานสถานะข้อมูลการแนะนำวัสดุเข้าสู่ระบบ
@login_required
def user_recommend_detail(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
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
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required
def deleteRecList(req, id):
    try:
        if req.user.is_authenticated:
            if req.user.status == "ถูกจำกัดสิทธิ์":
                messages.warning(req, 'คุณถูกจำกัดสิทธิ์')
                return redirect('Home')
            if req.user.tellphone is None or req.user.token is None:
                messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
                return redirect('/phone_add_number')
            obj = ListFromRec.objects.get(id=id)
            obj.delete()
            messages.success(req, 'ลบการแนะนำรายการสำเร็จ!')
            return redirect('/user_recommend')
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

@login_required
def delete_Multi_RecList(req):
    try:
        if req.user.is_authenticated:
            if req.method == 'POST':
                ids = req.POST.getlist('id')
                ListFromRec.objects.filter(id__in=ids).delete()
                return redirect('user_recommend')
        else:
            return redirect("login") 
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         


def user_position(req):
    try:
        if req.user.is_authenticated:
            AllDurable = Add_Durable.objects.all()
            AllParcel = Add_Parcel.objects.all()
            AllPosition =  SettingPosition.objects.all()   
            AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
            AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
            TotalParcel = AllCartParcel_sum.get('quantity__sum') or 0
            TotalDurable = AllCartDurabl_sum.get('quantity__sum') or 0
            Total = TotalParcel + TotalDurable
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
                        "Total" : Total,
                        }    
            return render(req, 'pages/user_position.html', context)
        else:
            return redirect("login")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})         

def login_user_position(req):
    try:
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
        return render(req, 'pages/login_user_position.html', context)
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})     
    
def pdf_print_position(req):
    try:
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
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})     