"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include # new
from myapp.views import *
from myappstaff.views import *
from myappSuper.views import *
from myapp.models import *
from myappstaff.models import *
from myappSuper.models import *
from django.contrib.auth import views as auth_views
from mywebsite.settings import AUTHENTICATION_BACKENDS

from django.shortcuts import redirect

def login(req):
    if req.method == 'POST':
        if req.user is not None:
            if req.user.right == "เจ้าหน้าที่":
                return redirect('/staff_report')
            elif req.user.right == "ผู้ดูแลระบบ":
                return redirect('/admin_user')
            elif req.user.phone is None:
                return redirect('/phone_add_number')
            else:
                return redirect('/')
        else:
            return redirect('/login')
    else:
        return render(req, 'login.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), #accounts/login
    #path('', views.user_index, name='user_index'), 
    path('',include('myapp.urls')),
    path('',include('myappstaff.urls')),
    path('',include('myappSuper.urls')),
    path('login/', login,name='login'),
    #path('login/', auth_views.LoginView.as_view(template_name = 'login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'logout.html'),name='logout'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()