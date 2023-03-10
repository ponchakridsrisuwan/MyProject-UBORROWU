from django.urls import path
from myappSuper.views import *
from . import views

urlpatterns = [
    path('admin_personal_info', views.admin_personal_info, name="admin_personal_info"),
    path('admin_detail/<int:id>',views.admin_detail, name="admin_detail"), #delete
    
    path('admin_user',views.admin_user, name="admin_user"),
    path('admin_user_deadline/<int:id>',views.admin_user_deadline, name="admin_user_deadline"),
    path('admin_user_return/<int:id>',views.admin_user_return, name="admin_user_return"),
    
    path('admin_staff/',views.admin_staff, name="admin_staff"),
    path('admin_block',views.admin_block, name="admin_block"),
    
    #path('admin_user_setting_detail/<int:id>',views.admin_user_setting_detail, name="admin_user_setting_detail"),
    path('person_upload',views.person_upload, name="person_upload"),
    path('deleteProfile/<int:id>',views.deleteProfile, name="deleteProfile"),
    path('delete_profiles',views.delete_profiles, name="delete_profiles"),
    
    path('person_upload_staff',views.person_upload_staff, name="person_upload_staff"),
    path('deleteProfileStaff/<int:id>',views.deleteProfileStaff, name="deleteProfileStaff"),
    path('delete_profiles_staff',views.delete_profiles_staff, name="delete_profiles_staff"),
    
    path('delete_user/<int:id>',views.delete_user, name="delete_user"),
    
    path('csv_person_download',views.csv_person_download, name="csv_person_download"),
]
