from datetime import *
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
#from myapp.task import admin_user_return_task
from myappSuper.forms import *
from django.http import HttpResponseServerError, Http404, HttpResponse
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
import csv, io, os
from django.conf import settings
from django.db import transaction



@login_required
def admin_detail(req, id):
    try:
        if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
            return redirect('Home')
        if req.user.phone is None or req.user.token is None:
            messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
            return redirect('/phone_add_number')
        AllUser = User.objects.filter(id=id).first()
        context = {
            "AllUser" : AllUser,
        }
        return render(req, "pages/admin_detail.html", context)
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})        

@login_required
def delete_user(req, id):
    try:
        if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
            return redirect('Home')
        if req.user.phone is None or req.user.token is None:
            messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
            return redirect('/phone_add_number')
        
        user = User.objects.get(id=id)
        email = user.email
        profiles = Profile.objects.filter(email=email)
        profile_staffs = ProfileStaff.objects.filter(email=email)
      
        with transaction.atomic():
            user.delete()
            profiles.delete()
            profile_staffs.delete()

        messages.success(req, 'ลบผู้ใช้สำเร็จ!')
        return redirect('/admin_user')
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})        

@login_required
def admin_user_deadline(req, id):
    try:
        if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
            return redirect('Home')
        if req.user.phone is None or req.user.token is None:
            messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
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
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})    

@login_required
def admin_user_return(req, id):
    try:
        if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right == "นักศึกษา":
            return redirect('Home')
        if req.user.phone is None or req.user.token is None:
            messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
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
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})    

@login_required
def admin_user(req):
    try:
        if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
            return redirect('Home')
        if req.user.phone is None or req.user.token is None:
            messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
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
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})    

@login_required
def admin_staff(req):
    try:
        if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
            return redirect('Home')
        if req.user.phone is None or req.user.token is None:
            messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
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
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})    

@login_required
def admin_block(req):
    try:
        if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
            return redirect('Home')
        if req.user.phone is None or req.user.token is None:
            messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
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
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})    

def person_upload(req):
    try:
        if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
            return redirect('Home')
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
                messages.success(req, 'เพิ่มรายการสำเร็จ!')
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

        try:
            csv_file = req.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(req, 'THIS IS NOT A CSV FILE')
                return redirect('person_upload')
            data_set = csv_file.read().decode('UTF-8')
            data_set = data_set.replace('"', '')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                if not Profile.objects.filter(email=column[2]).exists():
                    Profile.objects.create(
                        firstname=column[0],
                        lastname=column[1],
                        email=column[2],
                    )
            messages.success(req, 'CSV file อัพโหลดสำเร็จ')
            return redirect('person_upload')
        except Exception as e:
            messages.error(req, f'เกิดข้อผิดพลาดขณะอัพโหลด CSV file : {e}')
            return redirect('person_upload')
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})    


@login_required
def deleteProfile(req, id):
    try:
        if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
            messages.warning(req, 'คุณถูกจำกัดสิทธิ์หรือไม่ใช่ผู้ดูแลระบบ')
            return redirect('Home')
        if req.user.phone is None or req.user.token is None:
            messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
            return redirect('/phone_add_number')
        
        with transaction.atomic():
            email = Profile.objects.get(id=id).email
            Profile.objects.filter(email=email).delete()
            ProfileStaff.objects.filter(email=email).delete()
            User.objects.filter(email=email).delete()
            
        messages.success(req, 'ลบสำเร็จ!')
        return redirect("person_upload")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})    

def delete_profiles(req):
    try:
        if req.method == 'POST':
            ids = req.POST.getlist('id')
            profiles = Profile.objects.filter(id__in=ids)
            emails = [p.email for p in profiles if p.email]
            User.objects.filter(email__in=emails).delete()
            ProfileStaff.objects.filter(email__in=emails).delete()
            profiles.delete()
            return redirect('person_upload')
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})


@login_required
def csv_person_download(req):
    try:        
        file_path = os.path.join(settings.MEDIA_ROOT, 'flies/csv_person.csv')
        if not os.path.exists(file_path):
            raise Http404('File not found')
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})   

def person_upload_staff(req):
    try:
        if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
            return redirect('Home')
        if req.user.phone is None or req.user.token is None:
            return redirect('/phone_add_number')
        data = ProfileStaff.objects.all()
        if 'sort' in req.GET:
            last_sort = req.GET.get('sort', 'default')
            if req.GET['sort'] == 'firstname':
                data = ProfileStaff.objects.order_by('firstname')
            elif req.GET['sort'] == 'lastname':
                data = ProfileStaff.objects.order_by('-lastname')
            elif req.GET['sort'] == 'email':
                data = ProfileStaff.objects.order_by('email')
            elif req.GET['sort'] == 'default':
                data = ProfileStaff.objects.all()
            else:
                last_sort = 'default'
                data = ProfileStaff.objects.all()
        else:
            last_sort = 'default'
            data = ProfileStaff.objects.all()
        search_rec = ""
        if 'search_rec' in req.GET:
            search_rec = req.GET['search_rec']
            data = ProfileStaff.objects.filter(Q(firstname=search_rec)|Q(lastname=search_rec)
                                                |Q(email=search_rec))
        form = ProfileStaffForm() 
        if req.method == 'POST':
            form = ProfileStaffForm(req.POST or None)
            if form.is_valid():
                form.save()
                messages.success(req, 'เพิ่มรายการสำเร็จ!')
                return redirect('person_upload_staff')
        else:
            form = ProfileStaffForm()
        context = {
            "navbar" : "person_upload_staff",
            'profiles': data,
            "search_rec" : search_rec,
            "last_sort" : last_sort,
            "form" : form
        }

        if req.method == "GET":
            return render(req, "pages/person_upload_staff.html", context)

        try:
            csv_file = req.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(req, 'THIS IS NOT A CSV FILE')
                return redirect('person_upload_staff')
            data_set = csv_file.read().decode('UTF-8')
            data_set = data_set.replace('"', '')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                if not ProfileStaff.objects.filter(email=column[2]).exists():
                    ProfileStaff.objects.create(
                        firstname=column[0],
                        lastname=column[1],
                        email=column[2],
                    )
                messages.success(req, 'CSV file อัพโหลดสำเร็จ')
            return redirect('person_upload_staff')
        except Exception as e:
            messages.error(req, f'เกิดข้อผิดพลาดขณะอัพโหลด CSV file : {e}')
            return redirect('person_upload_staff')
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})    


@login_required
def deleteProfileStaff(req, id):
    try:
        if req.user.status == "ถูกจำกัดสิทธิ์" or req.user.right != "ผู้ดูแลระบบ":
            messages.warning(req, 'คุณถูกจำกัดสิทธิ์หรือไม่ใช่ผู้ดูแลระบบ')
            return redirect('Home')
        if req.user.phone is None or req.user.token is None:
            messages.warning(req, 'กรุณาเพิ่มเบอร์โทรศัพท์และ Token')
            return redirect('/phone_add_number')
        
        with transaction.atomic():
            email = ProfileStaff.objects.get(id=id).email
            ProfileStaff.objects.filter(email=email).delete()
            Profile.objects.filter(email=email).delete()
            User.objects.filter(email=email).delete()
            
        messages.success(req, 'ลบสำเร็จ!')
        return redirect("person_upload_staff")
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})    


def delete_profiles_staff(req):
    try:
        if req.method == 'POST':
            ids = req.POST.getlist('id')
            profiles = ProfileStaff.objects.filter(id__in=ids)
            emails = [p.email for p in profiles if p.email]
            User.objects.filter(email__in=emails).delete()
            Profile.objects.filter(email__in=emails).delete()
            profiles.delete()
            return redirect('person_upload_staff')
    except Http404:
        return render(req, '404_Error_Page.html')
    except Exception as e:
        return render(req, '404_Error_Page.html', {'message': f"Oops, something went wrong. Please try again later. Error message: {str(e)}"})   